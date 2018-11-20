import serial
import gspread
from oauth2client.service_account import ServiceAccountCredentials

ser = serial.Serial('/dev/cu.usbmodem14301', 9600)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('Nocturnal-7d790916f958.json', scope)
gc = gspread.authorize(credentials)

sleeping = False

count = 1

temp_sum = 0
humid_sum = 0
light_sum = 0
previous_light = 500

def formatLine(line):
    output = str(line)
    return output[2:len(output)-5]

def getType(line):
    return line[:line.find(":")]

def getValue(line):
    return int(float(line[line.find(":")+1:]))

def uploadMinute(activity):
    # current time

def uploadWake():
    avg_temp = int(temp_sum / count)
    avg_humid = int(humid_sum / count)
    avg_light = int(light_sum / count)
    # sleep time
    # wake up time
    # sleep duration

def readData():
    while True:
        line = formatLine(ser.readLine())
        if line == "END":
            count += 1
        else:
            type = getType(line)
            value = getValue(line)
            if type == "Temperature":
                if sleeping:
                    temp_sum += value
            elif type == "Humidity":
                if sleeping:
                    humid_sum += value
            elif type == "Light":
                if sleeping:
                    light_sum += value
                if previous_light > 300 and value < 300 and not sleeping:
                    # Make sure its not day time
                    print("Going to bed...")
                    sleeping = True
                elif previous_light < 300 and value > 300 and sleeping:
                    # Make sure they were sleeping for 30+ minutes
                    print("Waking up...")
                    sleeping = False
                previous_light = value
            elif type == "Activity":

readData()
