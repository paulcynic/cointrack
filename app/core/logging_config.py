import logging
import sys

from app.core.config import settings
from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth,
                   exception=settings.LOG_TRACEBACK  #record.exc_info
                   ).log(level, record.getMessage())


def setup_logging():
    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    # remove every ther logger's handlers
    # and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # configure loguru
    logger.configure(handlers=[{"sink": sys.stdout}])
    # add to serialize -- "serialize": JSON_LOGS}])
    # writes logs to file
    logger.add("server.log",
               format="{time} {level} {message}",
               level=settings.LOG_LEVEL,
               backtrace=False,
               rotation="10 MB",
               compression="zip",
               retention="30 days"
               )

