from __future__ import annotations

from datetime import datetime

import peewee
from peewee import (
    AutoField, CharField, DateTimeField, ForeignKeyField, IntegerField, SqliteDatabase,
    TextField,
)

db = SqliteDatabase(None)


class Model(peewee.Model):

    class Meta:
        database = db


class Post(Model):
    pk = AutoField()
    author = TextField()
    created = DateTimeField(index=True, default=datetime.utcnow)
    c_year = IntegerField(null=True)
    c_month = IntegerField(null=True)
    c_day = IntegerField(null=True)
    updated = DateTimeField(default=datetime.utcnow)
    published = DateTimeField(null=True)
    title = CharField(max_length=240)
    slug = CharField(max_length=240, null=True)
    text = TextField()
    text_html = TextField(null=True)
    summary = TextField(null=True)

    class Meta:
        indexes = (
            (('c_year', 'c_month', 'c_day', 'slug'), True),
        )

    def tags(self, order=None):
        q = (
            TaggedPost.select(TaggedPost, Tag)
            .join(Tag)
            .switch(TaggedPost)
            .where(TaggedPost.post == self)
        )
        if isinstance(order, str):
            order = getattr(self, order, None)
        if order is not None:
            q = q.order_by(order)
        return q


class Tag(Model):
    pk = AutoField()
    name = CharField(max_length=200, unique=True)
    slug = CharField(max_length=200, index=True)


class TaggedPost(Model):
    pk = AutoField()
    post = ForeignKeyField(Post)
    tag = ForeignKeyField(Tag)
