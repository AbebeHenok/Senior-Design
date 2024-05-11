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

currLat = 0
currLon = 0
currDirection = 0
lock  = _thread.allocate_lock()

# Hazard Class used describe a hazardous instance 
class Hazard:
    def __init__(self, direction, lat, lon, flag_counter):      
        self.direction = direction
        self.lat = lat
        self.lon = lon
        self.flag_counter = flag_counter



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
    hazard_location = Hazard(dir_received,lat_received,lon_received,flag_received)
    print("Hazard Location: ", hazard_location)
    if(fromAhead(hazard_location)): #message is from a car up ahead going the same direction.
        print("Hazard is Ahead!")
        
        
def fromAhead(hazard_location):
    global currDirection, currLat, currLon
    print("Current Lat: ", currLat)
    print("Current Lon: ", currLon)
    print("Current Direction: ", currDirection)
    print("Hazad location lat: ", hazard_location.lat)
    print("Hazard location lon: ", hazard_location.lon)
    with lock:
        print("From head locked")
        if(hazard_location.direction == currDirection):           
            # check if the transmitter's location is behind or in front -- use GPS latitude and/or longtitude
            # DIRECTION KEY: 0 = South, 1 = North, 2 = West, 3=East
            # SOUTH DIRECTION
            print("Hazard Received Matches Current Direction.")
            if(currDirection == 0):
                print("Lat Distance Between Hazard and Current Location", (hazard_location.lat-currLat))
                if (hazard_location.lat- currLat < 0):    # CAR MOVING TOWARD HAZARD
                    print("hazard is south of current location")
                    return True
                else:
                    print("hazard is north of current location")
            # NORTH DIRECTION
            if(currDirection == 1):
                print("Lat Distance Between Hazard and Current Location", (hazard_location.lat-currLat))
                if (hazard_location.lat - currLat >= 0):    # CAR MOVING TOWARD HAZARD
                    print("hazard is north of current location")
                    return True
                else:
                    print("hazard is south of current location")
            # WEST DIRECTION
            elif(currDirection == 2):
                print("Lon Distance Between Hazard and Current Location", (hazard_location.lon-currLon))
                if (hazard_location.lon - currLon < 0):    # CAR MOVING TOWARD HAZARD
                    print("hazard is west of current location")
                    return True
                else:
                    print("hazard is east of current location")
            # EAST DIRECTION
            elif(currDirection == 3):
                print("Lon Distance Between Hazard and Current Location", (hazard_location.lon-currLon))
                if (hazard_location.lon - currLon >= 0):    # CAR MOVING TOWARD HAZARD
                   print("hazard is east of current location")
                   return True
                else:
                   print("hazard is west of current location")
            return False


uart =UART(0,baudrate = 9600,stop = 1 ,tx = Pin(16),rx = Pin(17))
    #uart = UART.init(baudrate=9600, bits=8, parity=None, stop=1, Tx = 0, Rx = 1)
#currLat and Lon is 0,0. Default direction is south
#sensorReading = "2,47.6061,-122.3328,1" # global string #Seattle, northwest
sensorReading = "0,-34.6037,-58.3816,1" # global string # Buenos Aires southwest
#sensorReading = "3,55.7558,37.6173,1" # global string #Moscow northeast
#sensorReading = "1,-33.8688,151.2093,1" # global string #Sydney southeast

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


