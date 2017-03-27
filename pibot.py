import sys
import time
import simplejson as json
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
from flask import Flask
from flask import request
from pprint import pprint

app = Flask(__name__)

@app.route('/forward', methods=['POST', 'GET'])
def forward(secs=0, dC=0):
    if request.method == 'POST':
        url_args = request.args.get('seconds','dutyCycle')
        pprint(url_args)

        # print "aha"
    # GPIO.output(SLP, GPIO.HIGH)

    # BIN1_pwm.ChangeDutyCycle(dutyCycle)
    # GPIO.output(BIN2, GPIO.LOW)

    # GPIO.output(AIN2, GPIO.LOW)
    # AIN1_pwm.ChangeDutyCycle(dutyCycle)

    # time.sleep(seconds)

    # stopall();

    return 'forward'

@app.route('/backward')
def backward(seconds=3, dutyCycle=70):
    print "backward"
    GPIO.output(SLP, GPIO.HIGH)

    GPIO.output(BIN1, GPIO.LOW)
    BIN2_pwm.ChangeDutyCycle(dutyCycle)

    AIN2_pwm.ChangeDutyCycle(dutyCycle)
    GPIO.output(AIN1, GPIO.LOW)
    time.sleep(seconds)

    stopall()

    return "backward"

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
  
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/pibot')
def pibot():
    print "hahhahah"
    return 'I am a robot!'

if __name__ == "__main__":
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
    
    app.run(host='0.0.0.0')