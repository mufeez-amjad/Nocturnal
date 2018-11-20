import serial
import gspread
from oauth2client.service_account import ServiceAccountCredentials

ser = serial.Serial('/dev/cu.usbmodem14301', 9600)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('Nocturnal-7d790916f958.json', scope)
gc = gspread.authorize(credentials)

def formatLine(data):
    output = str(data)
    return output[2:len(output)-5]

def getType(data):
    return data[:data.find(":")]

def getValue(data):
    return int(float(data[data.find(":")+1:]))

second = 0
activity = 0
temperature = 0
humidity = 0
light = 500

sleepsecond = 0
wakesecond = 0

sleeping = False

def uploadMinute():
    

def uploadWakeUp():

def readData():
    while True:
        line = formatLine(ser.readline())

        if line == "END":
            if second % 60 == 0 and sleeping:
                uploadMinute()
            second += 1

        type = getType(line)
        value = getValue(line)

        if type == "Activity":
            activity += value
        elif type == "Temperature":
            temperature += value
        elif type == "Humidity":
            humidity += value
        elif type == "Light":
            if light > 300 and value < 300 and not sleeping:
                # go to sleep
                print("Going to bed...")
                sleepsecond = second
                sleeping = True
            elif light < 300 and value > 300 and sleeping:
                if second - sleepsecond > 1800: # slept for at least 30 minutes
                    # wake up
                    print("Waking up...")
                    wakesecond = second
                    sleeping = False


                    sleep_duration = float(float(wakesecond - sleepsecond) / 3600)

            light = value



readData()
