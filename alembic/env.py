from __future__ import with_statement

from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import sys


#from sqlalchemy.ext.declarative import as_declarative, declared_attr

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'alembic revision --autogenerate -m "name of version"' support
# from myapp import mymodel
#!!!target_metadata = mymodel.Base.metadata!!!
# target_metadata = None

sys.path = ['', '..'] + sys.path[1:]

from app.models import Base
from app.db.session import SQLALCHEMY_DATABASE_URI

target_metadata = Base.metadata
SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI


# class_registry: t.Dict = {}
# 
# 
# @as_declarative(class_registry=class_registry)
# class Base:
#     id: t.Any
#     __name__: str
# 
#     # Generate __tablename__ automatically from classname
#     @declared_attr
#     def __tablename__(cls) -> str:
#         return cls.__name__.lower()

def get_url():
    return SQLALCHEMY_DATABASE_URI


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

