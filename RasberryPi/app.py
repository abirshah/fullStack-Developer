from gpiozero import LED, Button, MotionSensor
import time
import sys
import threading
import os
from flask import Flask, redirect, url_for, render_template
import urllib.request


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
    time.sleep(5)
    green_led.off()
    red_led.on()
    

def sense_motion():
    while True:
        motion_detector.wait_for_motion() 
        timestamp = time.strftime("%y%b%d%H%M%S")
        print("Motion Detector Triggered " + timestamp)
        try:
            urllib.request.urlopen("http://192.168.0.56:8000/motion/" + timestamp)
        except:
            print("Error sending motion detection timestamp")
        time.sleep(0.8)
        sense_motion()
    

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/open.html')
def open():
    open_door()
    return render_template('index.html')


@app.route('/submitbutton', methods=['POST'])
def submitbutton():
    open_door()
    return render_template('index.html')


#os.popen('sh /home/pi/capstone/fullStack-Developer/RasberryPi/LaunchVideoStream.sh')
#print("Streaming video from Pi Cam")
#print("Running server on RasberryPI")
motion_sensor_thread = threading.Thread(target=sense_motion)
motion_sensor_thread.start()

#app.run(host='192.168.0.42', port=5000)
app.run(debug=True, port=5000)
