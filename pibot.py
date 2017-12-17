#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import sys
import time
import picamera
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
    print "stop"

    io.output(SLP, io.LOW)

    io.output(BIN2, io.LOW)
    io.output(BIN1, io.LOW)
    io.output(AIN1, io.LOW)
    io.output(AIN2, io.LOW)

    BIN2_pwm.stop()
    AIN2_pwm.stop()
    BIN1_pwm.stop()
    AIN1_pwm.stop()
    # CAM_pwm.stop()

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

    io.output(AIN2, io.LOW)
    AIN1_pwm.start(dC)

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
    #right motor
    io.output(BIN2, io.LOW)
    BIN1_pwm.start(dC)
    #left motor
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

@app.route('/rightBack/<int:dC>')
def rightBack(dC):
    print "rightBack"
    io.output(SLP, io.HIGH)
    #right motor
    io.output(BIN2, io.LOW)
    BIN1_pwm.start(dC)

    return "rightBack"

@app.route('/leftBack/<int:dC>')
def leftBack(dC):
    print "leftBack"
    io.output(SLP, io.HIGH)
    #left motor
    io.output(AIN2, io.LOW)
    AIN1_pwm.start(dC)

    return "leftBack"

@app.route('/camAngle/<float:dC>')
def camAngle(dC):
    # dC = (1/18) * dC + 2
    # print str(dC)
    # change pulse to servo
    # CAM_pwm.start(dC)
    # CAM_pwm.ChangeDutyCycle(dC)
    # time.sleep(1)
    # CAM_pwm.stop()

    return "Cam Angle"+str(dC)

@app.route('/picture')
def picture():
    print "Take picture"
    # take a picture
    camera = picamera.PiCamera()
    camera.hflip = True
    camera.vflip = True
    camera.capture('captures/image.jpg')

    return "Take picture"

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/pibot')
def pibot():
    print "hahhahah"
    return 'I getting smarter!'

# sharp proximity sensor edge detection!
# currently if prox is sensed begin looking for that prox to drop away and move backwards
# if that prox drops away, stop moving and go back to sensing for prox
@app.route('/sensorAautoStopDetect')
def sensorAautoStopDetect(SensA):
    print "RIGHT sensor a DETECT"

    io.remove_event_detect(SensA)
    stop()
    io.add_event_detect(SensA, io.RISING, callback=sensorAautoStopRelease, bouncetime=450)

    return stop()

@app.route('/sensorBautoStopDetect')
def sensorBautoStopDetect(SensB):
    print "LEFT sensor b DETECT"
    
    io.remove_event_detect(SensB)
    stop()
    io.add_event_detect(SensB, io.RISING, callback=sensorBautoStopRelease, bouncetime=450)

    return stop()

@app.route('/sensorAautoStopRelease')
def sensorAautoStopRelease(SensA):
    print "RIGHT sensor a RELEASE"

    io.remove_event_detect(SensA)
    io.add_event_detect(SensA, io.FALLING, callback=sensorAautoStopDetect, bouncetime=450)

    return "RIGHT sensor a RELEASE"

@app.route('/sensorBautoStopRelease')
def sensorBautoStopRelease(SensB):
    print "LEFT sensor b RELEASE"
    
    io.remove_event_detect(SensB)
    io.add_event_detect(SensB, io.FALLING, callback=sensorBautoStopDetect, bouncetime=450)

    return "LEFT sensor b RELEASE"

# Begin AutoGo
@app.route('/sensorAautoGoDetect')
def sensorAautoGoDetect(SensA):
    print "RIGHT sensor a DETECT"

    io.remove_event_detect(SensA)
    stop()
    io.add_event_detect(SensA, io.RISING, callback=sensorAautoGoRelease, bouncetime=450)

    return spinLeft(40)
    # return leftBack(40)

@app.route('/sensorBautoGoDetect')
def sensorBautoGoDetect(SensB):
    print "LEFT sensor b DETECT"
    
    io.remove_event_detect(SensB)
    stop()
    io.add_event_detect(SensB, io.RISING, callback=sensorBautoGoRelease, bouncetime=450)

    return spinRight(40)
    # return rightBack(40)

@app.route('/sensorAautoGoRelease')
def sensorAautoGoRelease(SensA):
    print "RIGHT sensor a RELEASE"

    io.remove_event_detect(SensA)
    stop()
    io.add_event_detect(SensA, io.FALLING, callback=sensorAautoGoDetect, bouncetime=450)

    return forward(40)

@app.route('/sensorBautoGoRelease')
def sensorBautoGoRelease(SensB):
    print "LEFT sensor b RELEASE"
    
    io.remove_event_detect(SensB)
    stop()
    io.add_event_detect(SensB, io.FALLING, callback=sensorBautoGoDetect, bouncetime=450)

    return forward(40)
     
@app.route('/autoStop/<string:action>')
def autoStop(action):
    if action == "disable":
        print "Stopping sensor detection"
        
        io.remove_event_detect(SensB)
        io.remove_event_detect(SensA)
    if action == "enable":
        print "Starting sensor detection"

        io.add_event_detect(SensA, io.FALLING, callback=sensorAautoStopDetect, bouncetime=450)
        io.add_event_detect(SensB, io.FALLING, callback=sensorBautoStopDetect, bouncetime=450)
    
    return stop()

@app.route('/autoGo/<string:action>')
def autoGo(action):
    if action == "disable":
        print "Stopping sensor detection"
        
        io.remove_event_detect(SensB)
        io.remove_event_detect(SensA)
    if action == "enable":
        print "Starting sensor detection"

        io.add_event_detect(SensA, io.FALLING, callback=sensorAautoGoDetect, bouncetime=450)
        io.add_event_detect(SensB, io.FALLING, callback=sensorBautoGoDetect, bouncetime=450)
    
    return stop()

if __name__ == "__main__":
    # adafruit drv8833 breakout
    io.setmode(io.BCM)

    # Define Outputs to motors A and B SLP must be driven high to enable.
    BIN1 = 26 # BIN right motor #
    BIN2 = 19
    SLP = 13
    AIN2 = 6 # AIN left motor #
    AIN1 = 5

    CAM = 21 # pin for camera x axis servo
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

    io.setup(CAM, io.OUT)
    CAM_pwm = io.PWM(CAM, 50)
    # initialize position - otherwise it locks up way past 180??
    CAM_pwm.start(6.5)
    time.sleep(1)
    CAM_pwm.stop()



    # intialize sharp prox sensor inputs and callbacks
    # when something is sensed, red light comes on and FALLING edge is detected.
    # when object is no longer sensed RISING edge is detected
    # FALLING - on proximity sensed RISING - on promximity sense released
    io.setup(SensA, io.IN, pull_up_down=io.PUD_DOWN)
    io.setup(SensB, io.IN, pull_up_down=io.PUD_DOWN)

    # these can be commented out to disable auto mode TODO make toggle in ui which can remove these event detects
    # io.add_event_detect(SensA, io.FALLING, callback=sensorADetect, bouncetime=450)
    # io.add_event_detect(SensB, io.FALLING, callback=sensorBDetect, bouncetime=450)

    # ahhhh this calls the flask app! duhhhhh
    # only needed if invoking via python -m, not needed if invoked via flask run
    app.run(host='192.168.2.30', debug=True)
    io.cleanup()

# pibot_init()
