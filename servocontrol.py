#Importing necessary packages
import RPi.GPIO as GPIO
from time import sleep

#Setting up the GPIO mode and the output. 
GPIO.setup(17, GPIO.OUT)
pwm=GPIO.PWM(17, 50)
pwm.start(0)

#Function to automatically rotate to a set angle
def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(17, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(17, False)
    pwm.ChangeDutyCycle(0)