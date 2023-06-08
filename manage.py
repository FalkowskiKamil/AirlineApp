import os
import sys
import logging
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AirlinesApp.settings")

def configure_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(settings.LOGGING['loggers']['airlinesapp']['level'])

    # Check if the logger already has the handler
    if not logger.handlers:
        handler = logging.FileHandler(settings.LOGGING['handlers']['file']['filename'])
        handler.setLevel(settings.LOGGING['handlers']['file']['level'])

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
    
    return logger


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AirlinesApp.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        logger.exception("An error occurred: %s", str(exc))
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    logger.info("Server is starting...")
    try:
        execute_from_command_line(sys.argv)
    except Exception as e:
        logger.exception("An error occurred: %s", str(e))
        sys.exit(1)


if __name__ == "__main__":
    logger = configure_logger()
    main()