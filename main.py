from flask import Flask, render_template, request
import functions
from pymongo_connect import MongoDB


# gcloud app deploy
# deploy cron jobs:  gcloud app deploy cron.yaml
# flask --app main  run

app = Flask(__name__)
app.secret_key = "MyKey123456789!"


@app.route("/")
def returnStart():
    return render_template('home.html', content="Hey, you can use this page to find cancelled train connections for "
                                                "several stations")


@app.route("/newCancellation")
def newCancellation():
    return render_template("new_cancellation1.html")


@app.route("/newCancellation", methods=['POST'])
def newCancellation_post():
    station = request.form['stations']
    response = functions.getCancelledConnection(station)
    try:
        return render_template("new_cancellation_output.html", date=response.get("date"), origin=response.get("origin"),
                               departure=response.get("departure"), destination=response.get("destination"),
                               arrival=response.get("arrival"))
    except:
        return render_template("new_cancellation_exception.html")


# Berlin%20Hbf%238011160
# Hamburg%20Hbf%238002549
@app.route("/findCancellation")
def my_form():
    return render_template("past_cancellation.html")


@app.route('/findCancellation', methods=['POST'])
def my_form_post():
    date = str(request.form['date'])
    station = request.form['stations']
    connection = MongoDB()
    try:
        response = connection.read_from_db(date, station)
        return render_template("past_cancellation_output.html", date=response.get("date"), origin=response.get("origin"),
                               departure=response.get("departure"), destination=response.get("destination"),
                               arrival=response.get("arrival"))
    except:
        return render_template("past_cancellation_exception.html")


@app.route("/dailySchedule")
def dailySchedule():
    functions.dailySearch()
    return ""


if __name__ == "__main__":
    app.run(debug=True)
