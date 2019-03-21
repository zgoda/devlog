import datetime

from flask_login import UserMixin

from .ext import db
from .utils.models import TextProcessingMixin, MarkupField, SlugField


class User(db.Model, UserMixin, TextProcessingMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)  # noqa: A003
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), index=True)
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
        db.Index("ix_users_user_remote_id", "oauth_service", "remote_user_id"),
    )

    @classmethod
    def markup_fields(cls):
        return [
            MarkupField(
                source="blurb", dest="blurb_html", processor="blurb_markup_type"
            )
        ]

    @classmethod
    def slug_fields(cls):
        return [SlugField(source="name", dest="slug")]

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

    def has_blogs(self):
        return self.blogs.count() > 0

    def recent_blogs(self, limit=5):
        return self.blogs.order_by(db.desc(Blog.updated)).limit(limit)


@db.event.listens_for(User, "before_insert")
@db.event.listens_for(User, "before_update")
def user_brefore_save(mapper, connection, target):
    User.pre_save(mapper, connection, target)


class Blog(db.Model, TextProcessingMixin):

    __tablename__ = "blog"

    id = db.Column(db.Integer, primary_key=True)  # noqa: A003
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"))
    user = db.relationship(
        "User", backref=db.backref("blogs", lazy="dynamic", cascade="all,delete-orphan")
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

    __table_args__ = (db.Index("ix_blog_active_public", "active", "public"),)

    @classmethod
    def markup_fields(cls):
        return [
            MarkupField(
                source="blurb", dest="blurb_html", processor="blurb_markup_type"
            )
        ]

    @classmethod
    def slug_fields(cls):
        return [SlugField(source="name", dest="slug")]


@db.event.listens_for(Blog, "before_insert")
@db.event.listens_for(Blog, "before_update")
def blog_before_save(mapper, connection, target):
    Blog.pre_save(mapper, connection, target)


class Post(db.Model, TextProcessingMixin):

    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)  # noqa: A003
    blog_id = db.Column(db.Integer, db.ForeignKey("blog.id", ondelete="cascade"))
    blog = db.relationship(
        "Blog", backref=db.backref("posts", lazy="dynamic", cascade="all,delete-orphan")
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

    @classmethod
    def markup_fields(cls):
        return [
            MarkupField(source="text", dest="text_html", processor="text_markup_type")
        ]

    @classmethod
    def slug_fields(cls):
        return [SlugField(source="title", dest="slug")]

    @classmethod
    def pre_save(cls, mapper, connection, target):
        super().pre_save(mapper, connection, target)
        summary = target.text.split()[:10]
        target.summary_html = target.markup_to_html(summary, target.text_markup_type)


@db.event.listens_for(Post, "before_insert")
@db.event.listens_for(Post, "before_update")
def post_before_save(mapper, connection, target):
    Post.pre_save(mapper, connection, target)


class Activity(db.Model):
    __tablename__ = "activity"
    id = db.Column(db.Integer, primary_key=True)  # noqa: A003
    user_id = db.Column(db.Integer, index=True)
    activity_dt = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)
    obj_type = db.Column(db.String(200))
    obj_id = db.Column(db.Integer)
    description = db.Column(db.Text)
