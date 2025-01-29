# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       1053730                                                      #
# 	Created:      1/25/2025, 7:13:27 AM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #


# everything currently works except:
# Drive
# Auton blocks
# Potentiometer Measuring for clamp

# Library imports
from vex import *

brain = Brain()

controller = Controller()

clamp = Motor(Ports.PORT20)
clampMeasure = Potentiometer(brain.three_wire_port.a) # 3372 high point, 3925 low point ish
intake = Motor(Ports.PORT2)
train = Motor(Ports.PORT21)
leftA = Motor(Ports.PORT15)
leftB = Motor(Ports.PORT16)
left = MotorGroup(leftA, leftB)
rightA = Motor(Ports.PORT12)
rightB = Motor(Ports.PORT13)
right = MotorGroup(rightA, rightB)
drivetrain = DriveTrain(left, right, 319.19, 295, 40, MM, 1)

# initalize 
wait(30, MSEC)



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

intakeRunning = 0
trainRunning = 0
clampDown = 0

def clamp_lower():
    global clampDown
    clamp.spin(REVERSE)
    while clamp.is_spinning():
        brain.screen.print(clampMeasure.angle)
        if clamp.torque(TorqueUnits.NM) > 0.03:
                    clamp.stop()

def clamp_raise():
    global clampDown
    clamp.spin(FORWARD)
    while clamp.is_spinning():
        brain.screen.print(clampMeasure.angle)
        if clamp.torque(TorqueUnits.NM) > 0.03:
                    clamp.stop()

# bool - autotrack clamp movement
# ! HANDLE MANUAL MOVEMENT IN CLAMPDOWN VARIABLE (TRACK POSITION?)
def clamp_trigger():
    pass

def train_trigger():
    global trainRunning
    if trainRunning:
        train.stop()
        trainRunning = 0
    else:
        train.spin(FORWARD)
        trainRunning = 1

def intake_trigger():
    global intakeRunning
    if intakeRunning:
        intake.stop()
        intakeRunning = 0
    else: 
        intake.spin(FORWARD)
        intakeRunning = 1

# if everything is running, stop all intake methods
# else run all intake methods
def collections_trigger():
    global intakeRunning, trainRunning
    print(intakeRunning, trainRunning)
    if not intakeRunning or not trainRunning:
        trainRunning = 0
        intakeRunning = 0
        train_trigger()
        intake_trigger()
    else:
        trainRunning = 1
        intakeRunning = 1
        train_trigger()
        intake_trigger()


############################## CALLBACKS ##############################
controller.buttonR2.pressed(intake_trigger)
controller.buttonR1.pressed(train_trigger)

controller.buttonUp.pressed(clamp_raise)
controller.buttonUp.released(clamp.stop)

controller.buttonDown.pressed(clamp_lower)
controller.buttonDown.released(clamp.stop)

controller.buttonL2.pressed(collections_trigger)


############################## TROUBLESHOOTING ##############################
# test to see if controller registers presses
def test_controller(): 
    controller.rumble(".")
    brain.screen.print("controller works!")
    print('hi')
controller.buttonA.pressed(test_controller)


############################## AUTON BLOCKS ##############################
def auton_mobile():
    pass






############################## COMPETITION ##############################
def auton():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here

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