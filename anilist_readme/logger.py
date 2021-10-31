import logging

logger = logging.getLogger("AniList")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(fmt='%(asctime)s [%(levelname)s] - %(name)s: %(message)s',
                                       datefmt="%x %X"))

logger.addHandler(handler)
