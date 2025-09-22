"""
The physical pin location, in the form of PX_Y (P8_28)
The gpio name, in the form of GPIOX_Y (GPIO2_24)
The gpio number, in the form of 32*X + Y (88) (USE THIS)
"""
import Adafruit_BBIO.GPIO as GPIO
from time import sleep

"""
pulse-counting variables
"""

#read GPS signal nan
#pin set-up -> input GPS signal
gpspin_1 = "P8_12" 
GPIO.setup(gpspin_1, GPIO.IN) # sets up pin as input

#pin set-up -> output signal
outpin_1 = "P9_12"
GPIO.setup(outpin_1, GPIO.OUT) 
GPIO.output(outpin_1, GPIO.LOW) 

outpin_2 = "P9_14"
GPIO.setup(outpin_2, GPIO.OUT) 
GPIO.output(outpin_2, GPIO.LOW)

pulse_time = 1
time_to_pause = 120
pulse_max = time_to_pause / (1 / pulse_time)
pulse_count = 0

GPIO.add_event_detect("P8_12", GPIO.RISING)

try:
    while True: 

        if GPIO.event_detected("P8_12"):

            pulse_count += 1

            GPIO.output(outpin_1, GPIO.HIGH) 
            sleep(.02)
            GPIO.output(outpin_1, GPIO.LOW)

            GPIO.output(outpin_2, GPIO.HIGH)
            sleep(.02)
            GPIO.output(outpin_2, GPIO.LOW)

        if pulse_count == pulse_max: #is this still necessary

            sleep(2) # sleep for 2 full pulses
            pulse_count = 0

except KeyboardInterrupt:

    pass

# Clean up GPIO settings before exiting
GPIO.cleanup()

#what should the 'end' sign be? involve a button?


