import json
import extractData
from pymongo_connect import MongoDB


def getCancelledConnection(station):
    # today's date and current time
    date = extractData.getCurrentDateAndTime()[0]
    hour = extractData.getCurrentDateAndTime()[2]
    minute = extractData.getCurrentDateAndTime()[3]

    # get html result based on custom url and find the connection block with the first cancelled connection
    # loop, if no cancellation was found
    htmlResponse = extractData.getHTMLText(station, date, hour, minute)

    if htmlResponse == "Sorry, no cancelled connection was found":
        return "Sorry, no cancelled connection was found"
    htmlText = htmlResponse[0]
    departureStart = htmlResponse[1]

    # find origin station
    originData = extractData.findOrigin(htmlText, departureStart)
    departureTime = originData[0]
    originStation = originData[1]
    i = originData[2]

    # find final destination
    destinationData = extractData.findDestination(htmlText, i)
    arrivalTime = destinationData[0]
    finalDestination = destinationData[1]

    output = {
        "date": date,
        "origin": originStation,
        "departure": departureTime,
        "destination": finalDestination,
        "arrival": arrivalTime
    }
    #firestoreConnect.writeToFirestore(output)
    connection = MongoDB()
    connection.write_to_db(output)
    return output


def dailySearch():
    file = open("stations.json")
    stations = json.load(file)
    keys = stations.keys()
    for key in keys:
        getCancelledConnection(stations[key][1])


if __name__ == "__main__":
    dailySearch()



#print(getCancelledConnection("K%F6ln%20Hbf%238000207"))
# Ffm: Frankfurt(Main)Hbf%238000105
    # Köln: K%F6ln%20Hbf%238000207
    # M%FCnchen%20Hbf%238000261

