import time

from pydantic import create_model
from sqlalchemy import BigInteger, Boolean, Column, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.future import select

from rogerthat.config.config import Config
from rogerthat.db.engine import db_engine
from rogerthat.db.models.base import base_model, db_model_base
from rogerthat.logging.configure import AsyncioLogger
from rogerthat.mqtt.messages import TradingviewMessage
from rogerthat.queues.mqtt_queue import mqtt_queue
from rogerthat.utils.parsing_numbers import bool_or_none, decimal_or_none, int_or_none

logger = AsyncioLogger.get_logger_main(__name__)


EVENT_KEYS = [
    "topic",
    "timestamp_received",
    "timestamp_event",
    "sequence",
    "event_type",
    "params",
    "data",
    "msg",
    "exchange",
    "asset",
    "amount",
    "log_level",
    "restore",
    "script",
    "is_quickstart",
    "skip_order_cancellation",
    "strategy",
    "days",
    "verbose",
    "precision",
]


class filtered_event_keys:
    _filtered = None
    _key_translations = {
        "timestamp_event": "timestamp",
        "event_type": "type",
    }

    @classmethod
    def translate(cls, evt_key):
        return cls._key_translations.get(evt_key, evt_key)

    @classmethod
    def list(cls):
        if cls._filtered is None:
            if Config.get_inst().tradingview_include_extra_fields:
                cls._filtered = list(dict.fromkeys((EVENT_KEYS + Config.get_inst().tradingview_include_extra_fields)))
            else:
                cls._filtered = list(EVENT_KEYS)
            if Config.get_inst().tradingview_exclude_fields:
                for excl_key in Config.get_inst().tradingview_exclude_fields:
                    if excl_key != "topic" and excl_key in cls._filtered:
                        cls._filtered.remove(excl_key)
        return cls._filtered


class tradingview_event(db_model_base,
                        base_model):
    __name__ = 'tradingview_event'
    __tablename__ = 'tradingview_events'
    id = Column(BigInteger, primary_key=True, index=True, unique=True, autoincrement=True)
    topic = Column(String(220), index=True)
    timestamp_received = Column(BigInteger, index=True)
    timestamp_event = Column(BigInteger, index=True)
    sequence = Column(BigInteger, index=True)
    event_type = Column(String(90), index=True)
    params = Column(MutableDict.as_mutable(JSONB))
    data = Column(MutableDict.as_mutable(JSONB))
    msg = Column(String(500))
    exchange = Column(String(90), index=True)
    asset = Column(String(30), index=True)
    amount = Column(Numeric, index=True)
    log_level = Column(String(30))
    restore = Column(Boolean)
    script = Column(String(90))
    is_quickstart = Column(Boolean)
    skip_order_cancellation = Column(Boolean)
    strategy = Column(String(90), index=True)
    days = Column(Numeric)
    verbose = Column(Boolean)
    precision = Column(Integer)

    def __init__(self,
                 from_json=None,
                 topic=None,
                 timestamp=None,
                 sequence=None,
                 event_type=None,
                 params=None,
                 data=None,
                 msg=None,
                 exchange=None,
                 asset=None,
                 amount=None,
                 log_level=None,
                 restore=None,
                 script=None,
                 is_quickstart=None,
                 skip_order_cancellation=None,
                 strategy=None,
                 days=None,
                 verbose=None,
                 precision=None,
                 ):
        self.topic = topic
        self.timestamp_received = int(time.time() * 1000)
        self.timestamp_event = timestamp
        self.sequence = sequence
        self.event_type = event_type
        self.params = params
        self.data = data
        self.msg = msg
        self.exchange = exchange
        self.asset = asset
        self.amount = amount
        self.log_level = log_level
        self.restore = restore
        self.script = script
        self.is_quickstart = is_quickstart
        self.skip_order_cancellation = skip_order_cancellation
        self.strategy = strategy
        self.days = days
        self.verbose = verbose
        self.precision = precision
        if Config.get_inst().tradingview_include_extra_fields:
            for evt_key in Config.get_inst().tradingview_include_extra_fields:
                setattr(self, evt_key, None)
        if from_json:
            self.topic = from_json.get("topic")
            self.timestamp_event = int_or_none(from_json.get("timestamp"))
            self.sequence = int_or_none(from_json.get("sequence"))
            self.event_type = from_json.get("type")
            self.params = from_json.get("params")
            self.data = from_json.get("data")
            self.msg = from_json.get("msg")
            self.exchange = from_json.get("exchange")
            self.asset = from_json.get("asset")
            self.amount = decimal_or_none(from_json.get("amount"))
            self.log_level = from_json.get("log_level")
            self.restore = bool_or_none(from_json.get("restore"))
            self.script = from_json.get("script")
            self.is_quickstart = bool_or_none(from_json.get("is_quickstart"))
            self.skip_order_cancellation = bool_or_none(from_json.get("skip_order_cancellation"))
            self.strategy = from_json.get("strategy")
            self.days = decimal_or_none(from_json.get("days"))
            self.verbose = bool_or_none(from_json.get("verbose"))
            self.precision = int_or_none(from_json.get("precision"))
            if Config.get_inst().tradingview_include_extra_fields:
                for evt_key in Config.get_inst().tradingview_include_extra_fields:
                    setattr(self, evt_key, from_json.get(evt_key))

    async def process_event(self):
        logger.debug(f"Processing event from TradingView: {self.to_minimised_dict()}")
        await self.db_save()
        mqtt_queue.get_instance().broadcast(self)

    @property
    def to_pydantic(self):
        pydantic_model = create_model("TradingviewMessage",
                                      **self.to_minimised_dict(mqtt=True),
                                      __base__=TradingviewMessage)
        return pydantic_model()

    def to_minimised_dict(self, mqtt=False):
        minimised_dict = {}
        for i, key in enumerate(filtered_event_keys.list()):
            if i == 0 and mqtt:
                continue
            val = getattr(self, key)
            if val is not None:
                minimised_dict[filtered_event_keys.translate(key)] = val

        return minimised_dict

    @classmethod
    async def fetch_latest(cls,
                           topic=None):
        result = None
        async with AsyncSession(db_engine.db().engine,
                                expire_on_commit=False) as session:
            async with session.begin():
                stmt = (select(cls)
                        .limit(1)
                        .order_by(cls.timestamp_received.desc()))
                if topic:
                    stmt = stmt.where(cls.topic == topic)
                result = (await session.execute(stmt)).fetchone()
                if result:
                    result = result[0]
        return result
