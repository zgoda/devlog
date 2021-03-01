from datetime import datetime

import nanoid
import peewee
import pyotp
from flask_login import UserMixin
from nanoid.resources import alphabet as nanoid_alphabet
from passlib.context import CryptContext
from peewee import (
    AutoField, CharField, DateTimeField, ForeignKeyField, IntegerField, SqliteDatabase,
    TextField,
)
from pyuca import Collator
from werkzeug.utils import cached_property

c = Collator()

pwd_context = CryptContext(schemes=['argon2'])

ALPHABET = nanoid_alphabet.replace('_', '').replace('-', '')
NANOID_LEN = 16

db = SqliteDatabase(None)


@db.collation('UCA')
def collate_natural(s1: str, s2: str) -> int:  # pragma: nocover
    if s1.lower() == s2.lower():
        return 0
    if c.sort_key(s1) < c.sort_key(s2):
        return -1
    return 1


def generate_password_hash(password: str) -> str:  # pragma: nocover
    return pwd_context.hash(password)


def check_password_hash(stored: str, password: str) -> bool:  # pragma: nocover
    return pwd_context.verify(password, stored)


def check_otp(totp: pyotp.totp.TOTP, code: str) -> bool:  # pragma: nocover
    return totp.verify(code)


def generate_provisioning_uri(totp: pyotp.totp.TOTP, name: str) -> str:
    return totp.provisioning_uri(name, issuer_name='Devlog')


def gen_permalink() -> str:
    return nanoid.generate(ALPHABET, size=NANOID_LEN)


class Model(peewee.Model):

    class Meta:
        database = db


class User(UserMixin, Model):
    pk = AutoField()
    name = CharField(max_length=100, unique=True)
    password = TextField(null=True)
    otp_secret = TextField(default=pyotp.random_base32)
    otp_reg_dt = DateTimeField(null=True)

    class Meta:
        table_name = 'users'

    def set_password(self, password: str) -> None:  # pragma: nocover
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    @cached_property
    def totp(self):
        return pyotp.totp.TOTP(self.otp_secret)

    @property
    def is_active(self):
        return True

    def get_id(self):
        return str(self.pk)

    def register_otp(self):
        self.otp_reg_dt = datetime.utcnow()
        self.save()

    @property
    def otp_registered(self) -> bool:
        return self.otp_reg_dt is not None

    @property
    def provisioning_uri(self) -> str:
        return generate_provisioning_uri(self.totp, self.name)

    def verify_otp(self, code: str) -> bool:
        return check_otp(self.totp, code)

    def verify_secrets(self, password: str, otp_code: str) -> bool:
        return self.check_password(password) and self.verify_otp(otp_code)


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


class Quip(Model):
    pk = AutoField()
    author = TextField()
    title = CharField(max_length=240, null=True)
    text = TextField()
    text_html = TextField()
    created = DateTimeField(index=True, default=datetime.utcnow)
    permalink = CharField(max_length=20, default=gen_permalink)

    class Meta:
        indexes = (
            (['permalink'], True),
        )


MODELS = [Post, Quip, Tag, TaggedPost, Link, User]
