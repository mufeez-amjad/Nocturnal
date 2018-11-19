import serial
import gspread
from oauth2client.service_account import ServiceAccountCredentials

ser = serial.Serial('/dev/cu.usbmodem14101', 9600)

credentials = ServiceAccountCredentials.from_json_keyfile_name('Nocturnal-7d790916f958.json', scope)
gc = gspread.authorize(credentials)

def formatData(data):
    return data

def readData():
    while True:
        print(formatData(ser/readline()))

readData()
