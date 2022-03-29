import asyncio
from functools import wraps
from rogerthat.utils.regexes import regexes
from rogerthat.logging.configure import AsyncioLogger


logger = AsyncioLogger.get_logger_main(__name__)


class websockets_queue:
    def __init__(self):
        self._connected_websockets = set()
        self._connected_websockets_filtered = {}

    def _add_connection(self, filtered=None):
        queue = asyncio.Queue()
        if filtered:
            if filtered not in self._get_filter_keys():
                self._connected_websockets_filtered[filtered] = set()
            self._connected_websockets_filtered[filtered].add(queue)
        else:
            self._connected_websockets.add(queue)
        return queue

    def _remove_connection(self, queue, filtered=None):
        if filtered:
            self._connected_websockets_filtered[filtered].remove(queue)
        else:
            self._connected_websockets.remove(queue)

    def _get_filter_keys(self):
        return list(self._connected_websockets_filtered.keys())

    def _is_filtered_event(self, event):
        filter_keys = self._get_filter_keys()
        return event.event_descriptor and event.event_descriptor in filter_keys

    def _get_filter_from_args(self, kwargs):
        filter_name = None
        if kwargs:
            channel_name = kwargs.get("channel")
            if channel_name and regexes.valid_ws_channel_name.match(channel_name):
                filter_name = channel_name
        return filter_name

    def collect_websocket(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            filter_name = self._get_filter_from_args(kwargs)
            queue = self._add_connection(filter_name)
            try:
                return await func(queue, *args, **kwargs)
            finally:
                self._remove_connection(queue, filter_name)
        return wrapper

    async def broadcast(self, event):
        logger.info("Broadcasting message to all websocket queues.")
        for queue in self._connected_websockets:
            await queue.put(event.to_json)
        if self._is_filtered_event(event):
            logger.info(f"Broadcasting message to {event.event_descriptor} websocket queue.")
            for queue in self._connected_websockets_filtered[event.event_descriptor]:
                await queue.put(event.to_json)


ws_queue = websockets_queue()
