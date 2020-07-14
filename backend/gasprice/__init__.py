import sys
import logging

from . import config
from .app import create_app
from .utils.cache import get_cache_client


def setup_logger():
    """
    Prepare logging
    """
    handler = logging.StreamHandler(
        sys.stdout if config.LOG_STDOUT else sys.stderr)
    formatter = logging.Formatter(config.LOG_FORMAT)
    handler.setFormatter(formatter)
    # Set global logger
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(config.LOG_LEVEL)


setup_logger()


# Singlton redis connection instance
redis_client = get_cache_client()
