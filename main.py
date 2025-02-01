# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       1053730                                                      #
# 	Created:      1/25/2025, 7:13:27 AM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #


# everything currently works except:
# Auton blocks
# Potentiometer measuring for clamp

# Library imports
from vex import *

brain = Brain()

controller = Controller()

clamp = Motor(Ports.PORT20)
clampMeasure = Potentiometer(brain.three_wire_port.a) # 3372 high point, 3925 low point ish
intake = Motor(Ports.PORT2)
train = Motor(Ports.PORT21)
leftA = Motor(Ports.PORT15, True)
leftB = Motor(Ports.PORT16, True)
left = MotorGroup(leftA, leftB)
rightA = Motor(Ports.PORT11)
rightB = Motor(Ports.PORT12)
right = MotorGroup(rightA, rightB)
drivetrain = DriveTrain(left, right, 319.19, 385, 260, MM, 2)

# initalize 
wait(30, MSEC)



############################## MOTOR FUNCTIONS ##############################
def initialize(): # set standard velocities
    drivetrain.set_stopping(BRAKE) # Stopping Stops
    clamp.set_velocity(30, PERCENT) # Define the speed to run our motors
    intake.set_velocity(50, PERCENT)
    train.set_velocity(100, PERCENT)
    clamp.set_stopping(HOLD) # Clamp will actually hold

intakeRunning = 0
trainRunning = 0
clampDown = 0



# code for clamp should run as follows:
# on manual - when we press down, the clamp moves down until
# it experiences enough torque or hits the potentiometer limit
# if we go up then same thing (should stop at potentiometer first though)
# 
# the trigger should track potentiometer and decide whether or not to go up or down based on that and clampDown
def clamp_lower():
    # current code
    global clampDown
    clamp.spin(REVERSE)
    while clamp.is_spinning():
        if clamp.torque(TorqueUnits.NM) > 0.03:
            clamp.stop()
            clampDown = 1

    # code for when potentiometer is added
    # global clampDown
    # clamp.spin(REVERSE)
    # while clamp.is_spinning():
    #     if clampMeasure.angle() <= 0:
    #         clamp.stop()
    #         clampDown = 1

def clamp_raise():
    global clampDown
    clamp.spin(FORWARD)
    while clamp.is_spinning():
        brain.screen.print(clampMeasure.angle)
        if clamp.torque(TorqueUnits.NM) > 0.03:
            clamp.stop()
            clampDown = 0
    
    # code for when potentiometer is added
    # global clampDown
    # clamp.spin(REVERSE)
    # while clamp.is_spinning():
    #     if clampMeasure.angle() <= 0:
    #         clamp.stop()
    #         clampDown = 0

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
        while train.is_spinning():
            if train.torque(TorqueUnits.NM) > 0.5:
                train.stop()
                wait(0.05, SECONDS)
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
controller.buttonA.pressed(test_controller)


############################## AUTON BLOCKS ##############################


"""
Auton has four options:
Positive red
Negative red
Positive blue
Negative blue
 -______________________-
  |                     |
  |      O2  M  O2      |
  |                     |
R |       M      M      | B
E | O  O2    LL    O2 O | L
D |       M      M      | U
  |                     | E
  |  O   O2  M  O2  O   |
 +| ____________________|+

When in negative corner, we can:
Grab a mobile goal
Grab a center ring (?)
Touch ladder

When in positive corner, we can:
Grab a mobile goal
Grab a center ring (?)
Grab opponent ring
Touch ladder





"""

# assume starting in the center of 
def auton_mobile(color, corner):
    if color == "red":
        if corner == "+":
            # drivetrain back facing towards center
            drivetrain.drive_for(REVERSE, 23.08, INCHES)
            drivetrain.turn_for(RIGHT, 45, DEGREES)
            drivetrain.drive_for(REVERSE, 6, INCHES)
            clamp_lower()
            wait(0.5, SECONDS)
            
            # collect non-alliance ring
            collections_trigger()
            drivetrain.drive_for(FORWARD, 20, INCHES)
            wait(0.5, SECONDS)
            collections_trigger()
            clamp_raise()
            drivetrain.drive_for(FORWARD, 2, INCHES)
            drivetrain.turn_for(LEFT, 45, DEGREES)
            drivetrain.drive_for(REVERSE, 5, INCHES)
            drivetrain.turn_for(RIGHT, 45, DEGREES)
            drivetrain.drive_for(REVERSE, 32.64, INCHES)

        elif corner == '-':
            pass
    else:
        if corner == "+":
            # drivetrain back facing towards center
            drivetrain.drive_for(REVERSE, 23.08, INCHES)
            drivetrain.turn_for(LEFT, 45, DEGREES)
            drivetrain.drive_for(REVERSE, 6, INCHES)
            clamp_lower()
            wait(0.5, SECONDS)
            
            # collect non-alliance ring
            collections_trigger()
            drivetrain.drive_for(FORWARD, 20, INCHES)
            wait(0.5, SECONDS)
            collections_trigger()
            clamp_raise()
            drivetrain.drive_for(FORWARD, 2, INCHES)
            drivetrain.turn_for(RIGHT, 45, DEGREES)
            drivetrain.drive_for(REVERSE, 5, INCHES)
            drivetrain.turn_for(LEFT, 45, DEGREES)
            drivetrain.drive_for(REVERSE, 32.64, INCHES)
        elif corner == '-':
            pass
    pass


############################## COMPETITION ##############################
def test_decorator(func):
    def wrapper(*args, **kwargs):
        print(args)
        print(kwargs)
        return func(*args, **kwargs)
    return wrapper

def auton():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here

def user_control():
    brain.screen.clear_screen()
    brain.screen.print("driver control")
    initialize()
    left.spin(FORWARD)
    right.spin(FORWARD)
    while True:
        # OPTION ONE
        wait(20, MSEC)
        # left.set_velocity(controller.axis3.position(), PERCENT)
        # right.set_velocity(controller.axis2.position(), PERCENT) among us

        # OPTION TWO (DEADZONING)
        leftpos = controller.axis3.position()
        if -7 < leftpos < 7:
            left.set_velocity(0, PERCENT)
        else:
            left.set_velocity(controller.axis3.position(), PERCENT)
        rightpos = controller.axis2.position()
        if -7 < rightpos < 7:
            right.set_velocity(0, PERCENT)
        else:
            right.set_velocity(controller.axis2.position(), PERCENT)

        

# create competition instance
comp = Competition(user_control, auton)

# actions to do when the program starts
controller.rumble("-")
drivetrain.drive_for(FORWARD, 23.08, INCHES)