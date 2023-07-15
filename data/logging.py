from loguru import logger

logger.add("logs/info.log", format="{time} | {level} | {message}", level="DEBUG", rotation="3 MB")
