from sqlalchemy.ext.asyncio import create_async_engine

from rogerthat.config.config import Config


class db_engine():
    _shared_instance: "db_engine" = None

    @classmethod
    def db(cls) -> "db_engine":
        if cls._shared_instance is None:
            cls._shared_instance = cls(
                db_name=Config.get_inst().database_name,
                db_root_user=Config.get_inst().database_user_root,
                db_user=Config.get_inst().database_user,
                db_pw=Config.get_inst().database_password,
                protocol=Config.get_inst().database_protocol,
                db_host=Config.get_inst().database_host)
        return cls._shared_instance

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
                                                echo=Config.get_inst().debug_mode)
        self._engine_root = create_async_engine(self._db_url_root,
                                                echo=Config.get_inst().debug_mode,
                                                isolation_level='AUTOCOMMIT')

    @property
    def engine(self):
        return self._engine_main

    @property
    def engine_root(self):
        return self._engine_root
