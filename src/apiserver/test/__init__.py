from src.config.logging import LogConfig

log = LogConfig(__name__)
logger = log.create_logger()
