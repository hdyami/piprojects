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

# initialize pwm so we only have to do ChangeDutyCycle later
GPIO.setup(BIN1, GPIO.OUT)
BIN1_pwm=GPIO.PWM(BIN1,100)
BIN1_pwm.start(0)

GPIO.setup(BIN2, GPIO.OUT)
BIN2_pwm=GPIO.PWM(BIN2,100)
BIN2_pwm.start(0)

GPIO.setup(SLP, GPIO.OUT)

GPIO.setup(AIN2, GPIO.OUT)
AIN2_pwm=GPIO.PWM(AIN2,100)
AIN2_pwm.start(0)

GPIO.setup(AIN1, GPIO.OUT)
AIN1_pwm=GPIO.PWM(AIN1,100)
AIN1_pwm.start(0)

def forward(seconds=0, dutyCycle=0):
    print "forward"
    GPIO.output(SLP, GPIO.HIGH)

    BIN1_pwm.ChangeDutyCycle(dutyCycle)
    GPIO.output(BIN2, GPIO.LOW)

    GPIO.output(AIN2, GPIO.LOW)
    AIN1_pwm.ChangeDutyCycle(dutyCycle)

    time.sleep(seconds)

    stopall();

def backward(seconds=0, dutyCycle=0):
    print "backward"
    GPIO.output(SLP, GPIO.HIGH)

    GPIO.output(BIN1, GPIO.LOW)
    BIN2_pwm.ChangeDutyCycle(dutyCycle)

    AIN2_pwm.ChangeDutyCycle(dutyCycle)
    GPIO.output(AIN1, GPIO.LOW)
    time.sleep(seconds)

    stopall()

def stopall():
    print "stop"
    # Motor breaking
    # set SLP on, set AIN2 off and AIN1 off
    GPIO.output(SLP, GPIO.LOW)

    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.LOW) 

    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(AIN1, GPIO.LOW)
    
    BIN2_pwm.stop()
    AIN2_pwm.stop()
    AIN1_pwm.stop()
    BIN1_pwm.stop()
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
    GPIO.output(SLP, GPIO.HIGH)

    # set enA on, set BIN1 off and BIN2 on
    BIN1_pwm.ChangeDutyCycle(dutyCycle)
    GPIO.output(BIN2, GPIO.LOW) 
    # set SLP on, set AIN2 on and AIN1 off
    AIN2_pwm.ChangeDutyCycle(dutyCycle)
    GPIO.output(AIN1, GPIO.LOW) 

    time.sleep(seconds)
    stopall()

def spinRight(seconds=0):
    print "spinRight"
    GPIO.output(SLP, GPIO.HIGH)
    # set enA on, set BIN1 off and BIN2 on
    GPIO.output(SLP, GPIO.HIGH)

    GPIO.output(BIN1, GPIO.LOW)
    BIN2_pwm.ChangeDutyCycle(dutyCycle)
    GPIO.output(AIN2, GPIO.LOW)
    AIN1_pwm.ChangeDutyCycle(dutyCycle)

    time.sleep(seconds)
    stopall()


forward(2.5, 35)
backward(1.5, 55)



# spinLeft(1.5)
# spinRight(1.5)

GPIO.cleanup()
