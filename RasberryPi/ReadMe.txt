RasberryPI and hardware details

The RasberryPI is connected to three lights, blue, red and green.

The green and red lights represent the door being unlocked or locked, respectively.

When the electrical system is complete, its drivers or relays can be connected in place of the lights, for electro-mechanical control of the door

The blue light is turned on any time that the camera is activated.



Please refer to the video at this link for a demo of the files in this folder.

https://www.youtube.com/watch?v=Pl2zvEAlqzU


The video demonstrates:

SN-114 - As a developer, I want the system to equip with a motion detection sensor, so the user doesn’t need to manually start the system.

SN-121 - As a developer, I want the pet door sensor to be active for 10 seconds when it detects an owner’s pet so that the system can process the signal to open the door.

SN-166 Rasberry Pi needs to send and receive signals to and from the backend (https://www.youtube.com/watch?v=xEFoWv2WPZY&t=4s&ab_channel=Mike%3APlatinumAudio)

SN-167 Raspberry Pi needs to stream video to the backend (Demo is uploading...)


Endpoints:
Backend: 127.0.0.1:8000 --> 192.0.0.56:8000
Raspberry PI GPIO: 192.168.0.42:5000
Raspberry PI Cam Stream: 192.168.0.42:3000



Door Access
WebService/app.py open_door() --> RaspberryPi:5000/open

Motion Detection
RaspberryPi:5000 --> 127.0.0.1:8000/motion WebService/app.py

Video Stream
RaspberryPi:3000 --> WebService/camera.py cv2.CamVideoStream()
