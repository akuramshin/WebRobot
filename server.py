from flask import Flask, render_template, request, redirect, Response
import random, json
import create2api
import sys

app = Flask(__name__)
bot = create2api.Create2()

bot.digit_led_ascii('    ')  # clear DSEG before Off mode
bot.start()

def sendCmd(dir, speed):
        speed = 250
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

def changeMode(mode):
	if mode == "Off":
		bot.digit_led_ascii('    ')  # clear DSEG before Off mode
		bot.stop()
	elif mode == "Passive":
		bot.digit_led_ascii('    ')  # clear DSEG before Passive mode
		bot.start()
	elif mode == "Safe":
		bot.safe()
	elif mode == "Full":
		bot.full()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/move", methods = ['POST'])
def recieve():
    # read the JSON data recieved
    data = request.get_json()

    direction = str(data['Data']['direction'])
    speed = str(data['Data']['speed'])
    sendCmd(direction, int(speed))
        
    return "Robot moved"

@app.route("/mode", methods = ['POST'])
def rec():
	# read the JSOn data recieved
	data = request.get_json()

	mode = str(data['Data']['mode'])
	changeMode(mode)

	return "Mode changed"

if __name__ == "__main__":
    app.run("0.0.0.0", "8000")

