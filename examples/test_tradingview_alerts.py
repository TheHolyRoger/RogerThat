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
    "topic": "hbot/hummingbot_instance_1/start",
    "log_level": "DEBUG"
}

test_data_list = [
    {
        "topic": "hbot/hummingbot_instance_1/start",
        "log_level": "DEBUG"
    },
    {
        "topic": "hbot/hummingbot_instance_1/external/events/my_event",
        "type": "external_event",
        "timestamp": 1234567890,
        "sequence": 1234567890,
        "data": {
            "exchange": "{{exchange}}",
            "symbol": "{{ticker}}",
            "interval": "{{interval}}",
            "price": "{{close}}",
            "volume": "{{volume}}",
            "position": "{{strategy.market_position}}",
            "inventory": "{{strategy.order.comment}}"
        }
    }
]

ROGERTHAT_HOST = "localhost"
ROGERTHAT_PORT = Config.get_inst().quart_server_port
ROGERTHAT_API = Config.get_inst().api_allowed_keys_tv[0]


async def print_response(resp):
    print(f"HTTP Status: {resp.status}")
    print(f"Response: {await resp.text()}")


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
            await print_response(resp)

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, json=test_data_list) as resp:
            await print_response(resp)

asyncio.run(main())
