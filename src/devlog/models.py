from __future__ import annotations

from datetime import datetime

import peewee
from peewee import (
    AutoField, CharField, DateTimeField, ForeignKeyField, SqliteDatabase, TextField,
)

db = SqliteDatabase(None)


class Model(peewee.Model):

    class Meta:
        database = db


class Post(Model):
    pk = AutoField()
    author = TextField()
    created = DateTimeField(index=True, default=datetime.utcnow)
    updated = DateTimeField(default=datetime.utcnow)
    published = DateTimeField(null=True)
    title = CharField(max_length=240)
    slug = CharField(max_length=240, index=True, null=True)
    text = TextField()
    text_html = TextField(null=True)
    summary = TextField(null=True)


class Tag(Model):
    pk = AutoField()
    name = CharField(max_length=200, unique=True)
    slug = CharField(max_length=200, index=True)


class TaggedPost(Model):
    pk = AutoField()
    post = ForeignKeyField(Post)
    tag = ForeignKeyField(Tag)
