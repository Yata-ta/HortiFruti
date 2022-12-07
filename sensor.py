import board
import adafruit_bme680

def initialize_sensor():
    i2c = board.I2C()
    bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
    return bme680
    # [TODO] - Validade connected sensor

def get_sensor_data(bme680):
    return bme680.temperature 
