# import asyncio
from rogerthat.config.config import Config
from rogerthat.server.server import quart_server
from rogerthat.utils.logger import logger
from rogerthat.utils.splash import splash_msg
from rogerthat.app.delegate import App
from rogerthat.db.database_init import database_init


class RogerThat:
    def __init__(self):
        logger.set_file("main")
        logger.cycle()
        App.update_instance(self)
        quart_server.run(host="0.0.0.0", port=Config.quart_server_port, debug=Config.debug_mode)

    async def Initialise(self):
        await logger.log("Initialising database.")
        await database_init.initialise()
        await logger.log("Finished initialising database.")
        await logger.log(splash_msg)
