from quart import Blueprint, make_response, request

from rogerthat.config.config import Config
from rogerthat.route_handlers.route_handlers_ctrl import route_handlers

# from rogerthat.queues.ws_queue import ws_queue


routes_main = Blueprint('routes_main', __name__)


@routes_main.route("/", methods=['GET'])
async def main_route():
    handler_data = await route_handlers.get_instance().route_handler_main(request)
    return await make_response(handler_data, 200)


@routes_main.route(f"/{Config.get_inst().web_root}/tv_webhook/", methods=['POST', 'GET'])
async def api_route_tv_webhook():
    handler_data = await route_handlers.get_instance().route_handler_tradingview_webhook(request)
    response = await make_response(handler_data, 200)
    # response.timeout = Config.get_inst().api_response_timeout
    return response
