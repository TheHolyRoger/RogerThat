import asyncio
import signal
from rogerthat.config.config import Config
from rogerthat.server.server import quart_server
from rogerthat.utils.logger import logger
from rogerthat.utils.splash import splash_msg
from rogerthat.app.delegate import App
from rogerthat.db.database_init import database_init


class RogerThat:
    def __init__(self):
        logger.set_file("main")
        logger.cycle()
        App.update_instance(self)
        self.shutdown_event = asyncio.Event()

    async def Initialise(self):
        await logger.log("Initialising database.")
        await database_init.initialise()
        await logger.log("Finished initialising database.")
        await logger.log(splash_msg)

    def start_server(self):
        def _signal_handler(*_):  # noqa: N803
            logger.logb("Shutdown signal handler called.")
            self.shutdown_event.set()

        loop = asyncio.get_event_loop()
        try:
            loop.add_signal_handler(signal.SIGTERM, _signal_handler)
        except NotImplementedError:
            signal.signal(signal.SIGTERM, _signal_handler)

        logger.logb("Started RogerThat Server")
        if Config.debug_mode:
            quart_server.run(host="0.0.0.0", port=Config.quart_server_port, debug=Config.debug_mode)
        else:
            serv_task = quart_server.run_task(host="0.0.0.0",
                                              port=Config.quart_server_port,
                                              use_reloader=False,
                                              shutdown_trigger=self.shutdown_event.wait)
            loop.run_until_complete(serv_task)
            logger.logb("Stopped RogerThat Server")
