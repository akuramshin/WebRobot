import create2api
import socket

# Initialize our socket to recieve commands
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 9999))
sock.listen(1)

# Create out bot connection
bot = create2api.Create2()
bot.digit_led_ascii('    ')  # clear DSEG before Off mode
bot.start()

try:
	while True:
		conn, addr = sock.accept()
		print("Connected " + addr[0] + ":" + addr[1])

		while True:
			try:
				data = conn.recv(1024).decode()
			except Exception:
				break;
			print(data)
			if data[0:2] == "MO":
				# We are moving
				print(data)
			elif data[0:2] == "MD":
				# We are changing modes
				print(data)
		print("Disconnected " + addr[0] + ":" + addr[1])
		conn.close()

except Exception:
	sock.shutdown(socket.SHUT_RDWR)
    sock.close()

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