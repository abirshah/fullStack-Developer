from gpiozero import LED, Button, MotionSensor
import time
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import os


HOST = '127.0.0.1'
PORT = 4000
green_led = LED(4)
red_led = LED(22)
blue_led = LED(26)
motion_detector = MotionSensor(12)

timestamp = time.strftime("%y%b%d_%H:%M:%S")
print("System activated at " + timestamp)

green_led.off()
red_led.on()
blue_led.off()


def open_door():
    print("Door Opening for 10 seconds")
    red_led.off()
    green_led.on()
    time.sleep(10)
    green_led.off()
    red_led.on()
    

def sense_motion():
    while True:
        motion_detector.wait_for_motion() 
        timestamp = time.strftime("%y%b%d_%H:%M:%S")
        print("Motion Detector Triggered " + timestamp)
        time.sleep(0.8)
        sense_motion()
    

class RP_Server(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))


    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_data = post_data.split('=')[1]
        if post_data == 'open':
            open_door()
            print("Door Opened")
        self.do_GET()
        

# Run Server
os.popen('sh /home/pi/capstone/fullStack-Developer/RasberryPi/LaunchVideoStream.sh')
print("Streaming video from Pi Cam")
print("Running server on RasberryPI")
server = HTTPServer((HOST, PORT), RP_Server)
server_thread = threading.Thread(target=server.serve_forever)
motion_sensor_thread = threading.Thread(target=sense_motion)

server_thread.start()
motion_sensor_thread.start()
