import asyncio
import logging
import logging.handlers
from os.path import join as path_join
from queue import SimpleQueue as Queue
from typing import List

from rogerthat.config.config import Config
from rogerthat.logging.colours import ColouredFormatter

LOGGING_FILE_LIMIT = 1e6
LOG_LEVEL_ROOT = logging.DEBUG
LOG_LEVEL_GENERAL = logging.DEBUG


class AsyncLoggingQueueHandler(logging.handlers.QueueHandler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            self.enqueue(record)
        except asyncio.CancelledError:
            raise
        except Exception:
            self.handleError(record)


class AsyncLoggingQueueListener(logging.handlers.QueueListener):
    pass


class AsyncLoggingRotatingFileHandler(logging.handlers.RotatingFileHandler):
    pass


class AsyncLoggingStreamHandler(logging.StreamHandler):
    pass


class AsyncioLogger():
    _root_logger = None
    _file_handlers = {}
    _stream_handler = None
    _main_logs = {}
    _db_logs = {}
    _rolled_over = []

    @classmethod
    def _do_rollover(cls, log_file, handler):
        if log_file in cls._rolled_over:
            return
        cls._rolled_over.append(log_file)
        handler.doRollover()

    @classmethod
    def _build_logging_handler_stream(cls, filters=None):
        if cls._stream_handler:
            return
        stream_formatter = ColouredFormatter('[%(asctime)s] $BOLD%(name)s$RESET - %(levelname)s - %(message)s')
        stream_handler = AsyncLoggingStreamHandler()
        stream_handler.setFormatter(stream_formatter)
        if filters:
            stream_handler.addFilter(filters)
        cls._stream_handler = stream_handler

    @classmethod
    def _build_logging_handler_file(cls, log_file, filters=None):
        if log_file in cls._file_handlers:
            return
        file_formatter = logging.Formatter('[%(asctime)s] %(name)s - %(levelname)s - %(message)s')
        log_path = path_join(Config.get_inst().project_root, "logs", f"{Config.get_inst().app_name}-{log_file}.log")
        file_handler = AsyncLoggingRotatingFileHandler(
            log_path,
            "a",
            delay=True,
            maxBytes=LOGGING_FILE_LIMIT,
            backupCount=20)
        file_handler.setFormatter(file_formatter)
        if filters:
            file_handler.addFilter(filters)
        cls._do_rollover(log_file, file_handler)
        cls._file_handlers[log_file] = file_handler

    @classmethod
    def _build_logging_queue(cls, log_file, root, filters=None, set_log_level=True):
        cls._build_logging_handler_file(log_file, filters=filters)
        cls._build_logging_handler_stream(filters=filters)

        if set_log_level:
            root.setLevel(LOG_LEVEL_GENERAL)

        handlers: List[logging.Handler] = []
        queue = Queue()
        handler = AsyncLoggingQueueHandler(queue)
        root.addHandler(handler)
        for h in root.handlers[:]:
            if h is not handler:
                root.removeHandler(h)
                handlers.append(h)
        handlers.extend([cls._file_handlers[log_file], cls._stream_handler])

        listener = AsyncLoggingQueueListener(
            queue, *handlers, respect_handler_level=True
        )
        listener.start()

        return root

    @classmethod
    def _setup_root_logging_queue(cls):
        if not cls._root_logger:
            cls._root_logger = logging.getLogger()
            cls._root_logger.setLevel(LOG_LEVEL_ROOT)
            cls._build_logging_queue("root",
                                     cls._root_logger,
                                     set_log_level=False)

    @classmethod
    def setup_logging_queue(cls, log_file, log_name):
        cls._setup_root_logging_queue()

        root = logging.getLogger(log_name)
        root.propagate = False
        return cls._build_logging_queue(log_file, root)

    @classmethod
    def get_logger_main(cls, log_name):
        if log_name not in cls._main_logs:
            cls._main_logs[log_name] = cls.setup_logging_queue("Main", log_name)
        return cls._main_logs[log_name]

    @classmethod
    def get_logger_db(cls, log_name):
        if log_name not in cls._db_logs:
            cls._db_logs[log_name] = cls.setup_logging_queue("DB", log_name)
        return cls._db_logs[log_name]
