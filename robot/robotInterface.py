import create2api
import sys
import socket
import sys
sys.path.insert(0, '/home/pi/snowboy/examples/Python')
import snowboydecoder
import signal
import speech_recognition as sr
import os

# Initialize our socket to recieve commands
##sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
##sock.bind(('', 9999))
##sock.listen(1)
##print("Listening for connections...")

# Create out bot connection
bot = create2api.Create2()
bot.digit_led_ascii('    ')  # clear DSEG before Off mode
bot.start()


interrupted = False

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

##try:
##	while True:
##		conn, addr = sock.accept()
##		print("Connected " + str(addr[0]) + ":" + str(addr[1]))
##
##		while True:
##			try:
##				data = conn.recv(1024).decode()
##			except Exception:
##				break
##			if data:
##				print(data)
##			else:
##				break
##			if data[0:2] == "MO":
##				# We are moving
##				direction = data[2:data.index("S")]
##				speed = data[data.index("S")+1:]
##				sendCmd(direction, int(speed))
##
##			elif data[0:2] == "MD":
##				# We are changing modes
##				mode = data[2:]
##				changeMode(mode)
##
##		print("Disconnected " + str(addr[0]) + ":" + str(addr[1]))
##		conn.close()
##		bot.stop()
##
##except Exception:
##	print("Socket terminated")
##	sock.shutdown(socket.SHUT_RDWR)
##	sock.close()
def audioRecorderCallback(fname):
    print "converting audio to text"
    r = sr.Recognizer()
    with sr.AudioFile(fname) as source:
        audio = r.record(source)  # read the entire audio file
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        resp = r.recognize_google(audio)
        print(r.recognize_google(audio))
        if resp == "clean":
                bot.clean()
        elif resp == "stop":
                bot.stop()
    except sr.UnknownValueError:
        print "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        print "Could not request results from Google Speech Recognition service; {0}".format(e)

    os.remove(fname)



def detectedCallback():
    bot.play_test_sound()
    sys.stdout.write("recording audio...")
    sys.stdout.flush()

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) == 1:
    print "Error: need to specify model name"
    print "Usage: python demo.py your.model"
    sys.exit(-1)

model = sys.argv[1]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.38)
print "Listening... Press Ctrl+C to exit"

# main loop
detector.start(detected_callback=detectedCallback,
               audio_recorder_callback=audioRecorderCallback,
               interrupt_check=interrupt_callback,
               sleep_time=0.01)

detector.terminate()
bot.stop()
