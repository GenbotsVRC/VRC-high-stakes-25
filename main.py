# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       1053730                                                      #
# 	Created:      1/25/2025, 7:13:27 AM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

brain = Brain()

controller = Controller()

clamp = Motor(Ports.PORT10)
intake = Motor(Ports.PORT11)
train = Motor(Ports.PORT6)
leftA = Motor(Ports.PORT8)
leftB = Motor(Ports.PORT9)
left = MotorGroup(leftA, leftB)
rightA = Motor(Ports.PORT20)
rightB = Motor(Ports.PORT19)
right = MotorGroup(rightA, rightB)
drivetrain = DriveTrain(left, right, 319.19, 295, 40, MM, 1)

# initalize 
wait(30, MSEC)

############################## AUTON (PARTITION) ##############################
def auton():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here

############################## MOTOR FUNCTIONS ##############################
def testing():
    controller.rumble(".")
    brain.screen.print("ihe")

############################## CALLBACKS ##############################
controller.buttonA.pressed(testing)

def user_control():
    brain.screen.clear_screen()
    brain.screen.print("driver control")

    
    


    # place something in while loop (unclear)
    # i believe drive settings
    while True:
        wait(20, MSEC)
        

# create competition instance
comp = Competition(user_control, auton)

# actions to do when the program starts

controller.rumble("...")