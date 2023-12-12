import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AirlinesApp.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AirlinesApp.settings")
    try:
        from configurations.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    try:
        execute_from_command_line(sys.argv)
    except Exception as e:
        sys.exit(1)


if __name__ == "__main__":
    main()
