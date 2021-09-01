from quart import (
    abort
)
from rogerthat.models.wss_request import wss_request
# from rogerthat.utils.asyncio_tasks import safe_ensure_future


class wss_handlers_hummingbot:
    def __init__(self):
        pass

    async def wss_handler_hummingbot(self, ws_request, ws_queue):
        print("wss connection")
        request = wss_request(from_quart=ws_request, ws_queue=ws_queue)
        valid_request = request.check_auth()
        print(f"Accepted req: {valid_request}")
        if valid_request:
            await request.process_wss()
        return abort(401)
