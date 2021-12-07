from gpiozero import LED, Button, MotionSensor
from picamera import PiCamera
from time import sleep, pause

GPI.setmode(GPIO.BCM)
green_led = LED(4)
red_led = LED(22)
white_led = LED(26)
motion_detector = MotionSensor(12)
camera = PiCamera()
camera.resolution = (640, 480)
filename = "home/pi/Desktop/motion capture " + (time.strftime("%y%b%d_%H:%M:%S")) + ".jpg"

while True:
    motion_detector.wait_for_motion()
    print("Motion Detector Triggered")
    white.on()
    camera.capture(filename)
    camera.start_preview()
    sleep(5)
    camera.stop_preview()


