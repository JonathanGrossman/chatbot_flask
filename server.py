import json
from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_cors import CORS
from datetime import datetime
import sqlite3

app = Flask(__name__)
CORS(app)


connection = sqlite3.connect( ":memory:" )
cursor = connection.cursor()
sql_command = """CREATE TABLE messages (
                    message VARCHAR(300));"""
cursor.execute(sql_command)
cursor.execute("INSERT INTO messages VALUES ('hello')")
cursor.execute("SELECT * FROM messages")
results = cursor.fetchall()

@app.route("/", methods=['GET'])
def hello_handler():
    return render_template('index.html')


@app.route("/message/", methods=['GET', 'POST'])
def message_handler():
    global results
    if request.method == "POST":
        user_input = request.args.get("message")
        print(user_input)
        for m in results:
            print(m[0])
            if m[0] == user_input:
                response_message = {"message": "I've already answered that one."}
            else:
                response_message = {"message": "What did you say?"}
        return jsonify(response_message)


if __name__ == "__main__":
    app.run(host="localhost", port=7000, debug=True)
