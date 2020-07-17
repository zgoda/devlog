from __future__ import annotations

from peewee import TextField
from playhouse.migrate import SqliteMigrator, migrate

from .models import db


def add_post_description():
    field = TextField(null=True)
    migrator = SqliteMigrator(db)
    migrate(
        migrator.add_column('post', 'description', field)
    )


MIGRATIONS = {
    'add_post_description': add_post_description
}


def run_migration(name):
    migration = MIGRATIONS[name]
    migration()
