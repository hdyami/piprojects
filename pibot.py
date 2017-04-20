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
from flask import request
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
    return 'I am a robot!'

def sensorADetect(SensA):
    print "Sens A"

def sensorBDetect(SensB):
    print "Sens B"

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
    SensA = 17
    SensB = 18

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
    io.setup(SensA, io.IN, pull_up_down=io.PUD_DOWN)
    io.setup(SensB, io.IN, pull_up_down=io.PUD_DOWN)

    io.add_event_detect(SensA, io.RISING, callback=sensorADetect, bouncetime=100)
    io.add_event_detect(SensB, io.RISING, callback=sensorBDetect, bouncetime=100)
    
    # ahhhh this calls the flask app! duhhhhh
    # only needed if invoking via python -m, not needed if invoked via flask run
    app.run(host='192.168.2.30', debug=True)
    io.cleanup()

# pibot_init()
