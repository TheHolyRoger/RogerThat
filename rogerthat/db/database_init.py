import asyncio  # noqa: F401
import os
from sqlalchemy import text
# Alembic
from alembic.config import Config as alembic_config
from alembic import command as alembic_cmd
from rogerthat.config.config import Config
from rogerthat.db.models import (
    base_model,
)
from rogerthat.db.engine import db
from rogerthat.db.fetch_alembic_revision import fetch_alembic_revision


class database_init():
    _meta = base_model.metadata
    _alembic_cfg = alembic_config(os.path.join(Config.project_root, 'alembic.ini'))

    # *************************************************************************************************
    #
    # Database Management Stuff
    #

    @classmethod
    async def create_db(cls):
        await db.log("Database does not exist yet, creating.")
        async with db.engine_root.connect() as conn:
            await conn.execute(text(f"CREATE DATABASE {Config.database_name}"))
        return True

    @classmethod
    async def create_tables(cls):
        await db.log("Creating new or missing db tables.")
        async with db.engine.begin() as conn:
            await conn.run_sync(cls._meta.create_all)
        await db.log("Done creating tables.")
        return True

    @classmethod
    async def initialise(cls):
        try:
            await cls.create_tables()
        except Exception:
            await db.log("Failed to create tables.")
            await cls.create_db()
            await cls.create_tables()

        await db.log("Checking alembic.")
        try:
            current_revision = fetch_alembic_revision()
        except Exception as e:
            await db.log(f"Alembic exception: {e}")
            current_revision = None
        if not current_revision:
            await db.log("First time init, stamping revision.")
            alembic_cmd.stamp(cls._alembic_cfg, "head")
        else:
            await db.log("Running alembic migration.")
            alembic_cmd.upgrade(cls._alembic_cfg, "head")
        return True

    # async def wipe_and_create_db(cls):
    #     """
    #     Completely wipe and recreate all tables
    #     """
    #     async with db.engine.begin() as conn:
    #         await conn.run_sync(cls._meta.drop_all)
    #         await conn.run_sync(cls._meta.create_all, checkfirst=False)
    #     return True
