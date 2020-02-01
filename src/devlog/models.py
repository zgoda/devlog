from __future__ import annotations

from datetime import datetime
from typing import Optional

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .ext import db
from .utils.models import MarkupField, SlugField, TextProcessingMixin
from .utils.text import stripping_markdown


class User(db.Model, UserMixin, TextProcessingMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  # noqa: A003
    name = db.Column(db.String(200), nullable=False, unique=True)
    blurb = db.Column(db.Text)
    blurb_html = db.Column(db.Text)
    password = db.Column(db.Text, nullable=False)
    default_language = db.Column(db.String(20), default='pl')
    timezone = db.Column(db.String(80), default='Europe/Warsaw')
    active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, s):
        return check_password_hash(self.password, s)

    @classmethod
    def markup_fields(cls):
        return [MarkupField(source='blurb', dest='blurb_html')]

    @classmethod
    def slug_fields(cls):
        return [SlugField(source='name', dest='slug')]

    def is_active(self):
        return self.active

    @classmethod
    def get_by_name(cls, name: str) -> Optional[User]:
        return cls.query.filter_by(name=name).first()

    def has_blogs(self):
        return self.blogs.count() > 0

    def recent_blogs(self, limit=5):
        return self.blogs.order_by(db.desc(Blog.updated)).limit(limit)


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
    created = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow, index=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    slug = db.Column(db.String(200), index=True)
    blurb = db.Column(db.Text)
    blurb_html = db.Column(db.Text)
    default = db.Column(db.Boolean, default=False)
    language = db.Column(db.String(20))
    active = db.Column(db.Boolean, default=True)

    @property
    def effective_language(self):
        return self.language or self.user.default_language

    @classmethod
    def markup_fields(cls):
        return [MarkupField(source='blurb', dest='blurb_html')]

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
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    author = db.relationship(
        'User', backref=db.backref('posts', lazy='dynamic', cascade='all,delete-orphan')
    )
    created = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published = db.Column(db.DateTime, index=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), index=True)
    text = db.Column(db.Text)
    text_html = db.Column(db.Text)
    summary = db.Column(db.Text)
    mood = db.Column(db.String(50))
    draft = db.Column(db.Boolean, default=True)
    pinned = db.Column(db.Boolean, default=False)
    language = db.Column(db.String(20))

    @classmethod
    def markup_fields(cls):
        return [MarkupField(source='text', dest='text_html')]

    @classmethod
    def slug_fields(cls):
        return [SlugField(source='title', dest='slug')]

    @classmethod
    def pre_save(cls, mapper, connection, target):
        super().pre_save(mapper, connection, target)
        md = stripping_markdown()
        plain_text = md.convert(target.text)
        summary = plain_text.split()[:10]
        target.summary = ' '.join(summary)
        if target.draft:
            target.published = None
        else:
            if target.published is None:
                target.published = datetime.utcnow()
        if target.language is None:
            target.language = target.blog.effective_language
        if target.author_id is None:
            target.author_id = target.blog.user_id

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
