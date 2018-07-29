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
		bot.drive(speed/2, -1)
	elif dir == "left":
		bot.drive(speed/2, 1)
	else:
		bot.drive(0, 32767)

def changeMode(mode):
	if mode == "Off":
		bot.digit_led_ascii('    ')  # clear DSEG 
		bot.stop()
	elif mode == "Passive":
		bot.digit_led_ascii('    ')  # clear DSEG 
		bot.start()
	elif mode == "Safe":
		bot.safe()
	elif mode == "Full":
		bot.full()
	elif mode == "Seek Dock":
		bot.digit_led_ascii('DOCK')  # clear DSEG before Passive mode (Seek dock goes into passive mode)
		bot.start()
		bot.seek_dock()

@app.route("/")
def index():
	# Return our main page
    return render_template('index.html')

@app.route("/move", methods = ['POST'])
def recieve():
    # read the JSON data of the direction and speed issued
    data = request.get_json()

    direction = str(data['Data']['direction'])
    speed = str(data['Data']['speed'])
    sendCmd(direction, int(speed))
        
    return "Robot moved"

@app.route("/mode", methods = ['POST'])
def rec():
	# read the JSON data of the new mode
	data = request.get_json()

	mode = str(data['Data']['mode'])
	changeMode(mode)

	return "Mode changed"

"""
@app.route("/getMode", methods = ['GET'])
def returnMode():
	# Get the current mode of the bot
	if bot.sensor_state['oi mode'] == bot.config.data['oi modes']['OFF']:
		mode = "off"
	elif bot.sensor_state['oi mode'] == bot.config.data['oi modes']['PASSIVE']:
		mode = "passive"
	elif bot.sensor_state['oi mode'] == bot.config.data['oi modes']['SAFE']:
		mode = "safe"
	elif bot.sensor_state['oi mode'] == bot.config.data['oi modes']['FULL']:
		mode = "full"
	else:
		mode = "none"
	
	# Create JSON data object with the current mode
	currMode = json.dumps({"mode": mode})

	return currMode
"""

if __name__ == "__main__":
    app.run("0.0.0.0", "8000")

