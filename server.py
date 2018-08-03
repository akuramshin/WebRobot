from flask import Flask, render_template, request, redirect, Response
import random, json
import sys
import socket

app = Flask(__name__)
# Add a feature to index.html where we can see if bot is connected or not ...
# (if the socket client connected with the server running on the bot )

HOST = "192.168.0.55"
PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False

def connect():
	try:
		sock.connect((HOST, PORT))
		print("Connection with bot established.")
		return True
	except Exception:
		print("Failed to connect to bot.")
		return False


def relay(msg):
	if connected:
		sock.send(msg.encode())


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
    relay("MO" + direction + "S" + speed)
        
    return "Robot moved"


@app.route("/mode", methods = ['POST'])
def rec():
	# read the JSON data of the new mode
	data = request.get_json()

	mode = str(data['Data']['mode'])
	relay("MD" + mode)

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
	connected = connect()
	app.run("0.0.0.0", "8000")
