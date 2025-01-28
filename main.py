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

############################## AUTON ##############################
def auton():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here

############################## MOTOR FUNCTIONS ##############################
"""
We need to have functions for the following:
CLAMP - manual lower/raise
CLAMP - bool trigger
TRAIN - bool trigger
INTAKE - bool trigger
COLLECTIONS (TRAIN + INTAKE) - start/stop
"""


def initialize():
    drivetrain.set_stopping(BRAKE) # Stopping Stops
    clamp.set_velocity(30, PERCENT) # Define the speed to run our motors
    intake.set_velocity(50, PERCENT)
    train.set_velocity(100, PERCENT)
    clamp.set_stopping(HOLD) # Clamp will actually hold

intakeRolling = 0
trainRunning = 0

def clamp_lower():
    pass

def clamp_raise():
    pass

# bool - autotrack clamp movement
# ! HANDLE MANUAL MOVEMENT IN CLAMPDOWN VARIABLE (TRACK POSITION?)
def clamp_trigger():
    pass

def train_trigger():
    pass

def intake_trigger():
    pass

def collections_trigger():
    pass



def rollIntake(): # Turn on intake for rings
    global intakeRolling
    if intakeRolling:
        intake.stop()
        intakeRolling = 0
    else: 
        intake.spin(FORWARD)
        intakeRolling = 1

def trainRun(): # Move the conveyor to put intaken rings on goals
    global trainRunning
    if trainRunning:
        train.stop()
        trainRunning = 0
    else:
        train.spin(FORWARD)
        trainRunning = 1

clampDown = 0

def moveClampDown(): # Manual Clamp Movement Down
    global clampDown
    clamp.spin(REVERSE)
    while clamp.is_spinning():
        if clamp.torque(TorqueUnits.NM) > 0.03:
                    clamp.stop()
    clampDown = 0

def moveClampUp(): # Manual Clamp Movement Up
    global clampDown
    clamp.spin(FORWARD)
    while clamp.is_spinning():
        if clamp.torque(TorqueUnits.NM) > 0.03:
                    clamp.stop()
    clampDown = 0


def stopClamp(): # Manual Clamp Movement Stop
    global clampDown
    clamp.stop()
    clampDown = 0

cRunning = 0

def runCollection():
    global cRunning, trainRunning, intakeRolling
    if intakeRolling and trainRunning and not cRunning:
        cRunning = 1
    if cRunning:
        trainRunning = 1
        intakeRolling = 1
        trainRun()
        rollIntake()
        cRunning = 0
    else:
        trainRunning = 0
        intakeRolling = 0
        trainRun()
        rollIntake()
        cRunning = 1






############################## CALLBACKS ##############################
controller.buttonR2.pressed(rollIntake)
controller.buttonR1.pressed(trainRun)
controller.buttonUp.pressed(moveClampUp)
controller.buttonDown.pressed(moveClampDown)
controller.buttonUp.released(clamp.stop)
controller.buttonDown.released(clamp.stop)



############################## TROUBLESHOOTING ##############################
# test to see if controller registers presses
def test_controller(): 
    controller.rumble(".")
    brain.screen.print("ihe")
controller.buttonA.pressed(test_controller)

def user_control():
    brain.screen.clear_screen()
    brain.screen.print("driver control")
    # place something in while loop (unclear)
    # i believe drive settings
    initialize()
    while True:
        wait(20, MSEC)
        

# create competition instance
comp = Competition(user_control, auton)

# actions to do when the program starts
brain.screen.clear_screen()
controller.rumble("-")