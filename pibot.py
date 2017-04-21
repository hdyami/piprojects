#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import sys
import time
import simplejson as json
try:
    import RPi.GPIO as io
except RuntimeError:
    print("Error importing RPi.io!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
from flask import Flask
from flask import request, redirect, url_for
from pprint import pprint

app = Flask(__name__)

# stop all gpio
@app.route('/stop')
def stop():
    io.output(SLP, io.LOW)

    io.output(BIN2, io.LOW)
    io.output(BIN1, io.LOW)
    io.output(AIN1, io.LOW)
    io.output(AIN2, io.LOW)

    BIN2_pwm.stop()
    AIN2_pwm.stop()
    BIN1_pwm.stop()
    AIN1_pwm.stop()

    print "stop"

    return "stop"


@app.route('/backward/<int:dC>')
def backward(dC):
    print "backward"
    # set enable pin high
    io.output(SLP, io.HIGH)
    # set duty cycle to whatever we pass as argument
    # drive the other pole of our dc motor low
    io.output(BIN2, io.LOW)
    BIN1_pwm.start(dC)
    BIN1_pwm.ChangeDutyCycle(dC)

    io.output(AIN2, io.LOW)
    AIN1_pwm.start(dC)
    AIN1_pwm.ChangeDutyCycle(dC)

    return "backward"

@app.route('/forward/<int:dC>')
def forward(dC):
    print "forward"
    io.output(SLP, io.HIGH)

    io.output(BIN1, io.LOW)
    BIN2_pwm.start(dC)
    
    io.output(AIN1, io.LOW)
    AIN2_pwm.start(dC)

    return "forward"

@app.route('/spinRight/<int:dC>')
def spinRight(dC):
    print "spinRight"
    io.output(SLP, io.HIGH)

    io.output(BIN2, io.LOW)
    BIN1_pwm.start(dC)

    io.output(AIN1, io.LOW)
    AIN2_pwm.start(dC)

    return "spinRight"

@app.route('/spinLeft/<int:dC>')
def spinLeft(dC):
    print "spinLeft"
    io.output(SLP, io.HIGH)

    io.output(BIN1, io.LOW)
    BIN2_pwm.start(dC)

    io.output(AIN2, io.LOW)
    AIN1_pwm.start(dC)

    return "spinLeft"

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/pibot')
def pibot():
    print "hahhahah"
    return 'I getting smarter!'

# @app.route('/stop')
def stopauto():
    io.output(SLP, io.LOW)

    io.output(BIN2, io.LOW)
    io.output(BIN1, io.LOW)
    io.output(AIN1, io.LOW)
    io.output(AIN2, io.LOW)

    BIN2_pwm.stop()
    AIN2_pwm.stop()
    BIN1_pwm.stop()
    AIN1_pwm.stop()

    print "auto stop"
    backward(85)
    time.sleep(.25)
    stop()
    spinRight(55)
    time.sleep(.5)
    stop()
    spinLeft(55)
    time.sleep(.5)

    return stop()

def sensorADetect(SensA):
    print "RIGHT sensor a DETECT"

    io.remove_event_detect(SensA)
    stop()
    io.add_event_detect(SensA, io.RISING, callback=sensorARelease, bouncetime=500)

    return backward(35)

def sensorBDetect(SensB):
    print "LEFT sensor b DETECT"
    
    io.remove_event_detect(SensB)
    stop()
    io.add_event_detect(SensB, io.RISING, callback=sensorBRelease, bouncetime=500)

    return backward(35)

def sensorARelease(SensA):
    print "RIGHT sensor a RELEASE"
    
    io.remove_event_detect(SensB)
    io.add_event_detect(SensA, io.FALLING, callback=sensorBDetect, bouncetime=500)

    return stop()

def sensorBRelease(SensB):
    print "LEFT sensor b RELEASE"
    
    io.remove_event_detect(SensB)
    io.add_event_detect(SensB, io.FALLING, callback=sensorADetect, bouncetime=500)

    return stop()

if __name__ == "__main__":
    # adafruit drv8833 breakout
    io.setmode(io.BCM)

    # Define Outputs to motors A and B SLP must be driven high to enable.
    BIN1 = 26
    BIN2 = 19
    SLP = 13
    AIN2 = 6
    AIN1 = 5

    # Define inputs to two sharp 10 cm prox sensors
    SensA = 17 # left
    SensB = 18 # right

    # initialize pwm so we only have to do ChangeDutyCycle later
    io.setup(BIN1, io.OUT)
    BIN1_pwm=io.PWM(BIN1,100)

    io.setup(BIN2, io.OUT)
    BIN2_pwm=io.PWM(BIN2,100)

    io.setup(SLP, io.OUT)

    io.setup(AIN2, io.OUT)
    AIN2_pwm=io.PWM(AIN2,100)

    io.setup(AIN1, io.OUT)
    AIN1_pwm=io.PWM(AIN1,100)

    # intialize sharp prox sensor inputs and callbacks
    # when something is sensed, red light comes on and FALLING edge is detected.
    # when object is no longer sensed RISING edge is detected
    # FALLING - on proximity sensed RISING - on promximity sense released
    io.setup(SensA, io.IN, pull_up_down=io.PUD_DOWN)
    io.setup(SensB, io.IN, pull_up_down=io.PUD_DOWN)

    io.add_event_detect(SensA, io.FALLING, callback=sensorADetect, bouncetime=500)
    io.add_event_detect(SensB, io.FALLING, callback=sensorBDetect, bouncetime=500)

    # ahhhh this calls the flask app! duhhhhh
    # only needed if invoking via python -m, not needed if invoked via flask run
    app.run(host='192.168.2.30', debug=False)
    io.cleanup()

# pibot_init()
