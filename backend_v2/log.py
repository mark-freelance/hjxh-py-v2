import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)7s] %(filename)s - %(funcName)s: %(message)s')
logger = logging.getLogger(__name__)
