from rogerthat.route_handlers.handlers.hummingbot import (
    wss_handlers_hummingbot,
    route_handlers_hummingbot,
)
from rogerthat.route_handlers.handlers.tradingview import route_handlers_tradingview


class route_handlers_ctrl(wss_handlers_hummingbot,
                          route_handlers_hummingbot,
                          route_handlers_tradingview):
    pass


route_handlers = route_handlers_ctrl()
