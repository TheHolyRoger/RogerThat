import asyncio
import logging
import logging.handlers
from os.path import join as path_join
from queue import SimpleQueue as Queue
from typing import List
from rogerthat.config.config import Config
from rogerthat.logging.colours import ColouredFormatter


class AsyncioLoggingHandler(logging.handlers.QueueHandler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            self.enqueue(record)
        except asyncio.CancelledError:
            raise
        except Exception:
            self.handleError(record)


class AsyncioLogger():
    _root_logger = None
    _main_logs = {}
    _db_logs = {}

    @classmethod
    def _build_logging_queue(cls, root, log_file):
        queue = Queue()
        log_path = path_join(Config.project_root, "logs", f"{Config.app_name}-{log_file}.log")

        # Set all logs to DEBUG for now
        root.setLevel(logging.DEBUG)

        file_formatter = logging.Formatter('[%(asctime)s] %(name)s - %(levelname)s - %(message)s')
        stream_formatter = ColouredFormatter('[%(asctime)s] $BOLD%(name)s$RESET - %(levelname)s - %(message)s')

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(stream_formatter)
        file_handler = logging.FileHandler(log_path, "a")
        file_handler.setFormatter(file_formatter)

        handlers: List[logging.Handler] = []

        handler = AsyncioLoggingHandler(queue)
        root.addHandler(handler)
        for h in root.handlers[:]:
            if h is not handler:
                root.removeHandler(h)
                handlers.append(h)

        handlers.extend([file_handler, stream_handler])

        listener = logging.handlers.QueueListener(
            queue, *handlers, respect_handler_level=True
        )
        listener.start()

        return root

    @classmethod
    def _setup_root_logging_queue(cls):
        pass
        if not cls._root_logger:
            cls._root_logger = logging.getLogger()
            cls._build_logging_queue(cls._root_logger, "main")

    @classmethod
    def setup_logging_queue(cls, log_file, log_name):
        cls._setup_root_logging_queue()

        root = logging.getLogger(log_name)
        root.propagate = False
        return cls._build_logging_queue(root, log_file)

    @classmethod
    def get_logger_main(cls, log_name):
        if log_name not in cls._main_logs:
            cls._main_logs[log_name] = cls.setup_logging_queue("main", log_name)
        return cls._main_logs[log_name]

    @classmethod
    def get_logger_db(cls, log_name):
        if log_name not in cls._db_logs:
            cls._db_logs[log_name] = cls.setup_logging_queue("db", log_name)
        return cls._db_logs[log_name]
