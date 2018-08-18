from flask import Flask, render_template, request, redirect, Response, session, abort
import random, json
import sys
import socket

app = Flask(__name__)

app.secret_key = 'X;\xce\xcc\xde\x8f.\x117\x16tO\xfd\x98\n<'

# The local IP and Port of the socket server on the bot
HOST = "192.168.0.55"
PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False

def connect():
	if not connected:
		try:
			sock.connect((HOST, PORT))
			print("Connection with bot established.")
			return True
		except Exception:
			print("Failed to connect to bot.")
			return False
	return True


def relay(msg):
	if connected:
		try:
			print("Command sent")
			sock.send(msg.encode())
		except Exception:
			print("Failed to send command")
			connected = False


@app.route("/")
def index():
	if not session.get('logged_in'):
		# Return the log in page
		return render_template('login.html')
	else:
		# Return our main page
		return render_template('index.html')


@app.route("/login", methods = ['POST', 'GET'])
def do_login():
	if request.method == 'POST':
		if request.form['password'] == 'password' and request.form['username'] == 'admin':
			session['logged_in'] = True
		else:
			flash('Wrong Password!')
		return index()
	return render_template('login.html')

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


# Return the status of the connection with the bot
@app.route("/getStatus", methods = ['GET'])
def returnStatus():
	connected = connect()
	currMode = json.dumps({"status": str(connected)})

	return currMode


if __name__ == "__main__":
	connected = connect()
	app.run("0.0.0.0", "8000")
