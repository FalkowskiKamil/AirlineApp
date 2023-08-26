import logging
from django.conf import settings

def configure_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(settings.LOGGING["loggers"]["airlinesapp"]["level"])

    # Check if the logger already has the handler
    if not logger.handlers:
        handler = logging.FileHandler(settings.LOGGING["handlers"]["file"]["filename"])
        handler.setLevel(settings.LOGGING["handlers"]["file"]["level"])

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger

def logger_example():
    logger = configure_logger()
    logger.info(f"Example logger")