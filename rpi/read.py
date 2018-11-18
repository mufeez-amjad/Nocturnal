import serial

ser = serial.Serial('/dev/cu.usbmodem14101', 9600)

def readData():
    while True:
        print(ser.readline())

readData()
