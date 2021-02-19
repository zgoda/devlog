from __future__ import annotations

from peewee import CharField, TextField
from playhouse.migrate import SqliteMigrator, migrate

from .models import db, gen_permalink

migrator = SqliteMigrator(db)


def add_post_description():
    field = TextField(null=True)
    migrate(
        migrator.add_column('post', 'description', field)
    )


def add_quip_permalink():
    field = CharField(max_length=20, default='permalink')
    migrate(
        migrator.add_column('quip', 'permalink', field)
    )
    cursor = db.execute_sql('select pk from quip')
    for row in cursor:
        pk = row[0]
        permalink = gen_permalink()
        db.execute_sql(
            'update quip set permalink = ? where pk = ?', params=(permalink, pk)
        )
    migrate(
        migrator.add_index('quip', ['permalink'], unique=True)
    )


MIGRATIONS = {
    '001.add_post_description': add_post_description,
    '002.add_quip_permalink': add_quip_permalink,
}


def run_migration(name):
    migration = MIGRATIONS[name]
    migration()
