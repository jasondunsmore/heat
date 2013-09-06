import sqlalchemy


def upgrade(migrate_engine):
    meta = sqlalchemy.MetaData()
    meta.bind = migrate_engine

    stack_lock = sqlalchemy.Table(
        'stack_lock', meta,
        sqlalchemy.Column('id',
                          sqlalchemy.Integer,
                          primary_key=True,
                          nullable=False),
        sqlalchemy.Column('created_at', sqlalchemy.DateTime),
        sqlalchemy.Column('updated_at', sqlalchemy.DateTime),
        sqlalchemy.Column('stack_id', sqlalchemy.String(length=36),
                          sqlalchemy.ForeignKey('stack.id'),
                          nullable=False),
        sqlalchemy.Column('engine_id', sqlalchemy.String(length=64))
    )
    sqlalchemy.Table('resource', meta, autoload=True)
    stack_lock.create()


def downgrade(migrate_engine):
    meta = sqlalchemy.MetaData()
    meta.bind = migrate_engine

    stack_lock = sqlalchemy.Table('stack_lock', meta, autoload=True)
    stack_lock.drop()
