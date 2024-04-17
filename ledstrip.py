

from time import sleep
import time
import _thread
from machine import UART, Pin
#import digitalio
import board
import binascii
import re
import collections
from collections import deque
#from collections import deque
#import deque
#from micropython import alloc_deque
#from micropython import dealloc_deque
#import sys
from neopixel import *
from display import *

numpix = 5
strip = Neopixel(numpix, 0, 0, "GRB")

red = (255, 0, 0)
yellow = (255, 100, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
off = (0,0,0)
color_rgb = [red, yellow, green, blue, off]



curr_pix = 0
strip.brightness(50)
counter = 1000
def hazard_ahead():
    global counter 
    strip.fill(off)
    strip.show()

    if(counter == 0):
        print("Counter ", counter)
        strip.fill(red)
        strip.show()
        counter = 1000
    counter = counter - 1
while True:
   t1 = time.time()
   hazard_ahead()
   t2 = time.time()
   t3 = t2 - t1
   print("time: ", t3)
        
    
    
    
    



