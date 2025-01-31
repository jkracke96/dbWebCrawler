import stringConverter
import datetime
import requests
from bs4 import BeautifulSoup
from datetime import datetime


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


def getHTMLText(station):
    URL = "https://dbf.finalrewind.org/{placeholder}"
    resp = requests.get(URL.format(placeholder=station)).text
    soup = BeautifulSoup(resp, "html.parser")
    elements = soup.find(class_="cancelled")

    # get connection information
    for elem in elements:
        origin = elem.parent.get("data-from")

        # continue when station is origin
        if origin == station:
            continue

        arrival_time = elem.parent.get("data-arrival")
        link = elem.parent.find("a").get("href")
        break

    # get departure
    if link:
        link = URL.format(placeholder=link[1:])
        resp = requests.get(link).text
        soup = BeautifulSoup(resp, "html.parser")
        elements = soup.find(class_="time-sched")
        for elem in elements:
            departure_time = elem
    else:
        return None

    datetime.today().strftime('%Y-%m-%d')
    result = {
        "date": datetime.today().strftime('%d.%m.%y'),
        "origin": origin,
        "departure": departure_time,
        "destination": station,
        "arrival": arrival_time
    }
    return result


if __name__ == "__main__":
    print(getHTMLText("Frankfurt(Main)Hbf"))
