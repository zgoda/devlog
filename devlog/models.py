import datetime

from flask_login import UserMixin

from .ext import db


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    __mapper_args__ = {
        'confirm_deleted_rows': False,
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    blurb = db.Column(db.Text)
    email = db.Column(db.String(200))
    access_token = db.Column(db.Text)
    oauth_service = db.Column(db.String(50))
    remote_user_id = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        db.Index('user_remote_id', 'oauth_service', 'remote_user_id'),
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


class Blog(db.Model):

    __tablename__ = 'blog'

    __mapper_args__ = {
        'confirm_deleted_rows': False,
    }

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('blogs', lazy='dynamic'))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    name = db.Column(db.String(200), nullable=False)
    blurb = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    is_public = db.Column(db.Boolean, default=False)


class Post(db.Model):

    __tablename__ = 'post'

    __mapper_args__ = {
        'confirm_deleted_rows': False,
    }

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('posts', lazy='dynamic'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    blog = db.relationship('Blog', backref=db.backref('posts', lazy='dynamic'))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    title = db.Column(db.String(200))
    text = db.Column(db.Text)
    text_html = db.Column(db.Text)
    mood = db.Column(db.String(50))
    is_public = db.Column(db.Boolean, default=False)
