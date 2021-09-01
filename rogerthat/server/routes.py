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


@routes_main.route(f"/{Config.web_root}/tv_webhook/", methods=['POST', 'GET'])
async def api_route_tv_webhook():
    OneResp = await make_response((await route_handlers.route_handler_tradingview_webhook(request)), 200)
    # OneResp.timeout = Config.api_response_timeout
    return OneResp


# @routes_main.before_app_websocket
# def before():
#     print("before")


@routes_main.websocket(f"/{Config.wss_root}")
@ws_queue.collect_websocket
async def api_wss_hbot(queue):
    # websocket.headers
    print("wss")
    return await route_handlers.wss_handler_hummingbot(websocket, queue)
