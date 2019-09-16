import logging

logger = logging.getLogger('parallel_application')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('parallel_application.log')
fh.setLevel(logging.DEBUG)