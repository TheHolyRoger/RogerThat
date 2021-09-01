from datetime import datetime
import os
import time
import shutil
from rogerthat.config.config import Config
from rogerthat.utils.file_writing import append_to_file


class logger_cls:
    def __init__(self):
        self._log_dir = os.path.join(Config.project_root, "logs")
        self._log_file = None

    @property
    def log_file(self):
        if self._log_file:
            return os.path.join(self._log_dir, self._log_file)
        return None

    def set_file(self, log_file):
        self._log_file = f"{Config.app_name}-{log_file}.log"

    async def log(self, string):
        timeNow = datetime.now()
        string = f"[{timeNow}] {string}"
        print(string)
        if self.log_file:
            await append_to_file(string, self.log_file)
        return True

    def cycle(self):
        if self.log_file:
            fn = self.log_file.split(".log")[0]
            if os.path.exists(self.log_file):
                shutil.move(f"{fn}.log", f"{fn}.{int(time.time())}.log")


logger = logger_cls()
