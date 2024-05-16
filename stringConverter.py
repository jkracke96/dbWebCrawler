def convertString(phrase):
    current = ["&#x0028;", "&#x0029;", "&#228;", "&#246;", "&#252;", "\\u00F6", "(Halt entfaellt)", "&#223;"]
    replacer = ["(", ")", "ae", "oe", "ue", "oe", "", "ß"]
    for i in range(len(current)):
        phrase = phrase.replace(current[i], replacer[i])
    return phrase


def convertDate(date):
    year = date[2:4]
    month = date[5:7]
    day = date[8:10]
    date = f"{day}.{month}.{year}"
    return date
