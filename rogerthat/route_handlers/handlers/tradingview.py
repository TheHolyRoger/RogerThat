from quart import (
    abort,
    jsonify,
)
from rogerthat.models.web_request import web_request
from rogerthat.db.models.tradingview_event import tradingview_event
from rogerthat.utils.asyncio_tasks import safe_ensure_future


class route_handlers_tradingview:
    def __init__(self):
        pass

    async def route_handler_tradingview_webhook(self, quart_request):
        request = web_request(from_quart=quart_request)
        await request.build_request_args()
        valid_request = await request.check_is_valid()
        if valid_request:
            tv_event = tradingview_event(from_json=request.json_data)
            safe_ensure_future(tv_event.process_event())
            return jsonify({"success": True})
        print(f"Accepted req: {valid_request}")
        return abort(401)
