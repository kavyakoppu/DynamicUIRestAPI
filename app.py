import csv, logging, json, random, os
from datetime import date, datetime, timedelta
from flask import Flask, render_template, request, make_response, jsonify
app = Flask(__name__, template_folder='HTML')
# app.debug = True
app.static_folder = 'static'

def validateDate(inputDate):
    ValidDate = False
    try:
        inputDate = datetime.strptime(inputDate, "%Y%m%d").date()
        ValidDate = True
    except ValueError:
        ValidDate = False
    return ValidDate

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')
    # home = "Check Weather Information using the following Resources: \n/historical/ - GET, POST\n/historical/[date] - GET, DELETE\n/forecast/[date] - GET\n"
    # return home

@app.route('/historical/', methods=['GET'])
def getAvaliableHistoricalData():
    # if request.method == 'GET':
    dates = []
    with open('dailyweather.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 1
        for row in csv_reader:
            datefield = {"DATE":  row[0]}
            dates.append(datefield)
        dates.pop(0)
        # return json.dumps(dates)
        return make_response(jsonify(dates), 200)

@app.route('/historical/<inputDate>', methods=['GET'])
def gethistoricalDataOfADate(inputDate):
    if validateDate(inputDate) :
        data = []
        with open('dailyweather.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if(row[0] == inputDate):
                    data = {"DATE":  row[0], "TMAX": row[1], "TMIN": row[2]}
                    return make_response(jsonify(data), 200)
        return make_response(jsonify({'error' : 'Date Not found'}), 404)
    else :
        return make_response(jsonify({'error': 'Invalid Date'}), 400)

@app.route('/historical/', methods=['POST'])
def addHistoricalData():
    print(request.data)
    reqBodyData = json.loads(request.data)
    if validateDate(reqBodyData["DATE"]) :
        deleteHistoricalDataOfADate(reqBodyData["DATE"])
        outputFile = open('dailyweather.csv', 'a')
        outputWriter = csv.writer(outputFile)
        outputWriter.writerow([reqBodyData["DATE"], reqBodyData["TMAX"], reqBodyData["TMIN"]])
        return make_response(jsonify({'DATE' : reqBodyData["DATE"]}), 201)
    else :
        return make_response(jsonify({'error': 'Invalid Date'}), 400)

@app.route('/historical/<inputDate>', methods=['DELETE'])
def deleteHistoricalDataOfADate(inputDate):
    existing = False
    if validateDate(inputDate) :
        with open('dailyweather.csv', 'r') as inp, open('dailyweathercopy.csv', 'w') as temp:
            writer = csv.writer(temp)
            for row in csv.reader(inp):
                if row[0] != inputDate:
                    writer.writerow(row)
                else:
                    existing = True   
        os.remove('dailyweather.csv')
        os.rename('dailyweathercopy.csv', 'dailyweather.csv')
        if existing :
            return make_response(inputDate, 204)
        else :
            return make_response(jsonify({'error' : 'Date Not found'}), 404)
    else :
        return make_response(jsonify({'error': 'Invalid Date'}), 400)

@app.route('/forecast/<inputDate>', methods=['GET'])
def getForecastForAWeek(inputDate):
    if validateDate(inputDate) :
        forecast = []
        dictData = {}
        existing = False
        #add cold, moderate and hot temp for both min and max 
        sampleColdMaxData = [15.3, 18.8, 21, 24.4, 27.9, 31.1, 32.6] # 15 to 33
        sampleColdMinData = [-13.6, -12.1, 9.7, 11.4, 13.6, 14.9, 20.7 ] # -15 to 20
        sampleHotMaxData = [80.3, 83.2, 84.5, 86.8, 88, 90.4, 92.6, 94.9] # 80 to 95 
        sampleHotMinData = [64.8, 69.1, 70.8, 71.6, 72, 73.1, 74.5, 77.7] # 65 to 78
        sampleModMaxData = [63.2, 72.9, 68.2, 70.5, 67.6, 71.1, 72.3, 77.9] #65 to 75
        sampleModMinData = [44.7, 59.25, 51.2, 61.75, 52.5, 62.4, 61.3, 59.3]#45 to 60
        with open('dailyweather.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                dictData[row[0]] = {"DATE": row[0], "TMAX": row[1], "TMIN": row[2]}            
        for i in range(7):
            # try:
            #     my_dict_of_items[key_i_want_to_check]
            # except KeyError:
            #     # Do the operation you wanted to do for "key not present in dict".
            # else:
            if inputDate in dict.keys(dictData):
                print("found")
                data = dictData[inputDate]
                forecast.append(data)
            else :
                pastfound = False
                #get past year data.. if not available, then generate random
                tempDate = datetime.strptime(inputDate, "%Y%m%d").date()
                currentYear = int(tempDate.year)
                print(currentYear)
                if(currentYear >= 2013) :
                    year = 2013
                    dummyDate = date(year, tempDate.month, tempDate.day)
                    dummyDateFormatted = dummyDate.strftime("%Y%m%d")
                    print(dummyDate)
                    while (dummyDateFormatted not in dict.keys(dictData)) and year<2019:
                        year+=1
                        dummyDate = date(year, tempDate.month, tempDate.day)
                        dummyDateFormatted = dummyDate.strftime("%Y%m%d")
                    data = {"DATE":  inputDate, "TMAX": dictData[dummyDateFormatted]["TMAX"], "TMIN": dictData[dummyDateFormatted]["TMIN"]}
                    forecast.append(data)
                    print(data)
                    pastfound = True
                if (not pastfound) or (currentYear < 2013) :
                    tempDate = datetime.strptime(inputDate, "%Y%m%d").date()
                    index = random.randint(0,6)
                    month = int(tempDate.month)
                    if month > 9  and month < 3 : #JAN 0, FEB 1, MAR 2, NOV 10, DEC 11
                        data = {"DATE":  inputDate, "TMAX": sampleColdMaxData[index], "TMIN": sampleColdMinData[index]}
                        forecast.append(data)
                    elif month == 3 or month == 8 or month == 9 : #APR, SEP, OCT
                        data = {"DATE":  inputDate, "TMAX": sampleModMaxData[index], "TMIN": sampleModMinData[index]}
                        forecast.append(data)
                    elif month >=4 and month < 8 : #4,5,6,7 : MAY, JUN, JUL, AUG
                        data = {"DATE":  inputDate, "TMAX": sampleHotMaxData[index], "TMIN": sampleHotMinData[index]}
                        forecast.append(data)        
            # inputdate++
            tempDate = datetime.strptime(inputDate, "%Y%m%d").date()
            tempDate += timedelta(days=1)
            inputDate = tempDate.strftime("%Y%m%d")
        return make_response(jsonify(forecast), 200)
    else :
        return make_response(jsonify({'error': 'Invalid Date'}), 400)

# abort(400)
@app.errorhandler(404)
def notFound(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(405)
# make_response(jsonify({'error': 'Method Not Found'}), 405)
def methodNotFound(error):
    home = "Check Weather Information using the following Resources: \n/historical/ - GET, POST\n/historical/[date] - GET, DELETE\n/forecast/[date] - GET\n"
    return make_response(jsonify({'error': 'Method Not Found\n{home}'}), 405)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)