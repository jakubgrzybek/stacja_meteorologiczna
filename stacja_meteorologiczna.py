__author__ = "Jakub Grzybek"

import os, json, requests, time, datetime, compute, atmega_sensors, raspberry_sensors
from pprint import pprint
from atmega_sensors import Atmega_sensors
from raspberry_sensors import Raspberry_sensors
from data_sender import Data_sender

file = "offline_measurements.json"
local_database="local_database.txt"

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def connected_to_internet(url='http://www.google.com/', timeout=5):
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("No internet connection available.")
        return False

def is_file_empty(path):
    try:
        with open('{}'.format(path), 'r', encoding='utf-8') as f:
            f.seek(0)
            first_char = f.read(1)
            if not first_char:
                result = True
            else:
                result = False
            return result
    except:
        open("{}".format(path), "w").close()
        result = True
        return result

def append_measurements_to_file(path, measurements):
    with open('{}'.format(path), 'a', encoding='utf-8') as f:
        json.dump(measurements, f, ensure_ascii=False, indent=4)

def clear_file(path):
    open("{}".format(path), "w").close()

def send_first_measurements_from_file_and_save_the_rest(path):
    with open('{}'.format(path), 'r', encoding='utf-8') as f:
        data = f.read()
    data = data.replace('}{', '}\n\n{')
    data = data.split('\n\n')
    processed_data = json.loads(data[0])
    print ("Data to be send: {}".format(processed_data))
    data_sender.send_data(processed_data)
    clear_file(file)
    for i in range(len(data)):
        if i == 0:
            continue
        else:
            print("Data to be stored in file: {}".format(data[i]))
            data_to_append = json.loads(data[i])
            append_measurements_to_file(file, data_to_append)

if __name__ == '__main__':

    atmega_sensors = Atmega_sensors()
    raspberry_sensors = Raspberry_sensors()
    data_sender = Data_sender("http://station-api.foreel.linuxpl.eu/station-measurement/append/1074846e57dd2a98eb37182dcb1dd2dd")
    
    cls()
    print("Gathering data from sensors...")
    print("-"*20)
    print("DATA:")
    print("-"*20)
    ts = time.time()
    dt = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print("DateTime: {}".format(dt))
    print("Timestamp: {}".format(ts))
    li = compute.calculateLightIntensity(raspberry_sensors)
    print("Light intensity: {} lx".format(li))
    rn = compute.calculateRain(atmega_sensors)
    print("Is raining: {}".format(rn))
    pm = compute.calculateAirPollution(atmega_sensors)
    print("Air pollution: {} ug/m3".format(pm))
    hd = compute.calculateHumidity(raspberry_sensors)
    print("Air humidity: {} %".format(hd))
    temp = compute.calculateTemperature(raspberry_sensors)
    print("Air temperature: {} \u00B0C".format(temp))
    ap = compute.calculateAirPressure(raspberry_sensors)
    print("Air pressure: {} hPa".format(ap))
    print("-"*20)
    time.sleep(5)
    cls()

    measurements = ({'time_stamp' : ts, 'rain' : rn, 'pm': pm, 'humidity' : hd, 'temperature' : temp, 'light_intensity' : li, 'air_pressure': ap})
    measurements_for_local_database = ({'Czas:' : dt, 'Opady:' : rn, 'PM(2.5)': pm, 'Wilgotność' : hd, 'Temperatura' : temp, 'Natężenie światła' : li, 'Ciśnienie': ap})
    append_measurements_to_file(file,measurements)
    append_measurements_to_file(local_database,measurements_for_local_database)

    if connected_to_internet() is True:
        print("Connected to the internet!")
        i = 0
        while is_file_empty(file) is False: 
            try:
                i+=1
                print("-"*20)
                print("There is something in database to be send!")
                print("Trying to send the oldest measurements stored in file...[{}]".format(i))
                print("-"*20)
                send_first_measurements_from_file_and_save_the_rest(file)
            except:
                print("-"*20)
                print("Failed to send data!!")
                print("-"*20)
        print("Everything is up to date.")
            
    else:
        print("There was a problem with internet connection!")
        print("Data is stored in the database for future trial")
    print("-"*20)
    print("Done!")
    print("")