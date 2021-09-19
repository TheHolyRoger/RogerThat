import asyncio
import ujson
import websockets
import path_util  # noqa: F401
from rogerthat.config.config import Config


async def test_websocket():
    ws_url = f"ws://localhost:{Config.quart_server_port}/{Config.wss_root}"
    headers = {
        "HBOT-API-KEY": Config.api_allowed_keys_hbot[0],
        "User-Agent": "hummingbot",
    }
    ws_client = await websockets.connect(ws_url, extra_headers=headers)
    print("\nConnected to websocket\n\n")
    try:
        while True:
            raw_msg_str: str = await asyncio.wait_for(ws_client.recv(), timeout=10000)
            json_msg = ujson.loads(raw_msg_str)
            print(json_msg)
    finally:
        print("\n\nClosing websocket.\n")
        if ws_client:
            await ws_client.close()


try:
    asyncio.run(test_websocket())
except KeyboardInterrupt:
    quit()
