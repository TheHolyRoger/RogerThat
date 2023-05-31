import asyncio
import signal
import time

from rogerthat.app.delegate import App
from rogerthat.config.config import Config
from rogerthat.db.database_init import database_init
from rogerthat.logging.configure import AsyncioLogger
from rogerthat.queues.mqtt_queue import mqtt_queue
from rogerthat.queues.request_processing_queue import request_processing_queue
from rogerthat.server.server import quart_server
from rogerthat.utils.asyncio_tasks import safe_ensure_future, safe_gather
from rogerthat.utils.splash import splash_msg

logger = AsyncioLogger.get_logger_main(__name__)


class RogerThat:
    def __init__(self):
        App.update_instance(self)
        self.shutdown_event = asyncio.Event()
        self._request_queue = None
        self._mqtt_queue = None
        self._ev_loop = None
        self._serv_task = None

    @property
    def loop(self):
        return self._ev_loop

    def call_soon_threadsafe(self, *args, **kwargs):
        return self._ev_loop.call_soon_threadsafe(*args, **kwargs)

    async def async_run_in_executor(self, *args, **kwargs):
        return await self._ev_loop.run_in_executor(*args, **kwargs)

    async def Initialise(self):
        logger.debug("Initialising database.")
        db_started = await database_init.initialise()
        if not db_started:
            await asyncio.sleep(0.1)
            self.shutdown()
            return
        logger.debug("Finished initialising database.")
        logger.info(splash_msg)

    def _signal_handler(self, *_):  # noqa: N803
        logger.info("Shutdown signal handler called.")
        self.shutdown()

    def setup_loop(self):
        self._ev_loop = asyncio.get_event_loop()
        signals = [
            signal.SIGINT,
            signal.SIGTERM,
            signal.SIGQUIT,
        ]
        try:
            for sig in signals:
                self._ev_loop.add_signal_handler(sig, self._signal_handler)
        except NotImplementedError:
            for sig in signals:
                signal.signl(sig, self._signal_handler)

    def start_quart(self):
        self._ev_loop.run_until_complete(self.start_quart_loop())

    async def start_quart_loop(self):
        self._serv_task = quart_server.run_task(
            host="0.0.0.0",
            port=Config.get_inst().quart_server_port,
            debug=Config.get_inst().debug_mode,
            use_reloader=False if not Config.get_inst().debug_mode else True,
            shutdown_trigger=self.shutdown_event.wait)
        await safe_gather(self._serv_task)

    async def exit_loop(self):
        self._request_queue.stop()
        self._mqtt_queue.stop()
        logger.info("Stopped all queues.")
        await asyncio.sleep(1)

    def shutdown(self):
        logger.info("Stopping RogerThat Server.")
        self.shutdown_event.set()
        safe_ensure_future(self.exit_loop(), loop=self._ev_loop)

    def start_queues(self):
        self._request_queue = request_processing_queue.get_instance()
        logger.debug("Starting Broadcast Queues.")
        self._mqtt_queue = mqtt_queue.get_instance()
        self._mqtt_queue.start()

    def start_server(self):
        logger.info(f"RogerThat v{Config.get_inst().version} starting.")
        self.setup_loop()
        self.start_queues()
        logger.info("Starting RogerThat Server.")
        self.start_quart()

    def run(self):
        self.start_server()
        time.sleep(1)
        logger.info("Stopped RogerThat Server.")
        time.sleep(1)
