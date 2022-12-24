from rogerthat.route_handlers.handlers.main import route_handlers_main

from rogerthat.route_handlers.handlers.tradingview import route_handlers_tradingview


class route_handlers_ctrl(route_handlers_main,
                          route_handlers_tradingview):
    pass


route_handlers = route_handlers_ctrl()
