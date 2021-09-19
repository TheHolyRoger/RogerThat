from alembic.migration import MigrationContext
from sqlalchemy import create_engine
from rogerthat.config.config import Config


def fetch_alembic_revision():

    url = (f"postgresql://{Config.database_user}:{Config.database_password}@"
           f"{Config.database_host}/{Config.database_name}")
    engine = create_engine(url)
    conn = engine.connect()

    context = MigrationContext.configure(conn)
    current_rev = context.get_current_revision()
    return current_rev
