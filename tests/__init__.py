import logging

# Disable logger output during tests
anilist_logger = logging.getLogger("AniList")
anilist_logger.setLevel(logging.CRITICAL)
anilist_logger.disabled = True
# Remove all handlers to prevent any output
anilist_logger.handlers = []

