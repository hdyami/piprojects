#!/usr/bin/env python
import RPi.GPIO as io
import time

io.setmode(io.BCM)

io.setup(21, io.OUT)

p = io.PWM(21, 50)

p.start(7.5)

try:
        while True:
		p.ChangeDutyCycle(7.5)  # turn towards 90 degree
		print "90 degrees"
		time.sleep(1) # sleep 1 second
		p.ChangeDutyCycle(2.5)  # turn towards 0 degree
		print "0 degrees"
		time.sleep(1) # sleep 1 second
		p.ChangeDutyCycle(12.5) # turn towards 180 degree
		print "180 degrees"
        time.sleep(1) # sleep 1 second 
except KeyboardInterrupt:
	p.stop()
        io.cleanup()