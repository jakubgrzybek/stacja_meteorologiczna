#Libraries
import time
import Adafruit_DHT
from bmp280 import BMP280
from smbus2 import SMBus


class Raspberry_sensors():

    def __init__(self):
        self.name = __name__
        self.DHT_PIN = 21
        self.DHT_SENSOR = Adafruit_DHT.DHT22
        self.bus = SMBus(1)
        self.bmp280 = BMP280(i2c_dev=self.bus)

        #BH1750
        self.DEVICE     = 0x23 # Default device I2C address
        self.POWER_DOWN = 0x00 # No active state
        self.POWER_ON   = 0x01 # Power on
        self.RESET      = 0x07 # Reset data register value
        # Start measurement at 4lx resolution. Time typically 16ms.
        self.CONTINUOUS_LOW_RES_MODE = 0x13
        # Start measurement at 1lx resolution. Time typically 120ms
        self.CONTINUOUS_HIGH_RES_MODE_1 = 0x10
        # Start measurement at 0.5lx resolution. Time typically 120ms
        self.CONTINUOUS_HIGH_RES_MODE_2 = 0x11
        # Start measurement at 1lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        self.ONE_TIME_HIGH_RES_MODE_1 = 0x20
        # Start measurement at 0.5lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        self.ONE_TIME_HIGH_RES_MODE_2 = 0x21
        # Start measurement at 1lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        self.ONE_TIME_LOW_RES_MODE = 0x23
        self.bus = SMBus(1)  # Rev 2 Pi uses 1


    def readLight(self):
        # Read data from I2C interface
        data = self.bus.read_i2c_block_data(self.DEVICE,self.ONE_TIME_HIGH_RES_MODE_1,16)
        return self.convertToNumber(data)

    def convertToNumber(self, data):
        # Simple function to convert 2 bytes of data
        # into a decimal number. Optional parameter 'decimals'
        # will round to specified number of decimal places.
        result=(data[1] + (256 * data[0])) / 1.2
        return (result)