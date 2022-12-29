import asyncio

from rogerthat.db.models.tradingview_event import tradingview_event
from rogerthat.logging.configure import AsyncioLogger
from rogerthat.utils.asyncio_tasks import safe_ensure_future

logger = AsyncioLogger.get_logger_main(__name__)


class request_processing_queue:
    _shared_instance: "request_processing_queue" = None

    @classmethod
    def get_instance(cls) -> "request_processing_queue":
        if cls._shared_instance is None:
            cls._shared_instance = cls()
        return cls._shared_instance

    def __init__(self):
        self._request_processing_queue_task = None
        self._request_processing_queue = None

        self.start()
        logger.info("Request Processing Queue ready.")

    def _create_queue(self):
        self._request_processing_queue = asyncio.Queue()

    def start(self):
        self._create_queue()
        self._request_processing_queue_task = safe_ensure_future(
            self._listen_for_requests()
        )

    async def _listen_for_requests(self):
        while True:
            req = await self._request_processing_queue.get()
            if isinstance(req, list):
                for req_msg in req:
                    tv_event = tradingview_event(from_json=req_msg)
                    safe_ensure_future(tv_event.process_event(), with_timeout=1800.0)
            else:
                tv_event = tradingview_event(from_json=req)
                safe_ensure_future(tv_event.process_event(), with_timeout=1800.0)

    def add_request(self, request):
        if not self._request_processing_queue:
            logger.error("Cannot process requests, queue not started!")
            return
        logger.debug("Adding TradingView event to processing queue.")
        self._request_processing_queue.put_nowait(request)
