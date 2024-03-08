############################## INTELLIGENT HIGHWAY HAZARD WARNING SYSTEM ############################## 
#
# Authors - Henok Abebe, David Ngo, Jhaysonel  Gueverra, Nhu Pham, Mohmmed Rahman, Anthony C Cruz
# 
# Discription - This program is implemented to run on Raspberry Pi Pico with a LoRa module, 6 DOF Accelerometer/Gyroscope,
# and a GPS module. The program is meant to collect data from the GPS and Accelerometer/Gyroscope modules
# and analyze drivers behavior on a highway. If the Accelerometer/Gyroscope module detects sudden changes, it will
# raise the flagBit and increment the flagCounter. When a flagBit is raised, the program goes into the comm function
# and will transmit the GPS coordinates, flagBit, and flagCounter values to other vehicles. 

# imports
from deque import deque
from machine import UART, Pin, I2C
import busio
import board
from adafruit_lsm6ds.ism330dhcx import ISM330DHCX as ISM
import time
import _thread
import math
from mpy_decimal import *
#import mpy_decimal
import adafruit_gps
import binascii
import re
import sys
sys.path.append('adafruit_gps')
import uasyncio as asyncio
import adafruit_gps as as_GPS



#################### Initailizing sensor communication protocols. ########################
# GPS module
uart_GPS = UART(1, baudrate=9600, bits=8, stop=1, parity = None, tx=Pin(4), rx=Pin(5), timeout=300)
sreader = asyncio.StreamReader(uart_GPS)  # Create a StreamReader
gps = as_GPS.AS_GPS(sreader)  # Instantiate GPS

# Accelerometer/Gyroscope Module
i2c = busio.I2C(scl=board.GP15, sda=board.GP14)
accAndGyro = ISM(i2c)

# LoRa module
#uart =busio.UART(0,baudrate = 9600,stop = 1 ,tx = board.GP0, rx = board.GP1)
uart_lora = UART(0,baudrate = 9600,stop = 1 ,tx = Pin(0),rx = Pin(1))

prevLon = 0
prevLat = 0
curLon = 0
curLat = 0

#FlagBit is flipped from zero to 1 if a hazard is detected.
flagBit = 0

#FlagCounter is what counts the amount of flags we currently have.
flagCounter = 0

#Global Variables for received string. Initialized to an empty string.
receivedString = ""

#Global Variable for transmission string. Initialized to an empty string.
sensorReading = ""

#Boolean value for when on/off highway
onHighway = False

# Checked to warn the driver - turn on LED and speakers
hazard_flag = False

#transmit flag - when hazardous behavior detected, set to true. Receiver thread checks if its true it will change mode to transmit.
transmit_flag = False

#Reset bit: If reset flag is high, Hazard, flagBit, and flagCounter will be reset to default values
reset = 0

# Global Direction variable
currDirection = 0

HazardArray = []

# Hazard Class used describe a hazardous instance 
class Hazard:
    def __init__(self, lat, lon, fcount):
        self.lat = lat
        self.lon = lon
        self.fcount = fcount


# GPS Module
# gpsMod = busio.UART( # FIll in here )
################################################################################


###################### Program begins here ######################################## 

# lock will allow us to make sure both functions don't try to update the flagBit at the same time.
lock  = _thread.allocate_lock()




async def sensor_thread():
    print('waiting for GPS data')
    #await gps.data_received(position=True, altitude=True)
    global prevLon, prevLat,currLon, currLat, warning, currDirection
    direction, prevLat, prevLon, currLat, currLon = 0
    warning = False

    while True:
      #  print('Time: {}'.format(gps.time_string()))

        prevLat = currLat
        prevLon = currLon

      #  print('Latitude: {}'.format((gps.latitude(1))[0]))
     #   print('Longitude: {}'.format((gps.longitude(1))[0]))
     #   print('Speed: {}'.format(gps.speed_string(11)))
        gpsSpeed = gps.speed_string(11)
        speed = DecimalNumber(gpsSpeed[0: (len(gpsSpeed) - 4)])
        currLat = DecimalNumber(str(gps.latitude(1)[0]))
        currLon = DecimalNumber(str(gps.longitude(1)[0]))
        #calibrating initial location
        if(prevLat == 0):
            prevLat = currLat
            prevLon = currLon
            continue
       
        print("Prev Lat ", prevLat)
        print("Prev lon ", prevLon)
        print("Curr Lat ", currLat)
        print("Curr Lon ", currLon)
        #global lock, flagBit, flagCounter

        onHighway = False #initializing highway variable to be false.

        #Initialize GPS

        # GPS module will determine whether on Highway or not Highway
        #get latitude and longitude
        #store previous latitude and longitude
        #dist = from GPS long/l

        #DecimalNumber.set_scale(7)
       # prevLat = DecimalNumber(3885315,5) #fromGPS
       # currLat = DecimalNumber(388255,4)
       # prevLon = DecimalNumber(-773117,4)
       # currLon = DecimalNumber(-773154,4)


        #alternative, use if statements to compare degrees
        #GETTING DIRECTION - GPS METHOD
        #prevTangle = tAngle;
        tAngle = 1 #fromGPS OR MANUAL
        #IF STATEMENTS to SET DIRECTION
       # speed = 60
        print("checking speed > 55")
        if speed > 55:
            onHighway = True # if speed > 55, store direction EW or NS
               #GETTING DIRECTION - COORDINATE METHOD
            direction = 0 #0 = South, 1 = North, 2 = West, 3=East
            lonDiff = currLon - prevLon
            latDiff = currLat - prevLat
            if abs(lonDiff) >= abs(latDiff): # Going East/West

                if lonDiff >= 0:#going East
                    direction = 3
                    print("going East")
                elif lonDiff < 0: #going West
                    direction = 2
                    print("going West")
            else : # going North/South
                if latDiff >= 0:#going North
                    direction = 1
                    print("going North")
                elif latDiff < 0: #going South
                    direction = 0
                    print("going South")

       #direction = 0 #0 = east, 1 = west, etc
        print("checking onHighway")
        if(onHighway):#start receiver thread and initialize sensor lists
            print("On Highway")
            _thread.start_new_thread(lora_thread,())

            DEQUE_SIZE = 5.0

        while(onHighway):

            DEQUE_SIZE = 5.0

            # Initializing deque (with an intended size of 5) for accelerometer x, y, and z values.
            xAcc = deque(())
            yAcc = deque(())

            # Initializing deque (with an intended size of 5) for gyroscope x, y, and z values.
            xGyro = deque(())
            yGyro = deque(())
            zGyro = deque(())

            #if deque if full, calculate avg
            #to read avg value, pop all into 5 variables, sum and avg and then readd them in same order. O(1

            while True:
                    accel = accAndGyro.acceleration
                    gyro = accAndGyro.gyro

                    #append x,y,z axis values  to respective deques.
                    xAcc.append(accel[0]);yAcc.append(accel[1])
                    xGyro.append(gyro[0]);yGyro.append(gyro[1]);zGyro.append(gyro[2]);



                    #print(len(xAcc))
                    # Once the length of the deques has reached the maxlen, take the average.
                    if(len(xAcc) == 6):
                        #remove oldest values
                        xAcc.popleft();yAcc.popleft();
                        xGyro.popleft();yGyro.popleft();zGyro.popleft();
                        sumAccel = (xAcc.runSum(), yAcc.runSum())
                        averageAccel = (xAcc.runAvg(), yAcc.runAvg())
                        sumGyro = (xGyro.runSum(), yGyro.runSum(), zGyro.runSum())
                        averageGyro = (xGyro.runAvg(), yGyro.runAvg())

                        print("sumAcc X: %.3f, Y: %.3f" %(sumAccel))
                        print("AverageAcc X: %.3f, Y: %.3f" %(averageAccel))
                        print("sumGyro X: %.3f, Y: %.3f, Z: %.3f" %(sumGyro))
                        print("AverageGyro X: %.3f, Y: %.3f, Z: %.3f" %(averageGyro))

                        lonDiff = currLon - prevLon
                        latDiff = currLat - prevLat
                        with lock:
                            if abs(lonDiff) >= abs(latDiff): # Going East/West

                                if lonDiff >= 0:#going East
                                    currDirection = 3
                                    print("going East")
                                elif lonDiff < 0: #going West
                                    currDirection = 2
                                    print("going West")
                            else : # going North/South
                                if latDiff >= 0:#going North
                                    currDirection = 1
                                    print("going North")
                                elif latDiff < 0: #going South
                                    currDirection = 0
                                    print("going South")

                            #active state
                            if xAcc.runAvg() < -3:
                                #transmit
                                print("XACC DETECTED")
                                warning = True
                            if abs(zGyro.runAvg()) > abs(0.4):
                                print("ZGYRO DETECTED")
                                warning = True
                            if (direction == 0 or direction == 1):#stored at start of active mode: north or south
                                if currDirection  > 1 and speed > 10: # going east or west. speed check to ignore jitter at low speed.
                                    onHighway = False
                                    direction = currDirection
                            elif direction == 2 or direction == 3 and speed > 10: # going east or west. speed check to ignore jitter at low speed.
                                if currDirection  < 2 and speed > 10:   #going north and south
                                    onHighway = False
                                    direction = currDirection
                    
        print(" about to await")
        await asyncio.sleep(5)

            
def lora_thread():
    global transmit_flag, hazard_flag, receivedString, sensorReading, currDirection, flagBit, flagCounter, currLat, currLon, HazardArray
  
    #uart = UART.init(baudrate=9600, bits=8, parity=None, stop=1, Tx = 0, Rx = 1)
    # sensorReading = "1,0,30.0031,20.1241,W" # global string
    

    uart_lora.write(bytes("AT+MODE=TEST", "utf-8"))  #ATTEMPTING AT+MODE=TEST AUTO
    print("Checking.. AT+MODE=TEST")
    time.sleep(2)
    uart_lora.write(bytes("AT+TEST=RXLRPKT", "utf-8")) #set in receiver mode
    line = uart_lora.readline() #checking for messages from Lora module
    line = uart_lora.readline() #checking for messages from Lora module
    line = uart_lora.readline() #checking for messages from Lora module
    while True:# keep recieving
       
        print("receiving")  
        line = uart_lora.readline() #checking for messages from Lora module
        #print(line)
        
        if (line != None): #if there is a message
            receivedString += uart_lora.readline(); #compile/add to a string
        elif ((receivedString != None) and (line == None)): #uart message is finished
            #analyze receivedString message
            left = '"3C'  #PARSING STRING
            right = '3E"'
            dataRead = re.search(
                r"" + left + "(.*?)" + right + "", receivedString
            ).group(1)
            clearstring = binascii.unhexlify(dataRead).decode("utf8")
            print(clearstring)
            letter_list = clearstring.split(",")
            flag_str = letter_list[0]
            hazard_str = letter_list[1]
            lat_str = letter_list[2]
            lon_str = letter_list[3]
            dir_str = letter_list[4]

            print("flag: " + flag_str)
            print("hazard: " + hazard_str)
            print("gpsX: " + lat_str)
            print("gpsY: " + lon_str)
            print("dir: " + dir_str)
            time.sleep(5)

            dir_received = int(dir_str)                 # Direction in integer format  --- local
            flagBit_received = int(flag_str)             # Flag bit in integer format  --- local
            hazard_received = int(hazard_str)            # hazard bit in integer format --- local

            lat_received = DecimalNumber(lat_str)                   # Latitude value
            lon_received = DecimalNumber(lon_str)                   # Longtitude value
            
            with lock:
                currHeading = False
                if(dir_received == currDirection):
                    hazard_location = Hazard(lat_received,lon_received,flagBit_received)
                    # check if the transmitter's location is behind or in front -- use GPS latitude and/or longtitude
                    # DIRECTION KEY: 0 = South, 1 = North, 2 = West, 3=East
                    # SOUTH DIRECTION
                    if(currDirection == 0):
                        if (lat_received - curLat < 0):    # CAR MOVING TOWARD HAZARD
                            currHeading = True
                    # NORTH DIRECTION
                    if(currDirection == 1):
                        if (lat_received - curLat > 0):    # CAR MOVING TOWARD HAZARD
                            currHeading = True                    
                    # WEST DIRECTION
                    if(currDirection == 2):
                        if (lon_received - curLon < 0):    # CAR MOVING TOWARD HAZARD
                            currHeading = True
                    # EAST DIRECTION
                    if(currDirection == 3):
                        if (lon_received - curLon < 0):    # CAR MOVING TOWARD HAZARD
                            currHeading = True
                        
                    if (currHeading == True):
                        if(len(HazardArray) == 0):
                            HazardArray.append(hazard_location)
                        else:
                            for check in HazardArray:
                                if(check.lat == hazard_location.lat and check.lon == hazard_location.lon):    # NEED TO CHANGE TO A RANGE OF LAT & LON VALUES
                                    if(check.fcount < 3):
                                        check.fcount = flagBit_received    # UPDATE COUNT VALUE IN HAZARD ARRAY
                                        if(check.fcount > 2):
                                            # WARN USER
                                            hazard_flag = True

                                else:
                                    HazardArray.append(hazard_location)
                    else:
                        inlist = False
                        for check in HazardArray:
                            if(check.lat == hazard_location.lat and check.lon == hazard_location.lon):    # NEED TO CHANGE TO A RANGE OF LAT & LON VALUES
                                inlist = True
                                index_location = HazardArray.index(check)
                        if inlist:
                            HazardArray.pop(index_location)
                else:
                    continue
        
        # if(transmit_flag or hazard):
        #     transmit_flag_function()
        #     if timeout:
        #         break    
        if((hazard_flag == 1) or (flagBit == 1)):
            with lock:
                transmit_hazard()
###################################################### End of LoRa Thread ##############################################################################################
       
def transmit_flag_function() -> bool:
    pass
    return False
# Transmit code for LoRa -- Called in LoRa thread when hazard flag or flagbit is high.
def transmit_hazard():
    lock.acquire()
    global sensorReading, flagBit, hazard, currLat, currLon, currDirection
    sensorReading = (str(flagBit) + " " + str(hazard) + " " + str(currLat) +  " " + str(currLon) +  " "+ str(currDirection))
    packet = "AT+TEST=TXLRSTR "+bytes(binascii.hexlify(sensorReading.encode('utf-8'))).decode()
    packet = bytes(packet,'utf-8') 
    print(packet.decode())
    uart_lora.write(packet)

    # Clearing transmission response
    while uart_lora.readline() != None:
        uart_lora.readline()
        
    # After transmission of hazard, reset the hazard and flagBit. 
    flagBit, hazard = 0
    
    uart_lora.write(bytes("AT+MODE=TEST","utf-8"))
    time.sleep(0.1)
    print("going back to receive mode")
    uart_lora.write(bytes("AT+MODE=RXLRPKT" , "utf-8"))
    while uart_lora.realine() != None:
        uart_lora.readline()
    lock.release()


# Possible function for Accelerometer/Gyroscope calibration.
def calibriation():
    pass


if __name__ == "__main__":
    asyncio.run(sensor_thread())
