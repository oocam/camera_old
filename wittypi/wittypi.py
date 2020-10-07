import os
import logging

wittypi_logger = logging.getLogger(__name__)


class WittyPi:
    def __init__(self, path):
        # path as path to wittypi.sh script
        if os.path.isfile(self.path):
            self.path = path
        else:
            wittypi_logger.error("Path not found.")

    def clear_wittypi_schedule(self):
        # Clear current schedule
        os.system(f"sudo sh f{self.path} 10 6")
        wittypi_logger.info("Schedule has been cleared.")

    def set_wittypi_time(self):
        # Set RTC time to system
        os.system(f"sudo sh {self.path} 2")
        wittypi_logger.info("RTC time has been set to system.")

    def set_system_time(self):
        # Set system time to RTC
        os.system(f"sudo sh {self.path} 1")
        wittypi_logger.info("System time has been set to RTC.")

    def set_shutdown_time(self, shutdown_time):
        # Set Raspberry Pi next shutdown time
        os.system(f"sudo sh {self.path} 4 {self.shutdown_time}")
        wittypi_logger.info(f"Shutdown has been set to {self.shutdown_time}.")

    def set_startup_time(self, startup_time):
        # Setting Raspberry Pi next startup time
        os.system(f"sudo sh {self.path} 5 {self.startup_time}")
        wittypi_logger.info(f"Startup has been set to {self.startup_time}.")
