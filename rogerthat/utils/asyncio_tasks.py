import asyncio
import time
import inspect
import traceback
from rogerthat.utils.logger import logger


async def safe_wrapper(c):
    try:
        return await asyncio.wait_for(c, timeout=1800.0)
    except asyncio.CancelledError:
        raise
    except Exception as e:
        tb = traceback.format_exc()
        await logger.log(f"Unhandled error in background task: {str(e)}\n{tb}")


def safe_ensure_future(coro, *args, **kwargs):
    return asyncio.ensure_future(safe_wrapper(coro), *args, **kwargs)


async def safe_gather(*args, **kwargs):
    try:
        return await asyncio.gather(*args, **kwargs)
    except Exception as e:
        tb = traceback.format_exc()
        await logger.log(f"Unhandled error in background task: {str(e)}\n{tb}")
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
