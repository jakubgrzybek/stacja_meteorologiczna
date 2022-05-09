import serial, time

#test

class Atmega_sensors():
    
    def __init__(self):
        self.name = __name__
        self.name = serial.Serial('/dev/ttyS0', 9600)

    def open_connection(self):
        if not (self.name.isOpen()):
            self.name.open()
        else:
            self.name.reset_input_buffer()

    def getData(self, command):
        result = ""
        isDataCollected = False
        self.name.write(command.encode())
        time.sleep(.1)

        while not isDataCollected:
            if(self.name.inWaiting()):
                line = self.name.readline().decode()
                result = line.strip('\r\n')
                isDataCollected = True
        return result

    def close_connection(self):
        self.name.close()