import asyncio
from quart import (
    Quart,
)
# from quart_session import Session
from quart_auth import (
    AuthManager,
    # AuthUser,
    # login_user,
)
from rogerthat.config.config import Config
from rogerthat.app.delegate import App
from rogerthat.extensions.extension_quart_json import (
    JSONDecoder,
    JSONEncoder,
)
from rogerthat.server.routes import routes_main
from rogerthat.utils.time_date import time_in_seconds
from rogerthat.utils.misc import (
    set_bash_title,
)


#########################################################################
# *
# Quart server stuff
# *
quart_server = Quart(f"{Config.app_name}/API")
quart_server.config["QUART_AUTH_COOKIE_DOMAIN"] = Config.server_host
if Config.debug_mode:
    quart_server.config["QUART_AUTH_COOKIE_DOMAIN"] = Config.quart_cookie_domain_debug
quart_server.config["QUART_AUTH_COOKIE_NAME"] = "HH_AUTH"
quart_server.config["QUART_AUTH_SALT"] = Config.quart_auth_csalt
quart_server.config["QUART_AUTH_COOKIE_SECURE"] = False
quart_server.config["QUART_AUTH_DURATION"] = time_in_seconds.year
quart_server.config["TEMPLATES_AUTO_RELOAD"] = True
quart_server.config['SESSION_TYPE'] = 'redis'
quart_server.config['SESSION_PROTECTION'] = True
quart_server.config['SESSION_REVERSE_PROXY'] = True
# Generate New Secret key via:
#     import secrets
#     secrets.token_urlsafe(16)
quart_server.secret_key = Config.quart_secret_key
# JSON extension
quart_server.json_encoder = JSONEncoder
quart_server.json_decoder = JSONDecoder
# Blueprints
quart_server.register_blueprint(routes_main)
# Quart Loaders
QAuthManager = AuthManager()
# QAuthManager.user_class = QA_User
QAuthManager.init_app(quart_server)


@quart_server.before_serving
async def startup():
    set_bash_title(Config.app_name)
    loop = asyncio.get_event_loop()
    loop.create_task(App.Main.Initialise())
