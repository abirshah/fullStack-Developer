from gpiozero import LED, Button, MotionSensor
from picamera import PiCamera
import time
import sys
import io


green_led = LED(4)
red_led = LED(22)
blue_led = LED(26)
motion_detector = MotionSensor(12)
camera = PiCamera()

timestamp = time.strftime("%y%b%d_%H:%M:%S")
image_format = ".jpg"
video_format = ".h264"
print("System activated at " + timestamp)

green_led.off()
red_led.off() #Turn on when not in development mode
blue_led.off()
camera.resolution = (640, 480)
camera.vflip = True


def open_door():
    print("Door Opening for 10 seconds")
    red_led.off()
    green_led.on()
    time.sleep(10)
    green_led.off()
    red_led.on()
    red_led.off()   #Delete when not in development mode
    
    
def record_video(time_of_video):
    blue_led.on()
    camera.start_recording("video" + time_of_video + video_format)
    time.sleep(3)
    camera.stop_recording()
    blue_led.off()
    

def capture_image(time_of_capture):
    blue_led.on()
    camera.capture(str("capture" + time_of_capture + image_format))
    blue_led.off()


def exit_sequence():
    print("Exiting program")
    sys.exit()
    
    
# with pynput.keyboard.Listener(on_press = exit_sequence) as listener:
#     listener.join
    
def stream_video():
    print("camera streaming for 6 seconds")
    stream = io.BytesIO()
    blue_led.on()
    camera.start_recording(stream, format = "h264", quality = 20)
    camera.wait_recording(6)
    camera.stop_recording()
    blue_led.off()
    
    
# add exit if an key pressed
def main():
    while True:
        red_led.on()
        motion_detector.wait_for_motion() 
        timestamp = time.strftime("%y%b%d_%H:%M:%S")
        print("Motion Detector Triggered " + timestamp)
        camera.start_preview()
        capture_image(timestamp)
        record_video(timestamp)
        camera.stop_preview()
        red_led.off()
     
     
def test_door():
    print("Testing door")
    print("Door access will be active for 10 seconds")
    open_door()
    

def test_stream_video():
    print("Testing video stream")
    stream_video()
    

# test_door()
test_stream_video()
main()


