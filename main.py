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
left_motor_a = Motor(Ports.PORT8)
left_motor_b = Motor(Ports.PORT9)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT20)
right_motor_b = Motor(Ports.PORT19)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)

# initalize 
wait(30, MSEC)



def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here

def user_control():
    brain.screen.clear_screen()
    brain.screen.print("driver control")
    # place driver control in this while loop
    while True:
        wait(20, MSEC)

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()
controller.rumble("...")