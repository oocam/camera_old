import os
import logging
import logging.config

sensors_logger = logging.getLogger(__name__)

try:
    from .ms5837 import MS5837_30BA, DENSITY_SALTWATER, UNITS_Centigrade, UNITS_mbar
except Exception as e:
    sensors_logger.error(e)


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
