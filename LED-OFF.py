#in case LEDs get stuck in the on position
#   this turns LEDs off

from gpiozero import LED
from time import sleep

green = LED(14)
red = LED(15)

red.off()
green.off()
sleep(1)
