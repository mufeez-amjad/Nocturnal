import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template

app = Flask(__name__) 

weekLabels = [
    'Monday', 'Tuesday', 'Wednesday', 'Thursday',
    'Friday', 'Saturday', 'Sunday'
]

timeLabels2 = [
    '00:00', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30', '04:00', '04:30', '05:00', '05:30', '06:00', '06:30', '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00',
    '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30'
]

timeLabels = [
    '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30', '00:00', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30', '04:00', '04:30', '05:00', '05:30', '06:00', '06:30', '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00']

#Spreadsheed Auth
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('Nocturnal-7d790916f958.json', scope)

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"
]

@app.route("/")
def hello():
    gc = gspread.authorize(credentials)

    wks = gc.open('Nocturnal').worksheet("Time")

    allTime = wks.col_values(2)
    thisWeekTime = wks.col_values(4)
    del allTime[0]
    del thisWeekTime[0]

    avgTime = 0
    for cell in allTime:
        avgTime += float(cell)

    avgTime /= len(allTime)
    avgTime = round(avgTime, 1)

    wks = gc.open('Nocturnal').worksheet("Night")

    nigthData = wks.get_all_records()
    condensedNightData = []
    averageForInterval = 0

    for i in range(len(nigthData)):
        averageForInterval += nigthData[i]['Activity']
        if (nigthData[i]['Time'] in timeLabels2):
            if (i < 30): averageForInterval /= i+1
            else: averageForInterval /= 30
            condensedNightData.append(averageForInterval)
            averageForInterval = 0

    return render_template('index.html', sleepGraphLabels=timeLabels, values=condensedNightData, timeWeekLabels=weekLabels, averageTime=avgTime, timeGraphData=thisWeekTime)
 
if __name__ == "__main__":
    app.run(debug=True)
