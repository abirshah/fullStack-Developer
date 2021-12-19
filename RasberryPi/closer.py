from gpiozero import LED


green_led = LED(4)
red_led = LED(22)
blue_led = LED(26)


def close_lights():
    green_led.off()
    red_led.off()
    blue_led.off()


close_lights()

    