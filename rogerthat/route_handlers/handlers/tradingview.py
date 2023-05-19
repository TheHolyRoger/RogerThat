from quart import abort, jsonify

from rogerthat.models.web_request import web_request
from rogerthat.queues.request_processing_queue import request_processing_queue


class route_handlers_tradingview:
    def __init__(self):
        pass

    async def route_handler_tradingview_webhook(self, quart_request):
        request = web_request(from_quart=quart_request)
        await request.build_request_args()
        valid_request = await request.check_is_valid(for_tv_api=True)
        if valid_request:
            request_processing_queue.get_instance().add_request(request.json_data)
            return jsonify({"success": True})
        return abort(401)
