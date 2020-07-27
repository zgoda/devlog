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
    c_year = IntegerField()
    c_month = IntegerField()
    c_day = IntegerField()
    updated = DateTimeField(default=datetime.utcnow)
    published = DateTimeField(null=True)
    title = CharField(max_length=240)
    slug = CharField(max_length=240)
    text = TextField()
    text_html = TextField()
    summary = TextField(null=True)
    description = TextField(null=True)

    class Meta:
        indexes = (
            (('c_year', 'c_month', 'c_day', 'slug'), True),
        )

    @property
    def tags(self):
        q = (
            TaggedPost.select(TaggedPost, Tag)
            .join(Tag)
            .switch(TaggedPost)
            .where(TaggedPost.post == self)
        )
        q = q.order_by(Tag.name)
        return q


class Tag(Model):
    pk = AutoField()
    name = CharField(max_length=200, unique=True)
    slug = CharField(max_length=200, index=True)


class TaggedPost(Model):
    pk = AutoField()
    post = ForeignKeyField(Post)
    tag = ForeignKeyField(Tag)
