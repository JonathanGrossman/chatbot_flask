import json
from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_cors import CORS
from datetime import datetime
import sqlite3

app = Flask(__name__)
CORS(app)


@app.route("/<message>", methods=['GET', 'POST'])
def message_handler(message):
    if request.method == "POST":
        print(message)
    return message


if __name__ == "__main__":
    app.run(host="localhost", port=7000, debug=True)
