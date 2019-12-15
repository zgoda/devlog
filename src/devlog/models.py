from __future__ import annotations

import datetime
from typing import Optional

from flask_login import UserMixin
from sqlalchemy_utils import observes

from .sec import pwd_context
from .ext import db
from .utils.models import MarkupField, SlugField, TextProcessingMixin


class User(db.Model, UserMixin, TextProcessingMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  # noqa: A003
    name = db.Column(db.String(200))
    slug = db.Column(db.String(200), index=True)
    blurb = db.Column(db.Text)
    blurb_html = db.Column(db.Text)
    blurb_markup_type = db.Column(db.String(50))
    email = db.Column(db.String(200), nullable=False, unique=True)
    email_confirmed = db.Column(db.Boolean, default=False)
    confirmation_token = db.Column(db.String(200))
    confirmation_sent_dt = db.Column(db.DateTime)
    confirmed_dt = db.Column(db.DateTime)
    password = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, default=True)
    public = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    default_language = db.Column(db.String(20), default='pl')
    timezone = db.Column(db.String(80), default='Europe/Warsaw')

    def set_password(self, password):
        self.password = pwd_context.hash(password)

    def check_password(self, s):
        return pwd_context.verify(s, self.password)

    @property
    def display_name(self):
        return self.name or self.email

    @property
    def effective_public(self):
        return self.public

    @classmethod
    def markup_fields(cls):
        return [
            MarkupField(
                source='blurb', dest='blurb_html', processor='blurb_markup_type'
            )
        ]

    @classmethod
    def slug_fields(cls):
        return [SlugField(source='name', dest='slug')]

    def is_active(self):
        return self.active

    @classmethod
    def get_by_email(cls, email) -> Optional[User]:
        return cls.query.filter_by(email=email).first()

    def has_blogs(self):
        return self.blogs.count() > 0

    def recent_blogs(self, limit=5):
        return self.blogs.order_by(db.desc(Blog.updated)).limit(limit)

    def confirm_email(self):
        self.email_confirmed = True
        self.confirmed_dt = datetime.datetime.utcnow()

    def clear_email_confirmation(self):
        self.email_confirmed = False
        self.confirmed_dt = self.confirmation_token = self.confirmation_sent_dt = None


@db.event.listens_for(User, 'before_insert')
@db.event.listens_for(User, 'before_update')
def user_brefore_save(mapper, connection, target):
    User.pre_save(mapper, connection, target)


class Blog(db.Model, TextProcessingMixin):

    __tablename__ = 'blog'

    id = db.Column(db.Integer, primary_key=True)  # noqa: A003
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    user = db.relationship(
        'User', backref=db.backref('blogs', lazy='dynamic', cascade='all,delete-orphan')
    )
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow, index=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    slug = db.Column(db.String(200), index=True)
    blurb = db.Column(db.Text)
    blurb_html = db.Column(db.Text)
    blurb_markup_type = db.Column(db.String(50))
    active = db.Column(db.Boolean, default=True)
    public = db.Column(db.Boolean, default=True)
    default = db.Column(db.Boolean, default=False)
    language = db.Column(db.String(20))

    __table_args__ = (db.Index('ix_blog_active_public', 'active', 'public'),)

    @property
    def effective_public(self):
        return self.public and self.user.public

    @property
    def effective_language(self):
        return self.language or self.user.default_language

    @classmethod
    def markup_fields(cls):
        return [
            MarkupField(
                source='blurb', dest='blurb_html', processor='blurb_markup_type'
            )
        ]

    @classmethod
    def slug_fields(cls):
        return [SlugField(source='name', dest='slug')]


@db.event.listens_for(Blog, 'before_insert')
@db.event.listens_for(Blog, 'before_update')
def blog_before_save(mapper, connection, target):
    Blog.pre_save(mapper, connection, target)


class Post(db.Model, TextProcessingMixin):

    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)  # noqa: A003
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id', ondelete='cascade'))
    blog = db.relationship(
        'Blog', backref=db.backref('posts', lazy='dynamic', cascade='all,delete-orphan')
    )
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    published = db.Column(db.DateTime, index=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), index=True)
    text = db.Column(db.Text)
    text_html = db.Column(db.Text)
    text_markup_type = db.Column(db.String(50))
    summary_html = db.Column(db.Text)
    mood = db.Column(db.String(50))
    public = db.Column(db.Boolean, default=True, index=True)
    draft = db.Column(db.Boolean, default=True)
    pinned = db.Column(db.Boolean, default=False)
    language = db.Column(db.String(20))

    @property
    def effective_public(self):
        return self.public and self.blog.effective_public

    @observes('updated')
    def update_observer(self, updated):
        self.blog.updated = updated

    @classmethod
    def markup_fields(cls):
        return [
            MarkupField(source='text', dest='text_html', processor='text_markup_type')
        ]

    @classmethod
    def slug_fields(cls):
        return [SlugField(source='title', dest='slug')]

    @classmethod
    def pre_save(cls, mapper, connection, target):
        super().pre_save(mapper, connection, target)
        summary = target.text.split()[:10]
        summary = ' '.join(summary)
        target.summary_html = target.markup_to_html(summary, target.text_markup_type)
        if target.draft:
            target.published = None
        else:
            if target.published is None:
                target.published = datetime.datetime.utcnow()
        if target.language is None:
            target.language = target.blog.effective_language

    @property
    def ident(self):
        if self.draft:
            return {'post_id': self.id}
        else:
            return {
                'y': self.created.year, 'm': self.created.month, 'd': self.created.day,
                'slug': self.slug,
            }


@db.event.listens_for(Post, 'before_insert')
@db.event.listens_for(Post, 'before_update')
def post_before_save(mapper, connection, target):
    Post.pre_save(mapper, connection, target)
