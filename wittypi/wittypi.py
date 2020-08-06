import os

class WittyPi:
    def __init__(self, path):
        # path as path to wittypi.sh script
        self.path = path

    def clear_wittypi_schedule(self):
        # Clear current schedule
        os.system(f"sudo sh f{self.path} 10 6")
        
    def set_wittypi_time(self):
        # Set RTC time to system
        os.system(f"sudo sh {self.path} 2")

    def set_system_time(self):
        # Set system time to RTC
        os.system(f"sudo sh {self.path} 1")

    def set_shutdown_time(self, shutdown_time):
        # Set Raspberry Pi next shutdown time
        os.system(f"sudo sh {self.path} 4 {self.shutdown_time}")

    def set_startup_time(self, startup_time):
        # Setting Raspberry Pi next startup time
        os.system(f"sudo sh {self.path} 5 {self.startup_time}")