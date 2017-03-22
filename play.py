#!/usr/bin/python

import time
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

# ===========================================================================
# Example Code
# ===========================================================================

# adafruit drv8833 breakout
GPIO.setmode(GPIO.BCM)

# Define Outputs to motors A and B SLP must be driven high to enable.
BIN1 = 26
BIN2 = 19
SLP = 13
AIN2 = 6
AIN1 = 5

GPIO.setup(BIN1, GPIO.OUT)
BIN1_pwm=GPIO.PWM(26,100)
my_pwm.start(0)

GPIO.setup(BIN2, GPIO.OUT)
GPIO.setup(SLP, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)

def forward(seconds=0):
    print "forward"
    GPIO.output(SLP, GPIO.HIGH)

    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)

    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(AIN1, GPIO.HIGH)

    time.sleep(seconds)
    stop();

def backward(seconds=0):
    print "backward"
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH) 

    GPIO.output(SLP, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(AIN1, GPIO.LOW)
    time.sleep(seconds)
    stop()

def stop():
    print "stop"
    # Motor breaking
    # set SLP on, set AIN2 off and AIN1 off
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.LOW) 

    GPIO.output(SLP, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(AIN1, GPIO.LOW)

    # coasting
    # set enA off, set BIN1 off and BIN2 off
    # set SLP off, set AIN2 off and AIN1 off
  
def turnRight():
    print "turnRight"
    # set enA on, set BIN1 on and BIN2 off
    # set SLP off, set AIN2 off and AIN1 off
  
def turnLeft(seconds=0):
    print "spinLeft"
    # set enA on, set BIN1 off and BIN2 on
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH) 
    # set SLP on, set AIN2 on and AIN1 off
    GPIO.output(SLP, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW) 

    time.sleep(seconds)
    stop()

def spinLeft(seconds=0):
    print "spinLeft"
    # set enA on, set BIN1 off and BIN2 on
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW) 
    # set SLP on, set AIN2 on and AIN1 off
    GPIO.output(SLP, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(AIN1, GPIO.LOW) 

    time.sleep(seconds)
    stop()

def spinRight(seconds=0):
    print "spinRight"
    # set enA on, set BIN1 off and BIN2 on
    GPIO.output(SLP, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH) 
    # set SLP on, set AIN2 on and AIN1 off
    GPIO.output(SLP, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(AIN1, GPIO.HIGH) 

    time.sleep(seconds)
    stop()


# forward(.5)
# backward(.5)
spinLeft(1.5)
spinRight(1.5)

GPIO.cleanup()
