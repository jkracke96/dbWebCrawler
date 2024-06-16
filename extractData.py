import stringConverter
import datetime
import requests


def findBlock(htmlText):
    toFind = ">Fahrt f&#228;llt aus"
    foundAt = htmlText.find(toFind)
    # case when no cancelled connection was found
    if foundAt < 0:
        return -1
    else:
        i = foundAt

        while True:
            if htmlText[i-7:i] == "</span>" and htmlText[i-12:i-8] == "</a>":
                foundSpan = i
                break
            i = i-1
        departureStart = foundSpan + 8
        return departureStart


def findOrigin(htmlText, departureStart):
    i = departureStart
    while True:
        if htmlText[i] == "-" and htmlText[i - 4] == ":":
            departureTime = htmlText[i - 6:i - 1]
            originStation = htmlText[departureStart:i - 7]
            originStation = stringConverter.convertString(originStation)
            break
        i = i + 1
    return departureTime, originStation, i


def findDestination(htmlText, i):
    while True:
        if htmlText[i:i+5] == "</td>" or htmlText[i:i+5] == "<div ":
            arrivalTime = htmlText[i-6:i-1]
            j = i
            # find station
            while True:
                if htmlText[j] == "-" and htmlText[j-4] == ":":
                    finalDestination = htmlText[j+2:i-7]
                    finalDestination = stringConverter.convertString(finalDestination)
                    break
                j = j-1
            break
        i = i+1
    return arrivalTime, finalDestination


def getCurrentDateAndTime():
    weekdays = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
    date = str(datetime.date.today().strftime("%d.%m.%y"))
    day = datetime.date.today().weekday()
    dayName = weekdays[day]
    hour = datetime.datetime.now().strftime("%H")
    minute = datetime.datetime.now().strftime("%M")
    return date, dayName, hour, minute


def getHTMLText(station, date, hour, minute):
    # loop through html responses until a cancelled connection is found
    k = 0
    while True:
        # +2 für GCP +0 für local
        time = f"{int(hour) + 2 + k}:{minute}"

        # set up custom URL
        URL = f"https://reiseauskunft.bahn.de/bin/bhftafel.exe/" \
              f"dn?ld=43111&protocol=https:&rt=1&input={station}&" \
              f"boardType=arr&time={time}%2B60&productsFilter=11111&&&" \
              f"date={date}&&selectDate=&start=yes"
        print(URL)

        # get templates and find first cancelled train
        resp = requests.get(URL)
        htmlText = resp.text

        # find block with cancelled connection
        departureStart = findBlock(htmlText)
        if k == 8:
            return "Sorry, no cancelled connection was found"
        elif departureStart > 0:
            return htmlText, departureStart
        elif departureStart == -1:
            k = k + 1
