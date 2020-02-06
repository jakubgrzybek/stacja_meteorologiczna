import statistics, time, Adafruit_DHT
from bmp280 import BMP280
from decimal import Decimal
from atmega_sensors import Atmega_sensors

#Atmega commands
cmdRain             = "rain"
cmdPM               = "pm"

#REFERENCE
rain_treshold = 200
rain_iterations = 4
airPressure_iterations = 4

def calculateRain(object):
    object.open_connection()
    measurements = []
    for x in range (rain_iterations):
        measurements.append(convertToFloat(object.getData(cmdRain)))
    object.close_connection()
    sorted_measurements = sorted(measurements)
    median = statistics.median(sorted_measurements)
    if median < rain_treshold:
        result = False
    else:
        result = True
    return result

def calculateAirPollution(object):
    object.open_connection()
    result = round(convertToFloat(object.getData(cmdPM)),2)
    object.close_connection()
    return result

def calculateHumidity(object):
    try:
        humidity = Adafruit_DHT.read_retry(object.DHT_SENSOR, object.DHT_PIN)
        result = round(humidity[0],2)
    except:
        result = 0.0
    return result

def calculateTemperature(object):
    try:
        temperature = Adafruit_DHT.read_retry(object.DHT_SENSOR, object.DHT_PIN)
        result = round(temperature[1],2)
    except:
        result = 0.0
    return result

def calculateAirPressure(object):
    try:
        measurements = []
        for x in range (airPressure_iterations):
            measurements.append(convertToFloat(object.bmp280.get_pressure()))
        sorted_measurements = sorted(measurements)
        result = round(statistics.median(sorted_measurements),2)
    except:
        result = 0.0
    return result

def calculateLightIntensity(object):
    try:
        lightLevel = object.readLight()
        result = round(lightLevel,2)
    except:
        result = 0.0
    return result

def convertToFloat(word):
    return float(word)