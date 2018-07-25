from flask import Flask, render_template, request, redirect, Response
import random, json
import sys

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/receiver", methods = ['POST'])
def recieve():
    # read the JSON data recieved
    data = request.get_json()

    direction = str(data['Data']['direction'])
    speed = str(data['Data']['speed'])

    print (direction + ":" + speed)    
    return "JSON posted"

if __name__ == "__main__":
    app.run("0.0.0.0", "8000")
