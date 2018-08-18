import create2api
import socket

# Initialize our socket to recieve commands
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 9999))
sock.listen(1)
print("Listening for connections...")

# Create out bot connection
bot = create2api.Create2()
bot.digit_led_ascii('    ')  # clear DSEG before Off mode
bot.start()


def sendCmd(dir, speed):
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

try:
	while True:
		conn, addr = sock.accept()
		print("Connected " + str(addr[0]) + ":" + str(addr[1]))

		while True:
			try:
				data = conn.recv(1024).decode()
			except Exception:
				break
			if data:
				print(data)
			else:
				break
			if data[0:2] == "MO":
				# We are moving
				direction = data[2:data.index("S")]
				speed = data[data.index("S")+1:]
				sendCmd(direction, int(speed))

			elif data[0:2] == "MD":
				# We are changing modes
				mode = data[2:]
				changeMode(mode)

		print("Disconnected " + str(addr[0]) + ":" + str(addr[1]))
		conn.close()
		bot.stop()

except Exception:
	print("Socket terminated")
	sock.shutdown(socket.SHUT_RDWR)
	sock.close()
