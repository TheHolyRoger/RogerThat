from sqlalchemy.ext.asyncio import create_async_engine
from rogerthat.config.config import Config


class db_engine():
    def __init__(self,
                 db_name,
                 db_root_user='postgres',
                 db_user='postgres',
                 db_pw='pass',
                 protocol='postgresql+asyncpg',
                 db_host='localhost'):
        self._db_url_main = f"{protocol}://{db_user}:{db_pw}@{db_host}/{db_name}"
        self._db_url_root = f"{protocol}://{db_user}:{db_pw}@{db_host}/{db_root_user}"
        self._engine_main = create_async_engine(self._db_url_main,
                                                echo=Config.debug_mode)
        self._engine_root = create_async_engine(self._db_url_root,
                                                echo=Config.debug_mode,
                                                isolation_level='AUTOCOMMIT')

    @property
    def engine(self):
        return self._engine_main

    @property
    def engine_root(self):
        return self._engine_root


db = db_engine(db_name=Config.database_name,
               db_root_user=Config.database_user_root,
               db_user=Config.database_user,
               db_pw=Config.database_password,
               protocol=Config.database_protocol,
               db_host=Config.database_host)
