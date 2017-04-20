#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import sys
import signal
import time
try:
    import RPi.GPIO as io
except RuntimeError:
    print("Error importing RPi.io!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
from pprint import pprint

def sensorADetect(SensA):
	print "Sens A"

def sensorBDetect(SensB):
	print "Sens B"

def exit_gracefully(signum, frame):
	io.cleanup()
	print 'Signal handler called with signal', signum
	print "bye!"


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_gracefully)

    SensA = 17
    SensB = 18

    # Sharp GP2Y0D815Z0F pololu carrier/breakout
    io.setmode(io.BCM)
	

io.setup(SensA, io.IN, pull_up_down=io.PUD_DOWN)
io.setup(SensB, io.IN, pull_up_down=io.PUD_DOWN)

io.add_event_detect(SensA, io.RISING, callback=sensorADetect, bouncetime=50)
io.add_event_detect(SensB, io.RISING, callback=sensorBDetect, bouncetime=50)

time.sleep(60)

# while True:
# 	if io.input(SensA):
# 		print "sensor a"
# 	if io.input(SensB):
# 		print "sensor b"

# io.add_event_detect(SensA, io.RISING, callback=sensorADetect, bouncetime=50)
# io.add_event_detect(SensB, io.RISING, callback=sensorBDetect, bouncetime=50)

