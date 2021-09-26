import asyncio
from rogerthat.config.config import Config
from rogerthat.db.models.tradingview_event import tradingview_event
from rogerthat.utils.logger import logger


class wss_request:
    def __init__(self,
                 from_quart=None,
                 ws_queue=None):
        self._quart_request = None
        self._auth = None
        self._headers = None
        self._user_agent = None
        self._ws_queue = ws_queue
        self._received_events = set()
        if from_quart:
            self._quart_request = from_quart
            self._auth = self._quart_request.authorization
            self._headers = self._quart_request.headers
            self._user_agent = self._quart_request.user_agent.string.lower().strip()

    def _check_api_key(self):
        if self._headers and self._headers.get("HBOT-API-KEY") in Config.api_allowed_keys_hbot:
            return True
        return False

    def _check_user_agent(self):
        if self._user_agent and self._user_agent == "hummingbot":
            return True
        return False

    def check_auth(self):
        if Config.disable_websocket_authentication:
            return True
        return all([
                   self._check_api_key(),
                   self._check_user_agent(),
                   ])

    async def sending(self):
        while True:
            await self._quart_request.send(await self._ws_queue.get())

    async def receiving(self):
        while True:
            data = await self._quart_request.receive()
            try:
                remote_event = tradingview_event.from_json(data, raw=True)
                if remote_event:
                    event_id = f"{remote_event.timestamp_received}{remote_event.timestamp_event}"
                    if event_id in self._received_events:
                        continue
                    await remote_event.process_event_ws()
            except Exception as e:
                await logger.log(f"Websocket data received: {data}")
                await logger.log(f"Websocket receive error: {e}")

    async def process_wss(self, tv_event=None):
        producer = asyncio.create_task(self.sending())
        consumer = asyncio.create_task(self.receiving())
        if tv_event and Config.rebroadcast_on_ws_connect:
            await self._ws_queue.put(tv_event.to_json)
        return await asyncio.gather(producer, consumer)

    def __repr__(self):
        return f"{vars(self)}"
