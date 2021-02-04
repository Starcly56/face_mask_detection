from gpiozero import LED
from time import sleep

green = LED(14)
red = LED(15)


while True:
    green.off()
    red.on()
    sleep(1)
    red.off()
    green.on()
    sleep(1)
