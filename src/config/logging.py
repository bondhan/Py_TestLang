import errno
import logging
import os
from pathlib import Path

class LogConfig:
    log_filename = ""
    # LOG_DIR = str(Path(__file__).parents[1]) + "\log\\"
    LOG_DIR = ".\log\\"

    def __init__(self, log_filename, level=logging.ERROR):
        self.level = level
        self.log_loc = self.LOG_DIR + Path(log_filename).stem + ".log"

    def create_logger(self):

        try:
            os.makedirs(self.LOG_DIR)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s", "%Y-%m-%d %H:%M:%S")

        logger = logging.getLogger("sqlalchemy.engine")
        # logger = logging.getLogger()
        logger.setLevel(self.level)

        fh = logging.FileHandler(self.log_loc)
        fh.setFormatter(formatter)
        fh.setLevel(self.level)

        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        ch.setLevel(self.level)

        logger.addHandler(ch)
        logger.addHandler(fh)

        return logger

    def __repr__(self):
        return "Saving the log file to {}{}".format(self.LOG_DIR, self.log_filename)
