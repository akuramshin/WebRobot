from flask import Flask, render_template, request, redirect, Response
import random, json
import create2api
import sys

app = Flask(__name__)
bot = create2api.Create2()

bot.digit_led_ascii('    ')  # clear DSEG before Off mode
bot.start()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/move", methods = ['POST'])
def recieve():
    # read the JSON data recieved
    data = request.get_json()

    direction = str(data['Data']['direction'])
    speed = str(data['Data']['speed'])
    sendCmd(direction, speed)
        
    return "JSON posted"

if __name__ == "__main__":
    app.run("0.0.0.0", "8000")

def sendCmd(dir, speed):
	if dir == "forward":
		bot.drive(speed, 32767)
	elif dir == "backward":
		bot.drive(speed*-1, 32767)
	elif dir == "right":
		bot.drive(speed, -1)
	elif dir == "left":
		bot.drive(speed, 1)
	else:
		bot.drive(0, 32767)
