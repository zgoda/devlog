import datetime

from flask_login import UserMixin
from flask_babel import lazy_gettext as gettext

from .ext import db


class User(db.Model, UserMixin):

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
    is_active = db.Column(db.Boolean, default=True)
    is_public = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        db.Index('ix_users_user_remote_id', 'oauth_service', 'remote_user_id'),
    )

    def is_active(self):
        return self.is_active

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


class Blog(db.Model):

    __tablename__ = 'blog'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='set null'))
    user = db.relationship('User', backref=db.backref('blogs', lazy='dynamic'))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    blurb = db.Column(db.Text)
    blurb_html = db.Column(db.Text)
    blurb_markup_type = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    is_public = db.Column(db.Boolean, default=True)

    __table_args__ = (
        db.Index('ix_blog_active_public', 'is_active', 'is_public'),
    )


class Post(db.Model):

    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    blog = db.relationship('Blog', backref=db.backref('posts', lazy='dynamic'))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    title = db.Column(db.String(200))
    text = db.Column(db.Text)
    text_html = db.Column(db.Text)
    text_markup_type = db.Column(db.String(50))
    mood = db.Column(db.String(50))
    is_draft = db.Column(db.Boolean, default=True)
