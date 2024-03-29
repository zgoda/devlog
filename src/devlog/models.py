from datetime import datetime

import peewee
from peewee import (
    AutoField, CharField, DateTimeField, ForeignKeyField, IntegerField, SqliteDatabase,
    TextField,
)
from pyuca import Collator

c = Collator()

db = SqliteDatabase(None)


@db.collation('UCA')
def collate_natural(s1: str, s2: str) -> int:  # pragma: nocover
    if s1.lower() == s2.lower():
        return 0
    if c.sort_key(s1) < c.sort_key(s2):
        return -1
    return 1


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
    title = CharField(max_length=240, collation='UCA')
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
    name = CharField(max_length=200, unique=True, collation='UCA')
    slug = CharField(max_length=200, index=True)


class TaggedPost(Model):
    pk = AutoField()
    post = ForeignKeyField(Post)
    tag = ForeignKeyField(Tag)


class Link(Model):
    pk = AutoField()
    section = CharField(max_length=100, index=True, collation='UCA')
    text = TextField()
    text_html = TextField()


MODELS = [Post, Tag, TaggedPost, Link]
