import serial
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('Nocturnal-7d790916f958.json', scope)

gc = gspread.authorize(credentials)

time_sheet = gc.open('Nocturnal').worksheet("Time")
night_sheet = gc.open('Nocturnal').worksheet("Night")
ideal_sheet = gc.open('Nocturnal').worksheet("Ideal")

ser = serial.Serial('/dev/cu.usbmodem14301', 9600)

count = 0

sleeping = False

temp_sum = 0
humid_sum = 0
light_sum = 0
max_activity = 0
previous_light = 500

current_minute = datetime.datetime.now().minute

start_time = 0
end_time = 0

def formatLine(line):
    output = str(line)
    return output[2:len(output)-5]

def getType(line):
    return line[:line.find(":")]

def getValue(line):
    return float(line[line.find(":")+1:])

def uploadMinute():
    current_time = datetime.datetime.now()
    time_string = current_time.strftime("%H:%M")
    night_sheet.append_row([time_string, max_activity])

def uploadWake():
    time_difference = end_time - start_time
    duration = round(float(time_difference.total_seconds()) / 3600, 1)
    date_string = "%s/%s/%s" % (start_time.month, start_time.day, start_time.year)
    start_string = start_time.strftime("%H:%M")
    end_string = end_time.strftime("%H:%M")
    sleepscore = 5
    avg_temp = int(temp_sum / count)
    avg_humid = int(humid_sum / count)
    avg_light = int(light_sum / count)
    time_sheet.append_row([date_string, duration, start_string, end_string])
    ideal_sheet.append_row([date_string, sleepscore, avg_temp, avg_humid, avg_light])

def readData():
    global count
    global sleeping
    global temp_sum, humid_sum, light_sum, max_activity, previous_light
    global current_minute, start_time, end_time
    while True:
        line = formatLine(ser.readline())
        if line == "END":
            if sleeping:
                count += 1
                print(count)
        else:
            type = getType(line)
            value = getValue(line)
            if type == "Activity":
                if sleeping and (value > max_activity):
                    max_activity = value
            else:
                value = int(value)
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
                        # Clear night sheet
                        start_time = datetime.datetime.now()
                        sleeping = True
                    elif previous_light < 300 and value > 300 and sleeping:
                        # Make sure they aren't temporarily waking up
                        print("Waking up...")
                        end_time = datetime.datetime.now()
                        uploadWake()
                        sleeping = False
                        count = 0
                        temp_sum = 0
                        humid_sum = 0
                        light_sum = 0
                        max_activity = 0
                        previous_light = 500
                        start_time = 0
                        end_time = 0
                    previous_light = value
        if datetime.datetime.now().minute != current_minute:
            current_minute = datetime.datetime.now().minute
            if sleeping:
                uploadMinute()
                max_activity = 0

readData()
