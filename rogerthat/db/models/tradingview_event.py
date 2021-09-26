from decimal import Decimal as Dec
import time
import ujson
from sqlalchemy import (
    Column,
    BigInteger,
    Numeric,
    String,
)
from rogerthat.config.config import Config
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from rogerthat.db.engine import db
from rogerthat.db.models.base import (
    base_model,
    db_model_base,
)
from rogerthat.queues.ws_queue import ws_queue
from rogerthat.utils.logger import logger


class tradingview_event(db_model_base,
                        base_model):
    __tablename__ = 'tradingview_events'
    id = Column(BigInteger, primary_key=True, index=True, unique=True, autoincrement=True)
    timestamp_received = Column(BigInteger, index=True)
    timestamp_event = Column(BigInteger, index=True)
    event_descriptor = Column(String(100), index=True)
    command = Column(String(100), index=True)
    exchange = Column(String(90), index=True)
    symbol = Column(String(30), index=True)
    interval = Column(BigInteger, index=True)
    price = Column(Numeric, index=True)
    volume = Column(Numeric, index=True)
    inventory = Column(Numeric, index=True)

    def __init__(self,
                 from_json=None,
                 timestamp=None,
                 event_descriptor=None,
                 command=None,
                 exchange=None,
                 symbol=None,
                 interval=None,
                 price=Dec("0"),
                 volume=Dec("0"),
                 inventory=Dec("0"),
                 ):
        self.timestamp_received = int(time.time() * 1000)
        self.timestamp_event = timestamp
        self.event_descriptor = event_descriptor
        self.command = command
        self.exchange = exchange
        self.symbol = symbol
        self.interval = interval
        self.price = price
        self.volume = volume
        self.inventory = inventory
        if from_json:
            timestamp_event = from_json.get("timestamp")
            interval = from_json.get("interval")
            price = from_json.get("price")
            volume = from_json.get("volume")
            inventory = from_json.get("inventory")
            self.timestamp_event = int(timestamp_event) if timestamp_event else None
            self.command = from_json.get("command")
            self.exchange = from_json.get("exchange")
            self.symbol = from_json.get("symbol")
            self.interval = int(interval) if interval else None
            self.price = Dec(str(price)) if price else Dec("0")
            self.volume = Dec(str(price)) if volume else Dec("0")
            self.inventory = Dec(str(price)) if inventory else Dec("0")
            self.event_descriptor = from_json.get("event_descriptor")
            self._get_data_fields(from_json)

    def _get_data_fields(self, from_json):
        if not self.event_descriptor:
            for field in Config.tradingview_descriptor_fields:
                if field in from_json:
                    self.event_descriptor = from_json.get(field)
                    break

    async def process_event(self):
        await logger.log(f"Received event from TradingView: {self.to_dict}")
        await self.db_save()
        await ws_queue.broadcast(self.to_json)

    async def process_event_ws(self):
        await logger.log(f"Received event via websocket: {self.to_dict}")
        await self.db_save()
        await ws_queue.broadcast(self.to_json)

    @property
    def to_dict(self):
        return {
            "timestamp_received": self.timestamp_received,
            "timestamp_event": self.timestamp_event,
            "event_descriptor": self.event_descriptor,
            "command": self.command,
            "exchange": self.exchange,
            "symbol": self.symbol,
            "interval": self.interval,
            "price": self.price,
            "volume": self.volume,
            "inventory": self.inventory,
        }

    @property
    def to_json(self):
        return ujson.dumps(self.to_dict)

    @classmethod
    def from_json(cls,
                  data,
                  raw=False):
        json_data = ujson.loads(data) if raw else data
        new_event = cls(from_json=json_data)
        if new_event.event_descriptor:
            return new_event
        return None

    @classmethod
    async def fetch_latest(cls,):
        result = None
        async with AsyncSession(db.engine,
                                expire_on_commit=False) as session:
            async with session.begin():
                stmt = (select(cls)
                        .limit(1)
                        .order_by(cls.timestamp_received.desc()))
                result = (await session.execute(stmt)).fetchone()
                if result:
                    result = result[0]
        return result
