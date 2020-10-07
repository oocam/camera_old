import os
import json
import logging
from datetime import datetime

sensors_logger = logging.getLogger(__name__)

from .ms5837 import MS5837_30BA, DENSITY_SALTWATER, UNITS_Centigrade, UNITS_mbar
from .tsys01 import TSYS01_30BA, UNITS_Centigrade
from .tsl2561 import TSL2561_30BA


class ReadSensorData:
    def __init__(self, log_filename, pressure_data, temperature_data, luminosity_data):
        super().__init__()
        self.pressure_data = pressure_data
        self.temperature_data = temperature_data
        self.luminosity_data = luminosity_data
        self.log_filename = log_filename

    def write_data(self):
        if os.path.exists(self.log_filename):
            file_mode = "a"
        else:
            file_mode = "w"
        try:
            with open(self.log_filename, file_mode) as f:
                f.write(
                    json.dumps(
                        {
                            "timestamp": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                            "luminosity": self.luminosity_data,
                            "temp": self.temperature_data,
                            "pressure": self.pressure_data,
                        }
                    )
                )
        except:
            with open(self.log_filename, "w"):
                pass


# Pressure sensor
class PressureSensorNotConnectedException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PressureSensorCannotReadException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PressureSensor(MS5837_30BA):
    def __init__(self, bus=1):
        super().__init__(bus=bus)
        if not super().init():
            raise PressureSensorNotConnectedException(
                "MS5837_30BA may not be connected"
            )

        self.setFluidDensity(DENSITY_SALTWATER)

    def pressure(self, conversion=UNITS_mbar):
        if self.read():
            data = super().pressure(conversion=conversion)
            sensors_logger.info(f"Reading pressure data from the sensor: {data}")
            return data
        else:
            raise PressureSensorCannotReadException("Could not read pressure values")

    def temperature(self, conversion=UNITS_Centigrade):
        if self.read():
            data = super().temperature(conversion=conversion)
            sensors_logger.info(f"Reading temperature data from the sensor: {data}")
            return data
        else:
            raise PressureSensorCannotReadException("Could not read temperature values")

    def depth(self):
        if self.read():
            data = super().depth()
            sensors_logger.info(f"Reading depth data from the sensor: {data}")
            return data
        else:
            raise PressureSensorCannotReadException("Could not read depth values")


# Temperature sensor
class TemperatureSensorNotConnectedException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TemperatureSensorCannotReadException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TemperatureSensor(TSYS01_30BA):
    def __init__(self, bus=1):
        super().__init__(bus=bus)
        if not super().init():
            raise TemperatureSensorNotConnectedException(
                "TSYS01_30BA may not be connected"
            )

    def temperature(self, conversion=UNITS_Centigrade):
        if self.read():
            data = super().temperature(conversion=conversion)
            sensors_logger.info(f"Reading temperature data from the sensor: {data}")
            return data
        else:
            raise TemperatureSensorCannotReadException(
                "Could not read temperature values"
            )


# Luminosity Sensor
class LuminositySensorNotConnectedException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LuminositySensorCannotReadException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LuminositySensor(TSL2561_30BA):
    def __init__(self, bus=1):
        super().__init__(bus=bus)
        if not super().init():
            raise LuminositySensorNotConnectedException(
                "TSL2561_30BA may not be connected"
            )

    def luminosity(self):
        if self.read():
            data = super().lux()
            sensors_logger.info(f"Reading luminosity data from the sensor: {data}")
            return data
        else:
            raise LuminositySensorCannotReadException(
                "Could not read luminosity values"
            )


if __name__ == "__main__":
    pass
