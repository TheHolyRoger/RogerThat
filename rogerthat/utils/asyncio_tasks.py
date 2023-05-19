import asyncio
import inspect
import time
import traceback

from rogerthat.logging.configure import AsyncioLogger

logger = AsyncioLogger.get_logger_main(__name__)


async def safe_wrapper(c, with_timeout=None):
    try:
        if with_timeout:
            return await asyncio.wait_for(c, timeout=with_timeout)
        else:
            return await c
    except asyncio.CancelledError:
        raise
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"Unhandled error in background task: {str(e)}\n{tb}")


def safe_ensure_future(coro, with_timeout=None, *args, **kwargs):
    return asyncio.ensure_future(safe_wrapper(coro, with_timeout=with_timeout), *args, **kwargs)


async def safe_gather(*args, **kwargs):
    try:
        return await asyncio.gather(*args, **kwargs)
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"Unhandled error in background task: {str(e)}\n{tb}")
        raise


async def wait_til(condition_func, timeout=10):
    start_time = time.perf_counter()
    while True:
        if condition_func():
            return
        elif time.perf_counter() - start_time > timeout:
            raise Exception(f"{inspect.getsource(condition_func).strip()} condition is never met. Time out reached.")
        else:
            await asyncio.sleep(0.1)


async def run_command(*args):
    process = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    return stdout.decode().strip()
