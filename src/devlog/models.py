import datetime

from flask_login import UserMixin
from flask_babel import lazy_gettext as gettext

from .ext import db
from .utils.models import MarkupProcessingMixin, MarkupFields


class User(db.Model, UserMixin, MarkupProcessingMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    blurb = db.Column(db.Text)
    blurb_html = db.Column(db.Text)
    blurb_markup_type = db.Column(db.String(50))
    email = db.Column(db.String(200), index=True)
    access_token = db.Column(db.Text)
    oauth_service = db.Column(db.String(50))
    remote_user_id = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)
    public = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        db.Index('ix_users_user_remote_id', 'oauth_service', 'remote_user_id'),
    )

    @classmethod
    def markup_fields(cls):
        return MarkupFields(
            source='blurb', dest='blurb_html', processor='blurb_markup_type',
        )

    def is_active(self):
        return self.active

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_by_remote_auth(cls, service, user_id):
        return cls.query.filter(
            cls.oauth_service == service, cls.remote_user_id == user_id
        ).first()

    def display_name(self):
        return self.name or self.email.split('@')[0] or gettext('no name')


db.event.listen(User, 'before_insert', User.process_markup)
db.event.listen(User, 'before_update', User.process_markup)


class Blog(db.Model, MarkupProcessingMixin):

    __tablename__ = 'blog'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    user = db.relationship('User', backref=db.backref('blogs', lazy='dynamic'))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    blurb = db.Column(db.Text)
    blurb_html = db.Column(db.Text)
    blurb_markup_type = db.Column(db.String(50))
    active = db.Column(db.Boolean, default=True)
    public = db.Column(db.Boolean, default=True)
    default = db.Column(db.Boolean, default=False)

    __table_args__ = (
        db.Index('ix_blog_active_public', 'active', 'public'),
    )

    @classmethod
    def markup_fields(cls):
        return MarkupFields(
            source='blurb', dest='blurb_html', processor='blurb_markup_type',
        )


db.event.listen(Blog, 'before_insert', Blog.process_markup)
db.event.listen(Blog, 'before_update', Blog.process_markup)


class Post(db.Model, MarkupProcessingMixin):

    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id', ondelete='cascade'))
    blog = db.relationship('Blog', backref=db.backref('posts', lazy='dynamic'))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    title = db.Column(db.String(200))
    text = db.Column(db.Text)
    text_html = db.Column(db.Text)
    text_markup_type = db.Column(db.String(50))
    mood = db.Column(db.String(50))
    draft = db.Column(db.Boolean, default=True)
    pinned = db.Column(db.Boolean, default=False)

    __table_args__ = (
        db.Index('ix_post_draft_pinned', 'draft', 'pinned'),
    )

    @classmethod
    def markup_fields(cls):
        return MarkupFields(
            source='text', dest='text_html', processor='text_markup_type',
        )


db.event.listen(Post, 'before_insert', Post.process_markup)
db.event.listen(Post, 'before_update', Post.process_markup)
