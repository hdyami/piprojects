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

@app.route('/forward/<int:dC>/<int:seconds>')
def forward(dC,seconds):
    io.output(SLP, io.HIGH)
    BIN1_pwm.start(0)
    AIN1_pwm.start(0)

    BIN1_pwm.ChangeDutyCycle(dC)
    io.output(BIN2, io.LOW)

    io.output(AIN2, io.LOW)
    AIN1_pwm.ChangeDutyCycle(dC)

    time.sleep(seconds)

    io.output(SLP, io.LOW)
    BIN1_pwm.stop()
    AIN1_pwm.stop()

    return "forward"

@app.route('/backward/<int:dC>/<int:seconds>')
def backward(dC,seconds):
    print "backward"
    io.output(SLP, io.HIGH)
    BIN2_pwm.start(0)
    AIN2_pwm.start(0)


    io.output(BIN1, io.LOW)
    BIN2_pwm.ChangeDutyCycle(dC)

    AIN2_pwm.ChangeDutyCycle(dC)
    io.output(AIN1, io.LOW)

    time.sleep(seconds)
    
    io.output(SLP, io.LOW)
    BIN2_pwm.stop()
    AIN2_pwm.stop()

    return "backward"

@app.route('/spinRight/<int:dC>/<int:seconds>')
def spinRight(dC,seconds):
    print "spinRight"
    io.output(SLP, io.HIGH)
    BIN1_pwm.start(0)
    AIN2_pwm.start(0)

    io.output(BIN2, io.LOW)
    BIN1_pwm.ChangeDutyCycle(dC)
    io.output(AIN1, io.LOW)
    AIN2_pwm.ChangeDutyCycle(dC)

    time.sleep(seconds)

    io.output(SLP, io.LOW)
    BIN1_pwm.stop()
    AIN2_pwm.stop()

    return "spinRight"

@app.route('/spinLeft/<int:dC>/<int:seconds>')
def spinLeft(dC,seconds):
    print "spinLeft"
    io.output(SLP, io.HIGH)
    BIN2_pwm.start(0)
    AIN1_pwm.start(0)

    io.output(BIN1, io.LOW)
    BIN2_pwm.ChangeDutyCycle(dC)
    io.output(AIN2, io.LOW)
    AIN1_pwm.ChangeDutyCycle(dC)

    time.sleep(seconds)

    io.output(SLP, io.LOW)
    BIN2_pwm.stop()
    AIN1_pwm.stop()

    return "spinLeft"

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/pibot')
def pibot():
    print "hahhahah"
    return 'I am a robot!'

if __name__ == "__main__":
    # adafruit drv8833 breakout
    io.setmode(io.BCM)

    # Define Outputs to motors A and B SLP must be driven high to enable.
    BIN1 = 26
    BIN2 = 19
    SLP = 13
    AIN2 = 6
    AIN1 = 5

    # initialize pwm so we only have to do ChangeDutyCycle later
    io.setup(BIN1, io.OUT)
    BIN1_pwm=io.PWM(BIN1,100)
    # BIN1_pwm.start(0)

    io.setup(BIN2, io.OUT)
    BIN2_pwm=io.PWM(BIN2,100)
    # BIN2_pwm.start(0)

    io.setup(SLP, io.OUT)

    io.setup(AIN2, io.OUT)
    AIN2_pwm=io.PWM(AIN2,100)
    # AIN2_pwm.start(0)

    io.setup(AIN1, io.OUT)
    AIN1_pwm=io.PWM(AIN1,100)
    # AIN1_pwm.start(0)
    
    # ahhhh this calls the flask app! duhhhhh
    # only needed if invoking via python -m, not needed if invoked via flask run
    app.run(host='192.168.2.30', debug=True)
    io.cleanup()

# pibot_init()
