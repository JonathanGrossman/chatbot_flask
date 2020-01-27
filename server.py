import json
from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_cors import CORS
from datetime import datetime
import simplejson as json
import requests
import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler
from random import randrange


app = Flask(__name__)
CORS(app)

urls = ['https://boto20.herokuapp.com/message/?message=', 'https://morning-basin-34003.herokuapp.com/message/?message=']

connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM messages")
results = cursor.fetchall()

def time_function():
    time_message = ""
    now = datetime.now()
    seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    if seconds_since_midnight != 0:
        print(str(seconds_since_midnight) + " seconds until midnight")
    else:
        print("It's midnight!")

scheduler = BackgroundScheduler()
job = scheduler.add_job(time_function, 'interval', minutes=1)
scheduler.start()

@app.route("/", methods=['GET'])
def hello_function(): 
    return redirect(url_for("message_handler"))

@app.route("/message/", methods=['GET'])
def message_handler():
    random_number = randrange(11)
    random_number_urls = randrange(2)
    url = urls[random_number_urls]

    if request.method == "GET":
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM messages")
        results = cursor.fetchall()
        user_input = request.args.get("message")

        if random_number == 2:
            r = requests.get(url + user_input)
            json_string = json.loads(r.content)
            response_message = {"message": json_string["message"]}
        else:
            for m in results:
                if m[0] == user_input:
                    response_message = {"message": "I've already answered that one."}
                else:
                    cursor.execute("INSERT INTO messages VALUES (?)", ([user_input]))
                    response_message = {"message": "What did you say?"}
        return jsonify(response_message)


if __name__ == "__main__":
    app.run(host="localhost", port=7000, debug=True, use_reloader=False)
 
