import logging
import logging_config
from sensors import PressureSensor


def main():
    try:
        sensor = PressureSensor()
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    main()
