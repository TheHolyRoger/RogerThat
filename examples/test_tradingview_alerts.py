import asyncio
import sys

import aiohttp
import path_util  # noqa: F401

try:
    from rogerthat.config.config import Config
except Exception:
    print("Unable to load Config for tests, edit example manually.")
    sys.exit(0)


test_data = {
    "topic": "hbot/1/start",
    "log_level": "DEBUG"
}

ROGERTHAT_HOST = "localhost"
ROGERTHAT_PORT = Config.get_inst().quart_server_port
ROGERTHAT_API = Config.get_inst().api_allowed_keys_tv[0]


async def main():
    """
    Use this script to test/fake a TradingView alert.
    """
    headers = {
        "User-Agent": "go-http-client/1.1"
    }
    url = f"http://{ROGERTHAT_HOST}:{ROGERTHAT_PORT}/api/tv_webhook/?api_key={ROGERTHAT_API}"
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, json=test_data) as resp:
            print(f"HTTP Status: {resp.status}")
            print(f"Response: {await resp.text()}")

asyncio.run(main())
