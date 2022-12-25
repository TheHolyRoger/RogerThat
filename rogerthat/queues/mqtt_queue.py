import asyncio
from socket import gaierror
from ssl import SSLCertVerificationError, SSLEOFError
from rogerthat.config.config import Config
from rogerthat.logging.configure import AsyncioLogger
from rogerthat.mqtt.mqtt import MQTTGateway
from rogerthat.utils.asyncio_tasks import safe_ensure_future


logger = AsyncioLogger.get_logger_main(__name__)


class mqtt_queue_cls:
    def __init__(self):
        self._mqtt_queue_task = None
        self._mqtt_queue = None
        self._mqtt: MQTTGateway = None
        self._failure_msg = "Failed to connect to MQTT Broker!"

        if Config.mqtt_enable:
            try:
                self._mqtt = MQTTGateway()
                self._mqtt
                self._mqtt.run()
                self.start()
            except (ConnectionRefusedError, gaierror):
                logger.error(f"{self._failure_msg} Check host and port!")
            except SSLEOFError:
                logger.error(f"{self._failure_msg} Using plain HTTP port with SSL enabled!")
            except SSLCertVerificationError:
                logger.error(f"{self._failure_msg} You need to set up your SSL certificates correctly!")
            except Exception as e:
                logger.error(e)
                raise e
            logger.info("MQTT Gateway is ready.")

    def _create_queue(self):
        self._mqtt_queue = asyncio.Queue()

    def start(self):
        if self._mqtt:
            self._create_queue()
            self._mqtt_queue_task = safe_ensure_future(
                self._listen_for_broadcasts()
            )

    async def _listen_for_broadcasts(self):
        if not self._mqtt:
            raise Exception("listen_for_broadcasts called but mqtt is not enabled!")
        while True:
            msg = await self._mqtt_queue.get()
            publisher = self._mqtt.get_publisher_for(msg.topic)
            publisher.broadcast(msg.to_pydantic)

    def broadcast(self, event):
        if not self._mqtt_queue:
            logger.error("Cannot broadcast, MQTT not started!")
        if self._mqtt:
            logger.info("Broadcasting message to mqtt queue.")
            self._mqtt_queue.put_nowait(event)


mqtt_queue = mqtt_queue_cls()
