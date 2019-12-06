# create_logger the log
import os
from pathlib import Path

from config.logging import LogConfig

logObj = LogConfig(__name__)
logger = logObj.create_logger(__file__)
print(logObj)


logger.debug("test")
