from rogerthat.route_handlers.handlers.main import route_handlers_main
from rogerthat.route_handlers.handlers.tradingview import route_handlers_tradingview


class route_handlers(route_handlers_main,
                     route_handlers_tradingview):
    _shared_instance: "route_handlers" = None

    @classmethod
    def get_instance(cls) -> "route_handlers":
        if cls._shared_instance is None:
            cls._shared_instance = cls()
        return cls._shared_instance
