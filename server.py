import json
from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_cors import CORS
from datetime import datetime
import simplejson as json
import requests
import sqlite3

app = Flask(__name__)
CORS(app)


connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM messages")
results = cursor.fetchall()
 

@app.route("/", methods=['GET'])
def hello_handler():
    return render_template('index.html')

@app.route("/message/", methods=['GET'])
def message_handler():
    if request.method == "GET":
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM messages")
        results = cursor.fetchall()
        user_input = request.args.get("message")
        if user_input == 'zohar':
                r = requests.get('https://boto20.herokuapp.com/message/?message=' + user_input)
                json_string = json.loads(r.content)
                response_message = {"message": json_string["message"]}
                return jsonify(response_message)
        else:
            for m in results:
                if m[0] == user_input:
                    response_message = {"message": "I've already answered that one."}
                else:
                    cursor.execute("INSERT INTO messages VALUES (?)", ([user_input]))
                    response_message = {"message": "What did you say?"}
            return jsonify(response_message)


if __name__ == "__main__":
    app.run(host="localhost", port=7000, debug=True)
