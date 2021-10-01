# Private config vars
import os
from rogerthat.utils.class_helpers import no_setters
from rogerthat.config.loader import config_loader


_loaded_configs = config_loader()
_app_config = _loaded_configs.app_config
_db_config = _loaded_configs.db_config
_tv_config = _loaded_configs.tv_config
_web_config = _loaded_configs.web_config


class ConfigSetup(no_setters):
    # Main App
    _project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    _app_name = _app_config['app_name']
    _debug_mode = _app_config['debug_mode']
    _rebroadcast_on_ws_connect = _app_config.get('rebroadcast_on_ws_connect', True)
    _include_extra_order_fields = _app_config.get('include_extra_order_fields', False)

    # Web
    _server_host = _web_config['server_host']
    _web_root = _web_config['web_root']
    _wss_root = _web_config['wss_root']
    _quart_secret_key = _web_config['quart_secret_key']
    _quart_cookie_domain_debug = _web_config['quart_cookie_domain_debug']
    _quart_auth_pep = _web_config['quart_auth_pep']
    _quart_auth_csalt = _web_config['quart_auth_csalt']
    _quart_server_port = _web_config['quart_server_port']
    _protect_with_cloudflare_firewall_rules = _web_config.get('protect_with_cloudflare_firewall_rules', False)

    # Database
    _database_protocol = _db_config.get("database_protocol", "postgresql+asyncpg")
    _database_host = _db_config.get("database_host", "localhost")
    _database_name = _db_config.get("database_name", "rogerthat")
    _database_password = _db_config.get("database_password", "changeme")
    _database_user_root = _db_config.get("database_user_root", "postgres")
    _database_user = _db_config.get("database_user", "postgres")

    # Security
    _accepted_user_agents_tv = _web_config['accepted_user_agents_tv']
    _api_allowed_keys_tv = _web_config['api_allowed_keys_tv']
    _api_allowed_keys_hbot = _web_config['api_allowed_keys_hbot']
    _disable_websocket_authentication = _web_config.get('disable_websocket_authentication', False)

    # Trading View
    _tradingview_descriptor_fields = _tv_config['tradingview_descriptor_fields']


Config = ConfigSetup()
