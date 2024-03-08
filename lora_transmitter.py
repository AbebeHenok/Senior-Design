from deque import deque
from machine import UART, Pin, I2C
import busio
import board
from adafruit_lsm6ds.ism330dhcx import ISM330DHCX as ISM
import time
from time import sleep
import _thread
import math
from mpy_decimal import *
#import mpy_decimal
import adafruit_gps
import binascii
import re
import sys

uart =UART(0,baudrate = 9600,stop = 1 ,tx = Pin(0),rx = Pin(1))
    #uart = UART.init(baudrate=9600, bits=8, parity=None, stop=1, Tx = 0, Rx = 1)
sensorReading = "1,0,30.0031,20.1241,W" # global string
stringToTransmit = "312c352e303030303030312c342e30303030303031"
#stringToTransmit = "1 5.0000001 6.0000001"
uart.write(bytes("AT+MODE=TEST", "utf-8"))  #ATTEMPTING AT+MODE=TEST AUTO
time.sleep(1)
#uart.write(bytes("AT+MODE=TXLRPKT", "utf-8"))  #ATTEMPTING AT+MODE=TEST AUTO
#time.sleep(2)
b = "AT+TEST=TXLRSTR "+bytes(stringToTransmit.encode('utf-8')).decode()
b = bytes(b,'utf-8') 

uart.write(b);
while True:
    print(uart.readline())
    time.sleep(1)

