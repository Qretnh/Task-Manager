import logging
import sys

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)
logger.addHandler(stream_handler)
logger.propagate = False
