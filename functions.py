import json
import extractData
from pymongo_connect import MongoDB


def getCancelledConnection(station):
    # get html result based on custom url and find the connection block with the first cancelled connection
    # loop, if no cancellation was found
    output = extractData.getHTMLText(station)

    if output is None:
        return "Sorry, no cancelled connection was found"

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

