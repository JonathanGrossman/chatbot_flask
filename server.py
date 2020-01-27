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
result = cursor.fetchall()


@app.route("/", methods=['GET'])
def hello_handler():
    return render_template('index.html')


@app.route("/message/", methods=['GET', 'POST'])
def message_handler():
    if request.method == "POST":
        print(request.args.get("message")) 
        for m in result:
            print(m)
        #     if m == message:
        #         response_message = "You already asked me that."
        #     else:
        #         response_message = "What?"
        return jsonify({"response": "hi"})


if __name__ == "__main__":
    app.run(host="localhost", port=7000, debug=True)
