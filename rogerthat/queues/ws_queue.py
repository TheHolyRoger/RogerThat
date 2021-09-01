import asyncio
from functools import wraps


class websockets_queue:
    def __init__(self):
        self._connected_websockets = set()

    def collect_websocket(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            global connected_websockets
            queue = asyncio.Queue()
            self._connected_websockets.add(queue)
            try:
                return await func(queue, *args, **kwargs)
            finally:
                self._connected_websockets.remove(queue)
        return wrapper

    async def broadcast(self, data):
        for queue in self._connected_websockets:
            await queue.put(data)


ws_queue = websockets_queue()
