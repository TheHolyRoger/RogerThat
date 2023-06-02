import asyncio
import traceback
from socket import gaierror
from ssl import SSLCertVerificationError, SSLEOFError

from rogerthat.config.config import Config
from rogerthat.logging.configure import AsyncioLogger
from rogerthat.mqtt.mqtt import MQTTGateway
from rogerthat.utils.asyncio_tasks import safe_ensure_future

logger = AsyncioLogger.get_logger_main(__name__)


class mqtt_queue:
    _shared_instance: "mqtt_queue" = None

    @classmethod
    def get_instance(cls) -> "mqtt_queue":
        if cls._shared_instance is None:
            cls._shared_instance = cls()
        return cls._shared_instance

    def __init__(self):
        self._mqtt_queue_task = None
        self._mqtt_queue = None
        self._mqtt: MQTTGateway = None
        self._failure_msg = "Failed to connect to MQTT Broker!"
        self._is_ready = False

    def _create_queue(self):
        self._mqtt_queue = asyncio.Queue()

    def start(self):
        if not Config.get_inst().mqtt_enable:
            return

        try:
            self._mqtt = MQTTGateway()
            self._mqtt.start()
            self._start_queue_tasks()
        except (ConnectionRefusedError, gaierror, OSError) as e:
            if self._mqtt is not None:
                extra_debug = f" Parameters: {self._mqtt._params}"
            else:
                extra_debug = ""
            logger.error(f"{self._failure_msg} Check host and port! - {e}.{extra_debug}")
        except SSLEOFError:
            logger.error(f"{self._failure_msg} Using plain HTTP port with SSL enabled!")
        except SSLCertVerificationError:
            logger.error(f"{self._failure_msg} You need to set up your SSL certificates correctly!")
        except Exception as e:
            logger.error(e)
            raise e
        if self._is_ready:
            logger.debug("MQTT Queue is ready.")

    def _start_queue_tasks(self):
        if self._mqtt:
            self._create_queue()
            self._mqtt_queue_task = safe_ensure_future(
                self._listen_for_broadcasts()
            )
            self._is_ready = True
            safe_ensure_future(self._mqtt.async_set_ready())

    def stop(self):
        if self._mqtt_queue_task is not None:
            self._mqtt_queue_task.cancel()
            self._mqtt_queue_task = None
        logger.debug("MQTT Queue stopped.")
        if self._mqtt:
            self._mqtt.stop()

    async def _listen_for_broadcasts(self):
        if not self._mqtt:
            raise Exception("listen_for_broadcasts called but mqtt is not enabled!")
        while True:
            if not self._mqtt.health:
                if not self._mqtt_queue.empty():
                    logger.warning("MQTT not ready for broadcast, sleeping 5s before retry.")

                await asyncio.sleep(5)
                continue

            msg = None

            try:
                msg = await self._mqtt_queue.get()
                publisher = self._mqtt.get_publisher_for(msg.topic)
                publisher.broadcast(msg.to_pydantic)
            except asyncio.CancelledError:
                raise
            except Exception as e:
                tb = "".join(traceback.TracebackException.from_exception(e).format())
                logger.error(f"Error in mqtt_queue: {e}\n{tb}")

                if msg and self._mqtt_queue:
                    self._mqtt_queue.put_nowait(msg)

    def broadcast(self, event):
        if not self._mqtt_queue:
            logger.error("Cannot broadcast, MQTT Queue not started!")
            return

        logger.debug("Adding event to MQTT queue.")
        self._mqtt_queue.put_nowait(event)
