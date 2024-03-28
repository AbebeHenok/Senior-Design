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




def parse_message(receivedString):
    #TODO remember if message is a fluke, throw it away. also what if two messages conflict and the uart read is double the length.
    receivedString = str(receivedString).strip()
    print("receivedString: ", receivedString)
    left = " \""  #PARSING STRING
    right = "\""
    dataRead = re.search(
        r"" + left + "(.*?)" + right + "", receivedString
    ).group(1)
    if(dataRead == None):
        print("error: parsed message not formatted")
        return
    print(dataRead)
    dataRead = dataRead.strip()
    print(len(dataRead))
    clearstring = binascii.unhexlify(dataRead).decode("utf8")
    print(clearstring)
    letter_list = clearstring.split(",")
    
    dir_received = int(letter_list[0])                 # Direction in integer format  --- local
    lat_received = DecimalNumber(letter_list[1])                   # Latitude value
    lon_received = DecimalNumber(letter_list[2])                   # Longtitude value
    flag_received = int(letter_list[3])             # Flag bit in integer format  --- local
    print("message: ", dir_received, ",", lat_received, ",", lon_received, ",", flag_received)




uart =UART(0,baudrate = 9600,stop = 1 ,tx = Pin(0),rx = Pin(1))
    #uart = UART.init(baudrate=9600, bits=8, parity=None, stop=1, Tx = 0, Rx = 1)
sensorReading = "1,30.0031,20.1241,1" # global string
stringToTransmit = "312c352e303030303030312c342e30303030303031"


#stringToTransmit = "1 5.0000001 6.0000001"
uart.write(bytes("AT+MODE=TEST", "utf-8"))  #ATTEMPTING AT+MODE=TEST AUTO
time.sleep(1)
uart.read()
#uart.write(bytes("AT+MODE=TXLRPKT", "utf-8"))  #ATTEMPTING AT+MODE=TEST AUTO
#time.sleep(2)
b = "AT+TEST=TXLRSTR "+ binascii.hexlify(sensorReading.encode('utf-8')).decode()
b = bytes(b,'utf-8') 
print(b.decode())
#uart.read()
#time.sleep(1)
uart.write(b);
time.sleep(2)
parse_message(uart.read())

