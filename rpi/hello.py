import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template, jsonify
import datetime

app = Flask(__name__)

weekLabels = [
    'Monday', 'Tuesday', 'Wednesday', 'Thursday',
    'Friday', 'Saturday', 'Sunday'
]

tips = [
    'Increase bright light exposure during the day', 'Reduce blue light exposure in the evening', 'Don\'t consume caffeine late in the day', 'Reduce irregular or long daytime naps',
    'Try to sleep and wake at consistent times', 'Take a melatonin supplement', 'Don\'t drink alcohol', 'Optimize your bedroom environment', 'Set your bedroom temperature',
    'Don\'t eat late in the evening', 'Relax and clear your mind in the evening', 'Take a relaxing bath or shower', 'Rule out a sleep disorder', 'Get a comfortable bed, mattress and pillow',
    'Exercise regularly - but not before bed', 'Don\'t drink any liquids before bed'
]

timeIntervals = [
    '00:00', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30', '04:00', '04:30', '05:00', '05:30', '06:00', '06:30', '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00',
    '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30'
]

#Spreadsheed Auth
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('Nocturnal-7d790916f958.json', scope)
gc = gspread.authorize(credentials)

@app.route("/", methods=['GET', 'POST'])
def hello():
    wks = gc.open('Nocturnal').worksheet("Time")

    allTime = wks.col_values(2)
    del allTime[0]

    thisWeekTime = allTime[-7:] #last seven days
    dates = wks.col_values(1) #used to place it in order by day
    del dates[0]

    dates = dates[-7:]
    thisWeekTimeOrdered = [0 for x in range(7)]

    for i in range(len(thisWeekTime)): #orders
        month, day, year = (int(x) for x in dates[i].split('/'))
        weekDay = datetime.date(year, month, day).weekday()
        thisWeekTimeOrdered[weekDay] = thisWeekTime[i]

    avgTime = 0
    for cell in allTime:
        avgTime += float(cell)

    avgTime /= len(allTime)
    avgTime = round(avgTime, 1)

    wks = gc.open('Nocturnal').worksheet("Ideal")
    idealData = wks.get_all_records()

    #compare sleep scores with variables
    sleepScores = wks.col_values(2)
    del sleepScores[0]
    sleepScores = list(map(int, sleepScores))
    maxSleepScore = (max(sleepScores))
    idealTemps = []
    idealHumids = []
    idealLuxes = []
    for row in idealData:
        if (int(row['Sleep Score']) >= maxSleepScore):
            idealTemps.append(row['Temperature'])
            idealHumids.append(row['Humidity'])
            idealLuxes.append(row['Lux'])

    idealTemp = sum(idealTemps) / len(idealTemps)
    idealHum = sum(idealHumids) / len(idealHumids)
    idealLux = sum(idealLuxes) / len(idealLuxes)
    idealLight = ""
    if (idealLux < 300): idealLight = "Dark"
    elif (idealLux < 450): idealLight = "Dim"
    elif (idealLux < 650): idealLight = "Average"
    else: idealLight = "Bright"

    lightingToday = ""
    todaysLighting = idealData[-1]['Lux']
    if (todaysLighting < 300): lightingToday = "Dark"
    elif (todaysLighting < 450): lightingToday = "Dim"
    elif (todaysLighting < 650): lightingToday = "Average"
    else: lightingToday = "Bright"

    thisWeekSleepScores = sleepScores[-7:] #last seven days
    dates = wks.col_values(1) #used to place it in order by day
    del dates[0]

    dates = dates[-7:]
    thisWeekSleepScoresOrdered = [0 for x in range(7)]

    for i in range(len(thisWeekSleepScores)): #orders
        month, day, year = (int(x) for x in dates[i].split('/'))
        weekDay = datetime.date(year, month, day).weekday()
        thisWeekSleepScoresOrdered[weekDay] = thisWeekSleepScores[i]

    wks = gc.open('Nocturnal').worksheet("Night")

    nightData = wks.get_all_records()
    condensedNightData = []
    averageForInterval = 0

    timeLabels = []

    for i in range(len(nightData)):
        averageForInterval += nightData[i]['Activity']
        if (nightData[i]['Time'] in timeIntervals):
            timeLabels.append(nightData[i]['Time'])
            if (i < 30): averageForInterval /= i+1
            else: averageForInterval /= 30
            condensedNightData.append(averageForInterval)
            averageForInterval = 0

    return render_template('index.html', sleepGraphLabels=timeLabels, values=condensedNightData, timeWeekLabels=weekLabels,
     averageTime=avgTime, timeGraphData=thisWeekTimeOrdered, tipsArr=tips, timeSleptToday=round(float(thisWeekTime[-1]), 1),
      idealHumidity=idealHum, idealTemperature=idealTemp, idealLighting=idealLight, tempToday=idealData[-1]['Temperature'],
       humidityToday=idealData[-1]['Humidity'], lightingToday=lightingToday, thisWeekSleepScore=thisWeekSleepScoresOrdered)

@app.route("/update", methods=['POST'])
def update():
    wks = gc.open('Nocturnal').worksheet("Night")

    nigthData = wks.get_all_records()
    condensedNightData = []
    averageForInterval = 0

    timeLabels = []

    for i in range(len(nigthData)):
        averageForInterval += nigthData[i]['Activity']
        if (nigthData[i]['Time'] in timeIntervals):
            timeLabels.append(nigthData[i]['Time'])
            if (i < 30): averageForInterval /= i+1
            else: averageForInterval /= 30
            condensedNightData.append(averageForInterval)
            averageForInterval = 0

    return render_template('sleepGraph.html', sleepGraphLabels=timeLabels, values=condensedNightData, timeWeekLabels=weekLabels)

if __name__ == "__main__":
    app.run(debug=True)
