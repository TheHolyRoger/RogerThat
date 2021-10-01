#!/usr/bin/env python
import asyncio
import os
import sys
import path_util  # noqa: F401
from rogerthat.app.rogerthat import RogerThat


if __name__ == "__main__":
    pid = os.getpid()
    pid_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), ".rogerthat.pid")
    with open(pid_file, "w+") as fp:
        fp.write(f"{pid}")
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    RogerThat().start_server()
