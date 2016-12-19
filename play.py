#!/usr/bin/python

import time
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

# ===========================================================================
# Example Code
# ===========================================================================

# L298N setup code
GPIO.setmode(GPIO.BCM)

# Define Outputs to L298N 
#enA = GPIO.setup(20, GPIO.OUT)
#in1 = GPIO.setup(16, GPIO.OUT) 
#in2 = GPIO.setup(12, GPIO.OUT) 
#enB = GPIO.setup(21, GPIO.OUT)
#in3 = GPIO.setup(19, GPIO.OUT) 
#in4 = GPIO.setup(26, GPIO.OUT)

GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

def backward():
    print "backward"
    # set enB on, set in3 on and in4 off
    # set enA on, set in1 on and in2 off
    GPIO.output(21, GPIO.HIGH)
    GPIO.output(19, GPIO.HIGH)
    GPIO.output(26, GPIO.LOW)

    GPIO.output(20, GPIO.HIGH)
    GPIO.output(16, GPIO.HIGH)
    GPIO.output(12, GPIO.LOW)
  
def forward():
    print "forward"
    GPIO.output(21, GPIO.HIGH)
    GPIO.output(19, GPIO.LOW)
    GPIO.output(26, GPIO.HIGH) 

    GPIO.output(20, GPIO.HIGH)
    GPIO.output(16, GPIO.LOW)
    GPIO.output(12, GPIO.HIGH)
def stop():
    print "stop"
    # Motor breaking
    # set enA on, set in1 off and in2 off
    # set enB on, set in3 off and in4 off
    GPIO.output(21, GPIO.HIGH)
    GPIO.output(19, GPIO.LOW)
    GPIO.output(26, GPIO.LOW)
    GPIO.output(20, GPIO.HIGH)
    GPIO.output(16, GPIO.LOW)
    GPIO.output(12, GPIO.LOW)

    # coasting
    # set enA off, set in1 off and in2 off
    # set enB off, set in3 off and in4 off
  
def turnRight():
    print "turnRight"
    # set enA on, set in1 on and in2 off
    # set enB off, set in3 off and in4 off
  
def turnLeft():
    print "turnLeft"
    # set enA off, set in1 off and in2 off
    # set enB on, set in3 on and in4 off

  
def spinRight():
    print "spinRight"
    # set enA on, set in1 on and in2 off
    GPIO.output(21, GPIO.HIGH)
    GPIO.output(19, GPIO.HIGH)
    GPIO.output(26, GPIO.LOW)
    # set enB on, set in3 off and in4 on
    GPIO.output(20, GPIO.HIGH)
    GPIO.output(16, GPIO.LOW)
    GPIO.output(12, GPIO.HIGH)
    
def spinLeft():
    print "spinLeft"
    # set enA on, set in1 off and in2 on
    GPIO.output(21, GPIO.HIGH)
    GPIO.output(19, GPIO.LOW)
    GPIO.output(26, GPIO.HIGH)
    # set enB on, set in3 on and in4 off
    GPIO.output(20, GPIO.HIGH)
    GPIO.output(16, GPIO.HIGH)
    GPIO.output(12, GPIO.LOW)

forward()
time.sleep(3)
#backward()
#time.sleep(5)
#stop()
#time.sleep(1)
#backward()
#time.sleep(2)
#stop()
#spinLeft()
#time.sleep(2)
#spinRight()
#time.sleep(2)
GPIO.cleanup()
