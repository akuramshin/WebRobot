# WebRobot

Website interface to controll the Create 2 iRobot through the net with a livestream. This allows for easy, modular updates that can be implemented offline with instant access anywhere.

I have currently implemented two different setups for this system. The original implementation has the server running on the raspberry pi itself along with the iRobot interfacing code. The second setup allows for the server to be hosted on a seperate machine on the same network that then communicates with the raspberry pi on the robot via socket servers.

Equipment Used:
 - Create 2 iRobot:  Lots of documentation and easy to work with. The robot hardware you use is the least important part.
 - Raspberry Pi 3: Very powerfull for size and has wifi built into the board. Very reliable, safe option. Try to choose something that can    handle multiple processes at once, the video streaming is quite intensive. 
 - Webcam: I used an old webcam I had. This part is also not very important, depends on your quality preference and how much processing      power you have. A better quality image will strain your onboard hardware, but you can always scale the quality down with OpenCV.
 - Phone Power bank: I used a small 3000 mAh power bank. This is used to power the raspberry pi (and inturn, webcam), try to choose          something with larger capacity (5000 mAh +), the voltage output from phone banks is usually 5V which is enough for us. 
 - I used motion for the live stream of the webcam.

TODO bug fixes: 
 -  Add a time limit between movement commands? ~0.2 seconds
 -  Possibly make the image reload as soon as connection established?
 -  What if the robot disconnects? We need to update indicator? Or just refresh page?
 
 TODO Long term:
  - Intergrate voice activation/commands (google home/alexa but portable)
  - Wire up a way to charge raspberry pi powerbank from the iRobot's onboard battery
