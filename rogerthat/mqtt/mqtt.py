#!/usr/bin/env python

from typing import TYPE_CHECKING

from commlib.node import Node
from commlib.transports.mqtt import ConnectionParameters as MQTTConnectionParameters

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

        self._node = mqtt_node

        self._topic = topic

        self.publisher = self._node.create_publisher(
            topic=self._topic, msg_type=TradingviewMessage
        )

    def broadcast(self, event: "tradingview_event"):
        logger.debug(f"Broadcasting MQTT event on {self._topic}: {event}")
        self.publisher.publish(event)


class MQTTGateway(Node):
    NODE_NAME = "$APP.$UID"
    HEARTBEAT_URI = "$APP/$UID/hb"

    def __init__(self,
                 *args, **kwargs):
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

    def get_publisher_for(self, topic: str):
        if topic not in self._topic_publishers:
            logger.info(f"Starting MQTT Publisher for {topic}")
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
