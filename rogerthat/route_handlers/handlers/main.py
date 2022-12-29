from quart import jsonify


class route_handlers_main:
    def __init__(self):
        pass

    async def route_handler_main(self, quart_request):
        return jsonify("Roger That.")
