#!/usr/bin/env python
import asyncio
import sys
import path_util  # noqa: F401
from rogerthat.app.rogerthat import RogerThat


if __name__ == "__main__":
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    RogerThat()
