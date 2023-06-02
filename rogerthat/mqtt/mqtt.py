#!/usr/bin/env python

import asyncio
import threading
from typing import TYPE_CHECKING

from commlib.node import Node
from commlib.transports.mqtt import ConnectionParameters as MQTTConnectionParameters

from rogerthat.app.delegate import App
from rogerthat.config.config import Config
from rogerthat.logging.configure import AsyncioLogger
from rogerthat.mqtt.messages import TradingviewMessage

if TYPE_CHECKING:
    from rogerthat.db.models.tradingview_event import tradingview_event


logger = AsyncioLogger.get_logger_main(__name__)


class MQTTPublisher:

    def __init__(self,
                 topic: str,
                 mqtt_node: Node):
        self._initial_connection_completed = False

        self._node = mqtt_node

        self._topic = topic

        self.publisher = self._node.create_publisher(
            topic=self._topic, msg_type=TradingviewMessage
        )
        self.publisher.run()

    @property
    def is_ready(self):
        return self._initial_connection_completed

    @property
    def is_connected(self):
        is_connected = self.publisher._transport.is_connected

        if not self._initial_connection_completed and is_connected:
            self._initial_connection_completed = True

        return is_connected

    def broadcast(self, event: "tradingview_event"):
        logger.debug(f"Broadcasting MQTT event on {self._topic}: {event}")
        self.publisher.publish(event)

    def __del__(self):
        self.publisher.stop()


class MQTTGateway(Node):
    NODE_NAME = "$APP.$UID"
    HEARTBEAT_URI = "$APP/$UID/hb"

    def __init__(self,
                 *args, **kwargs):
        self._initial_connection_completed = False
        self._health = False
        self._gateway_ready = asyncio.Event()
        self._stop_event_async = asyncio.Event()
        self._restart_heartbeat_event_async = asyncio.Event()

        self.mqtt_publisher = None

        self.HEARTBEAT_URI = f"{Config.get_inst().app_name}/{Config.get_inst().mqtt_instance_name}/hb"

        self.NODE_NAME = f"{Config.get_inst().app_name}.{Config.get_inst().mqtt_instance_name}"

        self._params = self._create_mqtt_params_from_conf()

        self._topic_publishers = {}

        super().__init__(
            node_name=self.NODE_NAME,
            connection_params=self._params,
            heartbeat_uri=self.HEARTBEAT_URI,
            debug=True,
            *args,
            **kwargs
        )

    @property
    def health(self):
        return self._health

    async def async_set_ready(self):
        await asyncio.sleep(5)
        self._gateway_ready.set()

    def get_publisher_for(self, topic: str):
        if topic not in self._topic_publishers:
            logger.debug(f"Starting MQTT Publisher for {topic}")
            self._topic_publishers[topic] = MQTTPublisher(topic=topic, mqtt_node=self)
        return self._topic_publishers[topic]

    def _create_mqtt_params_from_conf(self):
        return MQTTConnectionParameters(
            host=Config.get_inst().mqtt_host,
            port=int(Config.get_inst().mqtt_port),
            username=Config.get_inst().mqtt_username,
            password=Config.get_inst().mqtt_password,
            ssl=Config.get_inst().mqtt_ssl
        )

    def _start_health_monitoring_loop(self):
        if threading.current_thread() != threading.main_thread():  # pragma: no cover
            App.get_instance().call_soon_threadsafe(self._start_health_monitoring_loop)
            return
        self._stop_event_async.clear()
        App.get_instance().ensure_future(self._monitor_health_loop())

    async def _restart_heartbeat(self):
        await asyncio.sleep(3)

        if not self._hb_thread._heartbeat_pub._transport.is_connected:
            logger.warning("Restarting heartbeat thread.")
            self._hb_thread.stop()
            await asyncio.sleep(3)

            try:
                self._init_heartbeat_thread()
                await asyncio.sleep(5)
                logger.warning("Heartbeat thread restarted.")

            except Exception:
                await asyncio.sleep(5)

        self._restart_heartbeat_event_async.clear()

    def _check_connections(self) -> bool:
        connected = True

        # Check heartbeat
        if (
            not self._hb_thread or
            self._hb_thread.stopped() or
            not self._hb_thread._heartbeat_pub._transport.is_connected
        ):
            if (
                self._initial_connection_completed and
                not self._restart_heartbeat_event_async.is_set() and
                self._hb_thread and (
                    self._hb_thread.stopped() or
                    not self._hb_thread._heartbeat_pub._transport.is_connected
                )
            ):
                self._restart_heartbeat_event_async.set()
                App.get_instance().ensure_future(self._restart_heartbeat())

            connected = False

        # Check Publishers
        topic_keys = list(self._topic_publishers.keys())

        for topic in topic_keys:

            p = self._topic_publishers[topic]

            if not p.is_connected:
                if p.is_ready and self._initial_connection_completed:
                    logger.debug(f"Restarting publisher thread on {topic}.")
                    del self._topic_publishers[topic]

                connected = False

        return connected

    async def _monitor_health_loop(self, period: float = 3.0):
        await self._gateway_ready.wait()
        logger.debug("Started MQTT health monitoring.")
        while not self._stop_event_async.is_set():
            self._health = await App.get_instance().async_run_in_executor(
                None, self._check_connections)

            if self._health:
                if not self._initial_connection_completed:
                    self._initial_connection_completed = True

                await asyncio.sleep(period)
            else:
                if self._initial_connection_completed:
                    logger.warning("MQTT Health check failed. Services should be restarting.")

                await asyncio.sleep(10.0)

    def _stop_health_monitoring_loop(self):
        self._stop_event_async.set()

    def start(self) -> None:
        self.run()
        self._start_health_monitoring_loop()

    def stop(self):
        self._stop_health_monitoring_loop()
        super().stop()

    def __del__(self):
        self.stop()
