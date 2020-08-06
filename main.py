import logging
import logging_config
from sensors import PressureSensor
from sensors import TemperatureSensor
from sensors import LuminositySensor

def main():
    try:
        presure_sensor = PressureSensor()
    except Exception as e:
        logging.error(e)

    try:
        temperature_sensor = TemperatureSensor()
    except Exception as e:
        logging.error(e)

    try:
        luminosity_sensor = LuminositySensor()
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    main()
