
from collections import deque
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

#################### Initailizing sensor communication protocols. ########################

# Accelerometer/Gyroscope Module
i2c = busio.I2C(scl=board.GP15, sda=board.GP14)
accAndGyro = ISM(i2c)

# LoRa module
#uart =busio.UART(0,baudrate = 9600,stop = 1 ,tx = board.GP0, rx = board.GP1)

# GPS Module
# gpsMod = busio.UART( # FIll in here )
################################################################################


###################### Program begins here ######################################## 

# lock will allow us to make sure both functions don't try to update the flagBit at the same time.
lock  = _thread.allocate_lock()


#FlagBit is flipped from zero to 1 if a hazard is detected.
flagBit = 0

#FlagCounter is what counts the amount of flags we currently have.
flagCounter = 0

#Global Variables for received string. Initialized to an empty string.
receivedString = ""

#Global Variable for transmission string. Initialized to an empty string.
stringToTransmit = ""

#Boolean value for when on/off highway
onHighway = False

#hazard Flag. True = Hazard, False = No Hazard
hazard = False

#warning Flag
warning = False

#Reset bit: If reset flag is high, Hazard, flagBit, and flagCounter will be reset to default values
reset = 0

# Global Direction variable
direction = 0
    
def main_thread():
    global lock, flagBit, flagCounter, receivedString, stringToTransmit, onHighway,hazard,warning, direction
    
    highWay: bool = False #initializing highway variable to be false.
    
    #Initialize GPS
    
    # GPS module will determine whether on Highway or not Highway
    
    #get latitude and longitude
    #store previous latitude and longitude
    #dist = from GPS long/l
    
    #DecimalNumber.set_scale(7)
    prevLat = DecimalNumber(3885315,5) #fromGPS
    currLat = DecimalNumber(388255,4)
    prevLon = DecimalNumber(-773117,4)
    currLon = DecimalNumber(-773154,4)

    meanEarthRadius = 6371#km
    period = 5 #polling rate for GPS
    #dist = (math.acos(math.cos(math.radians(90 - prevLat)) * math.cos(math.radians(90- currLat)) + math.sin(math.radians(90 - prevLat)) * math.sin(math.radians(90 - currLat)) * math.cos(math.radians(prevLon - currLon))) * meanEarthRadius)  
    dist = (DecimalNumber.acos(DecimalNumber.cos((90 - prevLat)*DecimalNumber.pi()/180) * DecimalNumber.cos((90- currLat)*DecimalNumber.pi()/180) + DecimalNumber.sin((90 - prevLat)*DecimalNumber.pi()/180) * DecimalNumber.sin((90 - currLat)*DecimalNumber.pi()/180) * DecimalNumber.cos((prevLon - currLon)*DecimalNumber.pi()/180)) * meanEarthRadius)  
    speed = dist/period #get speed from GPS-alternative method
    
 
        
    #alternative, use if statements to compare degrees
    #GETTING DIRECTION - GPS METHOD
    prevTangle = tAngle
    tAngle = 1 #fromGPS OR MANUAL
    #IF STATEMENTS to SET DIRECTION
    
    
    if speed > 55:
        onHighway = True # if speed > 55, store direction EW or NS
           #GETTING DIRECTION - COORDINATE METHOD
        direction = 0 #0 = South, 1 = North, 2 = West, 3=East
        longDiff = currLon - prevLon
        latDiff = currLat - prevLat
        if math.abs(longDiff) >= math.abs(latDiff): # Going East/West
           
            if longDiff >= 0:#going East
                direction = 3
            else: #going West
                direction = 2
        else : # going North/South  
            if latDiff >= 0:#going North
                direction = 1
            else: #going South
                direction = 0
    
    
    
   #direction = 0 #0 = east, 1 = west, etc
    
    if(onHighway):#start reciever thread and initialize sensor lists
        _thread.start_new_thread(reciever_transmitter_thread,())
                
        DEQUE_SIZE = 5.0
        
        # Initializing deque (with an intended size of 5) for accelerometer x, y, and z values.
        xAcc = deque(())
        yAcc = deque(())
        
        # Initializing deque (with an intended size of 5) for gyroscope x, y, and z values.
        xGyro = deque(())
        yGyro = deque(())
        zGyro = deque(())
        
        #if deque if full, calculate avg
        #to read avg value, pop all into 5 variables, sum and avg and then readd them in same order. O(1)
        xAccSum = 0.0
        yAccSum = 0.0
        zAccSum = 0.0
        xGyroSum = 0.0
        yGyroSum = 0.0
        zGyroSum = 0.0
        # While highway is true, continuously monitor the Accelerometer/Gyroscope.
        while(onHighway):


            accel = accAndGyro.acceleration    
            gyro = accAndGyro.gyro
            
            #add x,y,z axis values to sum variables and append them to respective deques.
            xAccSum += accel[0]; xAcc.append(accel[0]);
            yAccSum += accel[1]; yAcc.append(accel[1]);
            
            xGyroSum += gyro[0]; xGyro.append(gyro[0]);
            yGyroSum += gyro[1]; yGyro.append(gyro[1]);
            zGyroSum += gyro[2]; zGyro.append(gyro[2]);    

            
            
            #print(len(xAcc))
            # Once the length of the deques has reached the maxlen, take the average.
            if(len(xAcc) == 5):
                xAccSum -= xAcc.popleft();
                yAccSum -= yAcc.popleft();
               
                #print("Accel X: %.3f, Y: %.3f, Z: %.3f" %(xAccSum, yAccSum, zAccSum))

                # Average of acceleration in X axis
                xAcc_avg = xAccSum / DEQUE_SIZE
                yAcc_avg = yAccSum / DEQUE_SIZE
                
                average = (xAcc_avg, yAcc_avg)
                #print("Average Accel X: %.3f, Y: %.3f, Z: %.3f" %(average))
                #print("\n")
                xGyroSum -= xGyro.popleft();
                yGyroSum -= yGyro.popleft();
                zGyroSum -= zGyro.popleft();
                #print("Gyro X: %.3f, Y: %.3f, Z: %.3f" %(xGyroSum, yGyroSum, zGyroSum))

                # Average of gyro in axis
                xGyro_avg = xGyroSum / DEQUE_SIZE
                yGyro_avg = yGyroSum / DEQUE_SIZE
                zGyro_avg = zGyroSum / DEQUE_SIZE 
                average = (xGyro_avg, yGyro_avg, zGyro_avg)
                #print("Average Gyro X: %.3f, Y: %.3f, Z: %.3f" %(average))
                
               

                #active state
                if xAcc_avg < -3:
                    #transmit
                    warning = True
                if zGyro_avg > math.abs(0.4):
                    #transmit
                    warning = True
                if direction == 0 or direction == 1:#stored at start of active mode: north or south
                    if currDirection  > 1 and speed > 10: # going east or west. speed check to ignore jitter at low speed.
                        onHighway = False
                        direction = currDirection    
                elif direction == 2 | direction == 3 and speed > 10: # going east or west. speed check to ignore jitter at low speed.
                    if currDirection  < 2 and speed > 10:   #going north and south
                        onHighway = False
                        direction = currDirection
                if hazard: #warn users w LED n buzzer
                    hazard = False
            time.sleep(period)
            
def reciever_transmitter_thread():
    global direction
    uart =UART(0,baudrate = 9600,stop = 1 ,tx = Pin(0),rx = Pin(1))
    #uart = UART.init(baudrate=9600, bits=8, parity=None, stop=1, Tx = 0, Rx = 1)
    sensorReading = "1,0,30.0031,20.1241,W" # global string

    uart.write(bytes("AT+MODE=TEST", "utf-8"))  #ATTEMPTING AT+MODE=TEST AUTO
    print("Checking.. AT+MODE=TEST")
    time.sleep(2)
    uart.write(bytes("AT+TEST=RXLRPKT", "utf-8")) #set in reciever mode
    


    while True:# keep recieving
        line = uart.readline() #checking for messages from Lora module
        if warning:
            break
        elif line != None: #if there is a message
            receivedString += uart.readline(); #compile/add to a string
        elif receivedString != None and line == None: #uart message is finished
            #analyze receivedString message
            left = '"3C'  #PARSING STRING
            right = '3E"'
            dataRead = re.search(
                r"" + left + "(.*?)" + right + "", receivedString
            ).group(1)
            clearstring = binascii.unhexlify(dataRead).decode("utf8")
            print(clearstring)
            
            letter_list = clearstring.split(",")    
            flag_str = letter_list[0]           #Flag bit value       
            hazard_str = letter_list[1]         #Hazard bit value
            lat_str = letter_list[2]            # GPS val
            lon_str = letter_list[3]            # GPS val
            dir_str = letter_list[4]            # Direction-  0: South, 1: North, 2: West, 3: East 

            #Printing strings of our received values
            print("flag " +  flag_str)
            print("hazard:" + hazard_str)
            print("gpsX: " + lat_str)
            print("gpsY: " + lon_str)
            print("dir: " + dir_str)

            ############### still strings, need to convert + stick in object type cast ##############

            dir_received = int(dir_str)                 # Direction in integer format  --- local
            flagBit_received = int(flag_str)             # Flag bit in integer format  --- local
            hazard_received = int(hazard_str)            # hazard bit in integer format --- local

            lat_received = float(lat_str)                   # Latitude value
            lon_received = float(lon_str)                   # Longtitude value
            
        
            ################# determine direction from the received packet ########################

            if(dir_received == direction):
                pass
                # check if the transmitter's location is behind or in front -- use GPS latitude and/or longtitude
                
                # If we are moving closer toward the hazard -- check hazard array
                # If hazard array doesn't contain incident, save data into array
                # else ignore
                
                # us being the car in front: lat = 160
                # hazard received with lat = 120

                # Depending on direction:
                # if(rec_lat - curLat < 0) :
                # this for us.
                # else we're moving away
            else:
                continue
                

            # Transmission Code:      
            # if hazard:
    # b = "AT+TEST=TXLRSTR "+bytes(binascii.hexlify(stringToTransmit.encode('utf-8'))).decode()
    # b = bytes(b,'utf-8') 
    # print(b.decode())
    # warning = False
            
    #uart.write(b);  
    # while True:
    # time.sleep(1);
    # print(uart.readline());

# 




if __name__ == "__main__":
    main_thread()

    