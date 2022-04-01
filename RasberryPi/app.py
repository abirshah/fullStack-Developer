from gpiozero import LED, Button, MotionSensor
import time
import sys
import threading
import os
from flask import Flask, redirect, url_for, render_template
import urllib.request

LocalHostIp = "127.0.0.1"
RasPiIp = "169.254.235.178"
RasPiPort = "5000"
BackendServerIp = "169.254.135.232"
BackendServerPort = "8000"
RasPiHomepage = "index.html"
green_led = LED(4)
red_led = LED(22)
blue_led = LED(26)
motion_detector = MotionSensor(12)
green_led.off()
red_led.on()
blue_led.off()
timestamp = time.strftime("%y%b%d%H%M%S")
print("System activated at " + timestamp)


app = Flask(__name__)

def open_door():
    print("Door Opening for 10 seconds")
    red_led.off()
    green_led.on()
    time.sleep(10)
    green_led.off()
    red_led.on()
    

def sense_motion():
    while True:
        blue_led.off()
        motion_detector.wait_for_motion() 
        timestamp = time.strftime("%y%b%d%H%M%S")
        print("Motion Detector Triggered " + timestamp)
        try:
            urllib.request.urlopen("http://169.254.135.232:8000/motion/" + timestamp)
        except Exception as e:
            print("Error sending motion detection timestamp")
            print("http://" + BackendServerIp +":"+ BackendServerPort + "/motion/" + timestamp)
        blue_led.on()
        time.sleep(10.0)
        blue_led.off()
    

@app.route('/')
def index():
    return render_template(RasPiHomepage)


@app.route('/open.html')
def open():
    open_door()
    return render_template(RasPiHomepage)


@app.route('/submitbutton', methods=['POST'])
def submitbutton():
    open_door()
    return render_template(RasPiHomepage)


# Start Network Video Stream
os.popen('sh /home/pi/capstone/fullStack-Developer/RasberryPi/LaunchVideoStream.sh')
print("Streaming video from Pi Cam")
print("Running server on RaspberryPI")
motion_sensor_thread = threading.Thread(target=sense_motion)
motion_sensor_thread.start()

app.run(host=RasPiIp, port=RasPiPort)

