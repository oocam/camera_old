import logging
import logging.config
from sensors import PressureSensor

logging.config.fileConfig("logging.ini")


def main():
    try:
        sensor = PressureSensor()
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    main()
