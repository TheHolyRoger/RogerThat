from quart import (
    Blueprint,
    make_response,
    request,
)
from rogerthat.config.config import Config
from rogerthat.route_handlers.route_handlers_ctrl import route_handlers
# from rogerthat.queues.ws_queue import ws_queue


routes_main = Blueprint('routes_main', __name__)


@routes_main.route("/", methods=['GET'])
async def main_route():
    return await make_response((await route_handlers.route_handler_main(request)), 200)


@routes_main.route(f"/{Config.web_root}/tv_webhook/", methods=['POST', 'GET'])
async def api_route_tv_webhook():
    response = await make_response((await route_handlers.route_handler_tradingview_webhook(request)), 200)
    # response.timeout = Config.api_response_timeout
    return response
