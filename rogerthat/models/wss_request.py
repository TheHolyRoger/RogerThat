import asyncio
# from rogerthat.config.config import Config
from rogerthat.utils.logger import logger


class wss_request:
    def __init__(self,
                 from_quart=None,
                 ws_queue=None):
        self._quart_request = None
        self._auth = None
        self._ws_queue = ws_queue
        if from_quart:
            self._quart_request = from_quart
            self._auth = self._quart_request.authorization

    def check_auth(self):
        return True

    async def sending(self):
        while True:
            await self._quart_request.send(await self._ws_queue.get())

    async def receiving(self):
        while True:
            data = await self._quart_request.receive()
            await logger.log(f"Websocket data received: {data}")
            # await asyncio.sleep(10)

    async def process_wss(self, tradingview_event=None):
        await logger.log("New websocket client connected.")
        producer = asyncio.create_task(self.sending())
        consumer = asyncio.create_task(self.receiving())
        if tradingview_event:
            await self._ws_queue.put(tradingview_event.to_json)
        return await asyncio.gather(producer, consumer)

    def __repr__(self):
        return f"{vars(self)}"
