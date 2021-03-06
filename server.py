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

response_message = {"message": "What did you say?"}
# urls = ['https://boto20.herokuapp.com/message/?message=', 'https://morning-basin-34003.herokuapp.com/message/?message=', 'https://ancient-fjord-32267.herokuapp.com/message/?message=', 'https://randobot-5000.herokuapp.com/message/?message=', 'https://peaceful-stream-36739.herokuapp.com/?message=zohar']
urls = [{"url": 'https://boto20.herokuapp.com/message/?message=', "name": "Zohar"}, {"url": 'https://morning-basin-34003.herokuapp.com/message/?message=', "name": "Raz"}, {"url": 'https://ancient-fjord-32267.herokuapp.com/message/?message=', "name": "Gabe"}, {"url": 'https://randobot-5000.herokuapp.com/message/?message=', "name": "Jonathan"}, {"url": 'https://peaceful-stream-36739.herokuapp.com/?message', "name": "Jack"}]


connection = sqlite3.connect("database.db")
cursor = connection.cursor()


def time_function():
    time_message = ""
    now = datetime.utcnow()
    seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    rounded = round((86400 - seconds_since_midnight) / 60)
    if seconds_since_midnight != 0:
        return "Sent at " + str(now) + ", which is " + str(rounded) + " minutes until midnight (UTC). At midnight UTC, I ping a random bot and return its message here."
    else:
        random_number_urls = randrange(5)
        url = urls[random_number_urls]["url"]
        response = requests.get(url + "hi")
        json_string = json.loads(response.content)
        return "It's midnight! " + urls[random_number_urls]["name"] + " says " + json_string["message"]


scheduler = BackgroundScheduler()
job = scheduler.add_job(time_function, 'interval', minutes=1)
scheduler.start()  


@app.route("/", methods=['GET'])
def home_handler():
    return render_template("index.html")

@app.route("/database", methods=['GET'])
def get_database_messages():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM messages")
    results = cursor.fetchall()
    message_array = []
    for message in results:
        if message[0] != "undefined" and message[0] != "null":
            message_array.append(message[0])
    return jsonify({ "database_messages": message_array})


@app.route("/message/", methods=['GET'])
def message_handler():
    global response_message
    
    random_number = randrange(11)
    random_number_urls = randrange(5)
    url = urls[random_number_urls]["url"]
    
    if request.method == "GET":
        remote_address = request.environ["REMOTE_ADDR"]
        remote_port = request.environ["REMOTE_PORT"]
        user_input = request.args.get("message")
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM messages")
        results = cursor.fetchall()
        if user_input not in (item[0] for item in results):
            cursor.execute('INSERT INTO messages VALUES (?)', ([user_input]))
            connection.commit()     
        if random_number == 2:
            response = requests.get(url + user_input)
            json_string = json.loads(response.content)
            response_message = {"message": json_string["message"], "message_origin": "A message from: " + urls[random_number_urls]["name"], "sender_address": remote_address, "sender_port": remote_port, "time": time_function()}
        else:
            if user_input not in (item[0] for item in results):
                response_message = {"message": "What did you say?", "message_origin": "A message from this bot.", "sender_address": remote_address, "sender_port": remote_port, "time": time_function()}
            else:
                response_message = {"message": "I've already answered that one.", "message_origin": "A message from this bot.", "sender_address": remote_address, "sender_port": remote_port, "time": time_function()}
        return jsonify(response_message)

if __name__ == "__main__":
    app.run(host="localhost", port=7000, debug=True, use_reloader=False)
 
