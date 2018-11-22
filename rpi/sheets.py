import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

timeLabels2 = [
    '00:00', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30', '04:00', '04:30', '05:00', '05:30', '06:00', '06:30', '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00',
    '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30'
]

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('Nocturnal-7d790916f958.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open('Nocturnal').worksheet("Ideal")
idealData = wks.get_all_records()

#compare sleep scores with variables
sleepScores = wks.col_values(2)
del sleepScores[0]
sleepScores = map(int, sleepScores)
maxSleepScore = (max(sleepScores))
idealTemps = []
idealHumids = []
idealLuxes = []
for row in idealData:
    if (int(row['Sleep Score']) >= maxSleepScore):
        idealTemps.append(row['Temperature'])
        idealHumids.append(row['Humidity'])
        idealLuxes.append(row['Lux'])

idealTemperature = sum(idealTemps) / len(idealTemps)
idealHumidity = sum(idealHumids) / len(idealHumids)
idealLux = sum(idealLuxes) / len(idealLuxes)

# print(condensedData)
# for row in data

# wks.delete_row(2)

# print(wks.get_all_records())

#dictionary with rows
# wks.append_row(['this goes into first column', 'this goes into second column'])

# print(wks.acell('A2'))
# print(wks.cell(2,1).value) #row 2 column 1 .col return column, .row returns row .value returns value at cell

# wks.update_acell('B2', "This is B2")
# wks.update_cell(3,2, "This is B3")

# print(wks.find('Test')) #findall if theres duplicates

# list_of_cells = wks.findall('Test')

# for cell in list_of_cells:
#   cell.value = 'Looped value'
# list_of_cells[2].value = 'New value'

# wks.update_cells(list_of_cells)