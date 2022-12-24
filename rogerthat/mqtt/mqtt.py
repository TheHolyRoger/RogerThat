#!/usr/bin/env python

from typing import TYPE_CHECKING

from commlib.node import Node
from commlib.transports.mqtt import ConnectionParameters as MQTTConnectionParameters
from rogerthat.config.config import Config
from rogerthat.logging.configure import AsyncioLogger
from rogerthat.mqtt.messages import (
    EventMessage,
)

if TYPE_CHECKING:
    from rogerthat.db.models.tradingview_event import tradingview_event


logger = AsyncioLogger.get_logger_main(__name__)


class MQTTPublisher:

    def __init__(self,
                 topic: str,
                 mqtt_node: Node):

        self._node = mqtt_node

        self._topic = topic

        self.publisher = self._node.create_publisher(
            topic=self._topic, msg_type=EventMessage
        )

    def broadcast(self, event: "tradingview_event"):
        self.publisher.publish(event)


class MQTTGateway(Node):
    NODE_NAME = 'rogerthat.$UID'
    HEARTBEAT_URI = 'rogerthat/$UID/hb'

    def __init__(self,
                 *args, **kwargs):
        self.mqtt_publisher = None

        self.HEARTBEAT_URI = self.HEARTBEAT_URI.replace('$UID', Config.mqtt_instance_name)

        self._params = self._create_mqtt_params_from_conf()

        self._topic_publishers = {}

        super().__init__(
            node_name=self.NODE_NAME.replace('$UID', Config.mqtt_instance_name),
            connection_params=self._params,
            heartbeat_uri=self.HEARTBEAT_URI,
            debug=True,
            *args,
            **kwargs
        )

    def get_publisher_for(self, topic: str):
        if topic not in self._topic_publishers:
            logger.info(f"Starting MQTT Publisher for {topic}")
            self._topic_publishers[topic] = MQTTPublisher(topic=topic, mqtt_node=self)
        return self._topic_publishers[topic]

    def _create_mqtt_params_from_conf(self):
        return MQTTConnectionParameters(
            host=Config.mqtt_host,
            port=int(Config.mqtt_port),
            username=Config.mqtt_username,
            password=Config.mqtt_password,
            ssl=Config.mqtt_ssl
        )
