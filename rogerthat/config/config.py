# Private config vars
import os
import sys
from rogerthat.utils.class_helpers import no_setters
from rogerthat.config.utils import load_config


try:
    AppConfig = load_config("main_config")
    DBConfig = load_config("database")
    TVConfig = load_config("tradingview")
    WebConfig = load_config("web_server")
except ModuleNotFoundError:
    print("\n\nConfigs not created yet. Shutting Down.\n\n")
    sys.exit(1)


class ConfigSetup(no_setters):
    # Main App
    _project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    _app_name = AppConfig['app_name']
    _debug_mode = AppConfig['debug_mode']

    # Web
    _web_root = WebConfig['web_root']
    _wss_root = WebConfig['wss_root']
    _quart_secret_key = WebConfig['quart_secret_key']
    _quart_cookie_domain = WebConfig['quart_cookie_domain']
    _quart_cookie_domain_debug = WebConfig['quart_cookie_domain_debug']
    _quart_auth_pep = WebConfig['quart_auth_pep']
    _quart_auth_csalt = WebConfig['quart_auth_csalt']
    _quart_server_port = WebConfig['quart_server_port']

    # Database
    _database_protocol = DBConfig.get("database_protocol", "postgresql+asyncpg")
    _database_host = DBConfig.get("database_host", "localhost")
    _database_name = DBConfig.get("database_name", "rogerthat")
    _database_password = DBConfig.get("database_password", "changeme")
    _database_user_root = DBConfig.get("database_user_root", "postgres")
    _database_user = DBConfig.get("database_user", "postgres")

    # Security
    _accepted_user_agents_tv = WebConfig['accepted_user_agents_tv']
    _api_allowed_keys = WebConfig['api_allowed_keys']

    # Trading View
    _tradingview_data_fields = TVConfig['tradingview_data_fields']


Config = ConfigSetup()
