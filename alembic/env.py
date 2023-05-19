# Logging
# from logging.config import fileConfig
# SqlAlchemy
# Add parent to path
import sys
from pathlib import Path

from sqlalchemy import engine_from_config, pool

# Alembic
from alembic import context

sys.path.append(str(Path('.').absolute()))
from rogerthat.config.config import Config  # noqa: E402
from rogerthat.db.models import base_model  # noqa: E402
from rogerthat.utils import path_import  # noqa: F401, E402

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
alembic_config = context.config
DB_URL = "postgresql://{0}:{1}@{2}/{3}".format(Config.get_inst().database_user,
                                               Config.get_inst().database_password,
                                               Config.get_inst().database_host,
                                               Config.get_inst().database_name)
alembic_config.set_main_option('sqlalchemy.url', DB_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# fileConfig(alembic_config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

target_metadata = base_model.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


# alembic revision --autogenerate -m ""
def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = alembic_config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    alembic_online_config = alembic_config.get_section(alembic_config.config_ini_section)
    alembic_online_config['sqlalchemy.url'] = DB_URL
    connectable = engine_from_config(
        alembic_online_config,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
