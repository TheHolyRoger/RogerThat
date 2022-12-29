from sqlalchemy import create_engine

from alembic.migration import MigrationContext
from rogerthat.config.config import Config


def fetch_alembic_revision():

    url = (f"postgresql://{Config.get_inst().database_user}:{Config.get_inst().database_password}@"
           f"{Config.get_inst().database_host}/{Config.get_inst().database_name}")
    engine = create_engine(url)
    conn = engine.connect()

    context = MigrationContext.configure(conn)
    current_rev = context.get_current_revision()
    return current_rev
