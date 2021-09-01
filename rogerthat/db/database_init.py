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


class database_init():
    _meta = base_model.metadata
    _alembic_cfg = alembic_config(os.path.join(Config.project_root, 'alembic.ini'))

    # *************************************************************************************************
    #
    # Database Management Stuff
    #

    @classmethod
    async def alembic_current_rev(cls, input_cfg):
        captured_text = []

        def print_stdout(text, *arg):
            nonlocal captured_text
            captured_text.append(text)
        input_cfg.print_stdout = print_stdout
        alembic_cmd.current(input_cfg)
        return captured_text

    @classmethod
    async def create_db(cls):
        await db.log("Database does not exist yet, creating.")
        async with db.engine_root.connect() as conn:
            await conn.execute(text(f"CREATE DATABASE {Config.database_name}"))

    @classmethod
    async def create_tables(cls):
        await db.log("Creating tables.")
        async with db.engine.begin() as conn:
            await conn.run_sync(cls._meta.create_all)

    @classmethod
    async def initialise(cls):
        try:
            await cls.create_tables()
        except Exception:
            await cls.create_db()
            await cls.create_tables()

        current_revision = await cls.alembic_current_rev(cls._alembic_cfg)
        if len(current_revision) == 0:
            await db.log("First time init, stamping revision.")
            alembic_cmd.stamp(cls._alembic_cfg, "head")
        else:
            await db.log("Running alembic migration.")
            alembic_cmd.upgrade(cls._alembic_cfg, "head")

    # async def wipe_and_create_db(cls):
    #     """
    #     Completely wipe and recreate all tables
    #     """
    #     async with db.engine.begin() as conn:
    #         await conn.run_sync(cls._meta.drop_all)
    #         await conn.run_sync(cls._meta.create_all, checkfirst=False)
    #     return True
