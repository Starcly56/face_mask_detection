# Programmed By Ujjwal Humagain
# Date of Completion 11 February 2021
# Copyright (c) 2021 Ujjwal Humagain
#Importing file for servocontrolling function
import servocontrol


#Function for unlocking the door
def unlock():
    try: 
        print("Unlocking door...")
        #setting angle at 180
        servocontrol.SetAngle(180)
        print("Door is unlocked")
        return "Door is unlocked"
    except:
        print("The door was not correctly unlocked")
    
#Function for locking the door    
def lock():
    try:
        print("Locking door...")
        #setting angle at 0
        servocontrol.SetAngle(0)
        print("Door is locked")
        return "Door is locked"
    except:
        print("The door was not correcly locked")