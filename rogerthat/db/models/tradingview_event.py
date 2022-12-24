from decimal import Decimal as Dec
import time
from commlib.msg import PubSubMessage
from sqlalchemy import (
    Column,
    BigInteger,
    Numeric,
    String,
)
from typing import Optional
from rogerthat.config.config import Config
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from rogerthat.db.engine import db
from rogerthat.db.models.base import (
    base_model,
    db_model_base,
)
from rogerthat.queues.mqtt_queue import mqtt_queue
# from rogerthat.queues.ws_queue import ws_queue
from rogerthat.utils.parsing_numbers import (
    decimal_or_none,
    decimal_or_zero,
    int_or_none,
)
from rogerthat.logging.configure import AsyncioLogger


logger = AsyncioLogger.get_logger_main(__name__)


class pydantic_tradingview_event_base(PubSubMessage):
    id: int
    timestamp_received: int
    timestamp_event: Optional[int] = None
    topic: str
    command: Optional[str] = None
    exchange: Optional[str] = None
    symbol: Optional[str] = None
    interval: Optional[int] = None
    price: Optional[Dec] = None
    volume: Optional[Dec] = None
    inventory: Optional[Dec] = None

    class Config:
        orm_mode = True


class pydantic_tradingview_event_with_order(pydantic_tradingview_event_base):
    order_bid_spread: Optional[Dec] = None
    order_ask_spread: Optional[Dec] = None
    order_amount: Optional[Dec] = None
    order_levels: Optional[Dec] = None
    order_level_spread: Optional[Dec] = None


class tradingview_event(db_model_base,
                        base_model):
    __name__ = 'tradingview_event'
    __tablename__ = 'tradingview_events'
    id = Column(BigInteger, primary_key=True, index=True, unique=True, autoincrement=True)
    timestamp_received = Column(BigInteger, index=True)
    timestamp_event = Column(BigInteger, index=True)
    topic = Column(String(220), index=True)
    command = Column(String(100), index=True)
    exchange = Column(String(90), index=True)
    symbol = Column(String(30), index=True)
    interval = Column(BigInteger, index=True)
    price = Column(Numeric, index=True)
    volume = Column(Numeric, index=True)
    inventory = Column(Numeric, index=True)
    order_bid_spread = Column(Numeric, index=True)
    order_ask_spread = Column(Numeric, index=True)
    order_amount = Column(Numeric, index=True)
    order_levels = Column(Numeric, index=True)
    order_level_spread = Column(Numeric, index=True)

    def __init__(self,
                 from_json=None,
                 timestamp=None,
                 topic=None,
                 command=None,
                 exchange=None,
                 symbol=None,
                 interval=None,
                 price=Dec("0"),
                 volume=Dec("0"),
                 inventory=Dec("0"),
                 order_bid_spread=None,
                 order_ask_spread=None,
                 order_amount=None,
                 order_levels=None,
                 order_level_spread=None,
                 ):
        self.timestamp_received = int(time.time() * 1000)
        self.timestamp_event = timestamp
        self.topic = topic
        self.command = command
        self.exchange = exchange
        self.symbol = symbol
        self.interval = interval
        self.price = price
        self.volume = volume
        self.inventory = inventory
        self.order_bid_spread = order_bid_spread
        self.order_ask_spread = order_ask_spread
        self.order_amount = order_amount
        self.order_levels = order_levels
        self.order_level_spread = order_level_spread
        if from_json:
            self.timestamp_event = int_or_none(from_json.get("timestamp"))
            self.command = from_json.get("command")
            self.exchange = from_json.get("exchange")
            self.symbol = from_json.get("symbol")
            self.interval = int_or_none(from_json.get("interval"))
            self.price = decimal_or_zero(from_json.get("price"))
            self.volume = decimal_or_zero(from_json.get("volume"))
            self.inventory = decimal_or_zero(from_json.get("inventory"))
            self.order_bid_spread = decimal_or_none(from_json.get("order_bid_spread"))
            self.order_ask_spread = decimal_or_none(from_json.get("order_ask_spread"))
            self.order_amount = decimal_or_none(from_json.get("order_amount"))
            self.order_levels = decimal_or_none(from_json.get("order_levels"))
            self.order_level_spread = decimal_or_none(from_json.get("order_level_spread"))
            self.topic = from_json.get("topic")

    async def process_event(self):
        logger.info(f"Received event from TradingView: {self.to_dict}")
        await self.db_save()
        mqtt_queue.broadcast(self)

    @property
    def to_pydantic(self):
        if Config.include_extra_order_fields:
            return pydantic_tradingview_event_with_order.from_orm(self)
        return pydantic_tradingview_event_base.from_orm(self)

    @property
    def to_dict(self):
        the_dict = {
            "timestamp_received": self.timestamp_received,
            "timestamp_event": self.timestamp_event,
            "topic": self.topic,
            "command": self.command,
            "exchange": self.exchange,
            "symbol": self.symbol,
            "interval": self.interval,
            "price": self.price,
            "volume": self.volume,
            "inventory": self.inventory,
        }
        if Config.include_extra_order_fields:
            the_dict["order_bid_spread"] = self.order_bid_spread
            the_dict["order_ask_spread"] = self.order_ask_spread
            the_dict["order_amount"] = self.order_amount
            the_dict["order_levels"] = self.order_levels
            the_dict["order_level_spread"] = self.order_level_spread
        return the_dict

    @classmethod
    async def fetch_latest(cls,
                           topic=None):
        result = None
        async with AsyncSession(db.engine,
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
