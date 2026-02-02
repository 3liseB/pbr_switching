"""
The physical pin location, in the form of PX_Y (P8_28)
The gpio name, in the form of GPIOX_Y (GPIO2_24)
The gpio number, in the form of 32*X + Y (88) (USE THIS)
"""
import Adafruit_BBIO.GPIO as GPIO
import time
from time import sleep
import argparse 

"""
pulse-counting variables
"""

#read GPS signal nan
#pin set-up -> input GPS signal
gpspin_1 = "P8_8" 
GPIO.setup(gpspin_1, GPIO.IN) # sets up pin as input

#pin set-up -> output signal
outpin_1 = "P8_10"
GPIO.setup(outpin_1, GPIO.OUT) 
GPIO.output(outpin_1, GPIO.LOW) 

outpin_2 = "P8_12"
GPIO.setup(outpin_2, GPIO.OUT) 
GPIO.output(outpin_2, GPIO.LOW)

GPIO.add_event_detect("P8_8", GPIO.RISING)

def read_switch_count():
    try:
        with open("/home/debian/set_count.txt") as f:
            settings = dict(line.strip().split("=") for line in f)
            pulse_num = int(settings["set_pnum"])
            pulse_interval = int(settings["set_pint"])
            total_time = int(settings["set_tot"])   
        return pulse_num, pulse_interval, total_time
    except:
          return 1, 1, 1

last_switched = outpin_1
#nothing is using total_time right now

try:
    while True: 
        pulse_num, pulse_interval, total_time = read_switch_count() #number of times the output is triggered #how long until switch
        print(pulse_num, pulse_interval, total_time)

        if last_switched == outpin_1:
            print('switch pin2')
            for i in range(pulse_num):
                sleep(pulse_interval) #delay
                GPIO.wait_for_edge("P8_8", GPIO.RISING)
                GPIO.output(outpin_2, GPIO.HIGH)
                sleep(.5) #pulse period
                GPIO.output(outpin_2, GPIO.LOW)
            last_switched = outpin_2
    
        else:
            print('switch pin1')
            for i in range(pulse_num):
                sleep(pulse_interval) #delay
                GPIO.wait_for_edge("P8_8", GPIO.RISING)
                GPIO.output(outpin_1, GPIO.HIGH) 
                sleep(.5) #pulse period
                GPIO.output(outpin_1, GPIO.LOW)
            last_switched = outpin_1

except KeyboardInterrupt:

    pass

GPIO.cleanup()
