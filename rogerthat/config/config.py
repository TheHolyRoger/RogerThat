# Private config vars
import os

from rogerthat.config.loader import config_loader
from rogerthat.utils.class_helpers import no_setters
from rogerthat.utils.version_number import get_version_number

_loaded_configs = config_loader()
_app_config = _loaded_configs.app_config
_db_config = _loaded_configs.db_config
_mqtt_config = _loaded_configs.mqtt_config
_tv_config = _loaded_configs.tv_config
_web_config = _loaded_configs.web_config


class Config(no_setters):
    # Main App
    _project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    _version = get_version_number(_project_root)
    _app_name = _app_config['app_name']
    _debug_mode = _app_config['debug_mode']

    # Web
    _server_host = _web_config['server_host']
    _web_root = _web_config['web_root']
    _quart_secret_key = _web_config['quart_secret_key']
    _quart_cookie_domain_debug = _web_config['quart_cookie_domain_debug']
    _quart_auth_pep = _web_config['quart_auth_pep']
    _quart_auth_csalt = _web_config['quart_auth_csalt']
    _quart_server_port = _web_config['quart_server_port']
    _protect_with_cloudflare_firewall_rules = _web_config.get('protect_with_cloudflare_firewall_rules', False)

    # MQTT
    _mqtt_enable = _mqtt_config['mqtt_enable']
    _mqtt_instance_name = _mqtt_config['mqtt_instance_name']
    _mqtt_host = _mqtt_config['mqtt_host']
    _mqtt_port = _mqtt_config['mqtt_port']
    _mqtt_username = _mqtt_config['mqtt_username'] if len(str(_mqtt_config.get('mqtt_username', '')).strip()) else ''
    _mqtt_password = _mqtt_config['mqtt_password'] if len(str(_mqtt_config.get('mqtt_password', '')).strip()) else ''
    _mqtt_ssl = _mqtt_config['mqtt_ssl']
    _mqtt_reply_topic = _mqtt_config.get("mqtt_reply_topic") or f"{_app_name}/{_mqtt_instance_name}/messages"

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

    # Trading View
    _tradingview_include_extra_fields = _tv_config.get('tradingview_include_extra_fields')
    _tradingview_exclude_fields = _tv_config.get('tradingview_exclude_fields')
