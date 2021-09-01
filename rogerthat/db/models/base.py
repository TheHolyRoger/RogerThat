from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import (
    declarative_base,
)
from sqlalchemy.future import select
from rogerthat.db.engine import db


# Setup SQL BaseModel
base_model = declarative_base()


# Base DB Model functions class
class db_model_base():

    # *************************************************************************************************
    #
    # Table Model Functions: Generic
    #

    async def db_save(self):
        """
        Save one.
        """
        result = None
        async with AsyncSession(db.engine,
                                expire_on_commit=False) as session:
            async with session.begin():
                session.add_all([self])
                result = self
        return result

    @classmethod
    async def db_find(cls,
                      ByID='current'):
        """
        Find one object by ID.
        """
        async with AsyncSession(db.engine,
                                expire_on_commit=False) as session:
            async with session.begin():
                if ByID is not None:
                    stmt = select(cls).where(cls.ID == ByID)
                result = (await session.execute(stmt)).fetchone()
                if result is not None:
                    result = result[0]
        return result

    async def db_delete(self):
        async with AsyncSession(db.engine,
                                expire_on_commit=False) as session:
            async with session.begin():
                await session.delete(self)
                # make_transient(self)
        return True

    def __repr__(self):
        RemoveVars = ['metadata', 'registry']
        localvars = list([k for k in dir(self) if ('_' not in k and k not in RemoveVars)])
        localvars = {k: getattr(self, k) for k in localvars}
        return f"{localvars}"
