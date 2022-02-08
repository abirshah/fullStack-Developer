from gpiozero import LED, Button, MotionSensor
from picamera import PiCamera
import time
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler


#HOST = '192.168.0.43'  #RasberryPI wlan1
#HOST = '192.168.0.42'  #RasberryPI wlan0
HOST = '127.0.0.1'
PORT = 4000
green_led = LED(4)
red_led = LED(22)
blue_led = LED(26)
motion_detector = MotionSensor(12)
# camera = PiCamera()

timestamp = time.strftime("%y%b%d_%H:%M:%S")
image_format = ".jpg"
video_format = ".h264"
print("System activated at " + timestamp)

green_led.off()
red_led.on()
blue_led.off()
# camera.resolution = (640, 480)
# camera.vflip = True


def open_door():
    print("Door Opening for 10 seconds")
    red_led.off()
    green_led.on()
    time.sleep(10)
    green_led.off()
    red_led.on()
    
    
class RP_Server(BaseHTTPRequestHandler):

    def do_GET(self):
        print("Get block: " + str(self) )
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
print("Running server on RasberryPI")
server = HTTPServer((HOST, PORT), RP_Server)
server.serve_forever()


