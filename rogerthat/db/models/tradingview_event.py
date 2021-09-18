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
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from rogerthat.db.engine import db
from rogerthat.db.models.base import (
    base_model,
    db_model_base,
)
from rogerthat.queues.ws_queue import ws_queue


class tradingview_event(db_model_base,
                        base_model):
    __tablename__ = 'tradingview_events'
    id = Column(BigInteger, primary_key=True, index=True, unique=True, autoincrement=True)
    timestamp_recieved = Column(BigInteger, index=True)
    timestamp_event = Column(BigInteger, index=True)
    event_descriptor = Column(String(200), index=True)
    command = Column(String(200), index=True)
    exchange = Column(String(200), index=True)
    price = Column(Numeric, index=True)
    volume = Column(Numeric, index=True)

    def __init__(self,
                 from_json=None,
                 timestamp=None,
                 event_descriptor=None,
                 command=None,
                 exchange=None,
                 symbol=None,
                 price=Dec("0"),
                 volume=Dec("0"),
                 inventory=Dec("0"),
                 ):
        self.timestamp_recieved = int(time.time())
        self.timestamp_event = timestamp
        self.event_descriptor = event_descriptor
        self.command = command
        self.exchange = exchange
        self.symbol = symbol
        self.price = price
        self.volume = volume
        self.inventory = inventory
        if from_json:
            self.timestamp_event = from_json.get("timestamp")
            self.command = from_json.get("command")
            self.exchange = from_json.get("exchange")
            self.symbol = from_json.get("symbol")
            self.price = Dec(str(from_json.get("price", Dec("0"))))
            self.volume = Dec(str(from_json.get("volume", Dec("0"))))
            self.inventory = Dec(str(from_json.get("inventory", Dec("0"))))
            self._get_data_fields(from_json)

    def _get_data_fields(self, from_json):
        for field in Config.tradingview_descriptor_fields:
            if field in from_json:
                self.event_descriptor = from_json.get(field)
                break

    async def process_event(self):
        await self.db_save()
        await ws_queue.broadcast(self.to_json)

    @property
    def to_dict(self):
        return {
            "timestamp_recieved": self.timestamp_recieved,
            "timestamp_event": self.timestamp_event,
            "event_descriptor": self.event_descriptor,
            "command": self.command,
            "exchange": self.exchange,
            "symbol": self.symbol,
            "price": self.price,
            "volume": self.volume,
            "inventory": self.inventory,
        }

    @property
    def to_json(self):
        return ujson.dumps(self.to_dict)
