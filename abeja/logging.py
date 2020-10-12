import logging
import sys
from logging import getLogger


logger = getLogger('tracking')
if len(logger.handlers) == 0:
    logger.addHandler(logging.StreamHandler(stream=sys.stdout))
if logger.level == logging.NOTSET:
    logger.setLevel(logging.WARN)
