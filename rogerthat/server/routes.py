from quart import (
    Blueprint,
    make_response,
    request,
    websocket,
)
from rogerthat.config.config import Config
from rogerthat.route_handlers.route_handlers_ctrl import route_handlers
from rogerthat.queues.ws_queue import ws_queue


routes_main = Blueprint('routes_main', __name__)


@routes_main.route("/", methods=['GET'])
async def main_route():
    return await make_response((await route_handlers.route_handler_main(request)), 200)


@routes_main.route(f"/{Config.web_root}/tv_webhook/", methods=['POST', 'GET'])
async def api_route_tv_webhook():
    response = await make_response((await route_handlers.route_handler_tradingview_webhook(request)), 200)
    # response.timeout = Config.api_response_timeout
    return response


# @routes_main.before_app_websocket
# def before():
#     print("before")


@routes_main.route(f"/{Config.web_root}/hbot/", methods=['GET'])
async def api_route_hummingbot():
    return await make_response((await route_handlers.route_handler_hummingbot(request)), 200)


@routes_main.websocket(f"/{Config.wss_root}")
@ws_queue.collect_websocket
async def api_wss_hbot(queue):
    return await route_handlers.wss_handler_hummingbot(websocket, queue)


@routes_main.websocket(f"/{Config.wss_root}/<channel>")
@ws_queue.collect_websocket
async def api_wss_hbot_filtered(queue, channel):
    return await route_handlers.wss_handler_hummingbot(websocket, queue, channel)
