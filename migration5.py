
############################## INTELLIGENT HIGHWAY HAZARD WARNING SYSTEM ############################## 
#
# Authors - Henok Abebe, David Ngo, Jhaysonel  Gueverra, Nhu Pham, Mohmmed Rahman, Anthony C Cruz
# 
# Discription - This program is implemented to run on Raspberry Pi Pico with a LoRa module, 6 DOF Accelerometer/Gyroscope,
# and a GPS module. The program is meant to collect data from the GPS and Accelerometer/Gyroscope modules
# and analyze drivers behavior on a highway. If the Accelerometer/Gyroscope module detects sudden changes, it will
# raise the flagBit and increment the flagCounter. When a flagBit is raised, the program goes into the comm function
# and will transmit the GPS coordinates, flagBit, and flagCounter values to other vehicles. 

#imports											 
from deque import deque
from machine import UART, Pin, I2C, SPI, PWM
import busio
import board
from adafruit_lsm6ds.ism330dhcx import ISM330DHCX as ISM
import time
from time import sleep
import _thread
import math
from mpy_decimal import *
import adafruit_gps
import binascii
import re
import sys
sys.path.append('adafruit_gps')
import uasyncio as asyncio
import adafruit_gps as as_GPS
import framebuf
import os
from display import *



#################### Initailizing sensor communication protocols. ########################
#GPS module
uart_GPS = UART(1, baudrate=9600, bits=8, stop=1, parity = None, tx=Pin(4), rx=Pin(5), timeout=300)
sreader = asyncio.StreamReader(uart_GPS)  # Create a StreamReader
gps = as_GPS.AS_GPS(sreader)  # Instantiate GPS

# Accelerometer/Gyroscope Module
i2c = busio.I2C(scl=board.GP27, sda=board.GP26)
accAndGyro = ISM(i2c)

# LoRa module
#uart =busio.UART(0,baudrate = 9600,stop = 1 ,tx = board.GP0, rx = board.GP1)
uart_lora = UART(0,baudrate = 9600,stop = 1 ,tx = Pin(0),rx = Pin(1))

# Speaker
speaker = machine.PWM(machine.Pin(14))
speaker.duty_u16(0)

#stores the current longitude/latitude and previous longitude/latitude measurements				
prevLon, prevLat, currLon, currLat = (0,)*4      
		   
# 
# #Global Variables for received string. Initialized to an empty string.
receivedString = None
# 
# #Global Variable for transmission string. Initialized to an empty string.
# sensorReading = ""
# 
# #Boolean value for when on/off highway
onHighway = False
# 
# # Checked to warn the driver - turn on LED and speakers
hazard_flag = False
# 

# 
# # Global Direction variable
currDirection = 0
# 
HazardArray = []

#index in alarm sequence, timer for alarm
alarm_seq = 0
tim = None

note_freq = {
  "A4": 440,
  "C5": 523,
  "D5": 587,
  "E5": 659,
  "R": 100
}
tune = ["A4", "C5", "A4", "R"]

#display state - true = on, false = off
display_on = False
#hazard on display
display_hazard = None
#display linger timer
display_timer = None

# Hazard Class used describe a hazardous instance 
class Hazard:
    def __init__(self, direction, lat, lon, flag_counter):      
        self.direction = direction
        self.lat = lat
        self.lon = lon
        self.flag_counter = flag_counter
		
# lock will allow us to make sure both functions don't try to update the flagBit at the same time.
lock  = _thread.allocate_lock()																				
################################################################################

###################### Program begins here ######################################## 
						  
async def sensor_thread():
    print('waiting for GPS data')
    #await gps.data_received(position=True, altitude=True)  
    global prevLon, prevLat,currLon, currLat, warning, currDirection, onHighway
    direction, prevLat, prevLon, currLat, currLon = (1,)*5        
	#onHighway indicates if vehicle is on highway.
    onHighway = False 
		
	#direction stores the original direction of the vehicle once it enters the highway.
    direction = 0	
	
    while True:
        prevLat = currLat
        prevLon = currLon
        gpsSpeed = gps.speed_string(11)
        speed = DecimalNumber(gpsSpeed[0: (len(gpsSpeed) - 4)])
        currLat = DecimalNumber(str(gps.latitude(1)[0]))
        currLon = DecimalNumber(str(gps.longitude(1)[0]))
        
        			
        print("Prev Lat ", prevLat)
        print("Prev lon ", prevLon)
        print("Curr Lat ", currLat)
        print("Curr Lon ", currLon)   
        print("speed: ", speed)
        #calibrating initial location
        if(prevLat == 0):
            prevLat = currLat
            prevLon = currLon
            continue

        if speed > 55:
            print("on Highway!")
            onHighway = True # if speed > 55, store direction EW or NS
               #GETTING DIRECTION - COORDINATE METHOD
            direction = 0 #0 = South, 1 = North, 2 = West, 3=East
            lonDiff = currLon - prevLon;
            latDiff = currLat - prevLat;
            if abs(lonDiff) >= abs(latDiff): # Going East/West
            
                if lonDiff >= 0:#going East
                    direction = 3
                    print("going East")
                else: #going West
                    direction = 2
                    print("going West")
            else : # going North/South  
                if latDiff >= 0:#going North
                    direction = 1
                    print("going North")
                else: #going South
                    direction = 0
                    print("going South")
        
       #direction = 0 #0 = east, 1 = west, etc
        print("checking onHighway")
        onHighway = True
        if(onHighway):#start receiver thread and initialize sensor lists
            print("On Highway")
            _thread.start_new_thread(lora_thread,())
            print("init sensor loop")
            DEQUE_SIZE = 5.0						 																																																																
            # Initializing deque (with an intended size of 5) for accelerometer x, y, and z values.
            xAcc = deque(()); yAcc = deque(())
            
            # Initializing deque (with an intended size of 5) for gyroscope x, y, and z values.
            xGyro = deque(()); yGyro = deque(()); zGyro = deque(())
    
            # While highway is true, continuously monitor the Accelerometer/Gyroscope.
            while(onHighway):
                print("onHighway - Sleeping")
                time.sleep(.5) #TEMPORARY TODO																		
                accel = accAndGyro.acceleration
                gyro = accAndGyro.gyro

                #append x,y,z axis values  to respective deques.
                xAcc.append(accel[0]);yAcc.append(accel[1])
                xGyro.append(gyro[0]);yGyro.append(gyro[1]);zGyro.append(gyro[2]);
                                                                                                                                                                                       
                # Once the length of the deques has reached the maxlen, take the average.
                if(len(xAcc) == 6):
                    #remove oldest values
                    xAcc.popleft();yAcc.popleft();
                    xGyro.popleft();yGyro.popleft();zGyro.popleft();
                    
                    #set current direction
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
                        else: # going North/South
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
                            hazard_flag = 1
                            transmit_flag = True
                        if abs(zGyro.runAvg()) > abs(0.4):
                            print("ZGYRO DETECTED")
                            hazard_flag = 1
                            transmit_flag = True
                        if (direction == 0 or direction == 1):#stored at start of active mode: north or south
                            if currDirection  > 1 and speed > 10: # going east or west. speed check to ignore jitter at low speed.
                                onHighway = False
                                direction = currDirection
                                print("exiting highway.")
                        elif direction == 2 or direction == 3 and speed > 10: # going east or west. speed check to ignore jitter at low speed.
                            if currDirection  < 2 and speed > 10:   #going north and south
                                onHighway = False
                                direction = currDirection
                                print("exiting highway.")
                print("offHighway - Sleeping")
                time.sleep(5) #TEMPORARY TODO
  #  await asyncio.sleep(5)  

            
def lora_thread():
    global hazard_flag, flagBit, transmitted_flag, receivedString, direction, currDirection, onHighway
    sensorReading = "1,0,30.0031,20.1241,W" # global string
    uart_lora.write(bytes("AT+MODE=TEST", "utf-8"))  #ATTEMPTING AT+MODE=TEST AUTO
    receivedString = None #RESET RECEIVED STRING
    print("Checking.. AT+MODE=TEST")
    time.sleep(1)
    print(uart_lora.read())
    uart_lora.write(bytes("AT+TEST=RXLRPKT", "utf-8")) #set in receiver mode
    time.sleep(1)
    print(uart_lora.read())   
#    while uart_lora.readline()  != None:
#        uart_lora.readline()
    while True:# keep recieving
        time.sleep(1) #temporary TODO
        print("receiving")  
        #line += str(uart_lora.readline()) #checking for messages from Lora module
        #print(line)
        receivedString = uart_lora.read()
        if(not onHighway): #check if back to non-highway; kill thread.
            print("exiting receiver thread")
            _thread.exit()
        elif((hazard_flag == 1)):#hazard detected, transmit hazard
            with lock:
                 transmit_hazard(Hazard(currDirection, currLat,currLon, 1)) #transmit current hazard (will override it if identified

        elif receivedString != None: #uart message is finished
            #analyze receivedString message - parse it, identify it with stored data (if existing), and update hazard flag.
            parse_message(receivedString)
            receivedString = None
            time.sleep(3)
									  								 
###################################################### End of LoRa Thread ##############################################################################################
	
# Transmit code for LoRa -- Called in LoRa thread when hazard flag or flagbit is high.
def transmit_hazard(hazard_location):
    lock.acquire()
    #CHECK HAZARD ARRAY FOR HAZRARD IN SAME AREA AND DIRECTION, IF SO, SEND THAT DATA WITH +1 COUNTER. oTHERWISE NEW, 0 COUNTER
    #ALSO, MAKE SURE TO RESET PREV LAT AND LON IF PAUSING SENSOR THREAD FOR STUFF
    hazard_to_transmit = identify_hazard(hazard_location, True)
    transmit_String = (str(hazard_to_transmit.direction) + "," + str(hazard_to_transmit.lat) +  "," + str(hazard_to_transmit.lon) +  ","+ str(hazard_to_transmit.flag)) #NEW HAZARD, COUNTER AT 0
    packet = "AT+TEST=TXLRSTR "+bytes(binascii.hexlify(transmit_String.encode('utf-8'))).decode()
    packet = bytes(packet,'utf-8') 
    print(packet.decode())
    uart_lora.write(packet)

    # Clearing transmission response
    while uart_lora.readline() != None:
        uart_lora.readline()
        
    # After transmission of hazard, reset the hazard and flagBit. 
    flagBit, hazard_flag = 0
    
    uart_lora.write(bytes("AT+MODE=TEST","utf-8"))
    time.sleep(2)
    uart_lora.read()
    print("going back to receive mode")
    uart_lora.write(bytes("AT+MODE=RXLRPKT" , "utf-8"))
    time.sleep(2)
    uart_lora.read()
    lock.release()

def parse_message(receivedString):
    #TODO remember if message is a fluke, throw it away. also what if two messages conflict and the uart read is double the length.
    receivedString = str(receivedString).strip()
    print("receivedString: ", receivedString)
    left = " \""  #PARSING STRING
    right = "\""
    dataRead = re.search(
        r"" + left + "(.*?)" + right + "", receivedString
    ).group(1)
    clearstring = binascii.unhexlify(binascii.unhexlify(dataRead).decode("utf8"))
    print(clearstring)
    letter_list = clearstring.split(",")
    
    dir_received = int(letter_list[0])                 # Direction in integer format  --- local
    lat_received = DecimalNumber(letter_list[1])                   # Latitude value
    lon_received = DecimalNumber(letter_list[2])                   # Longtitude value
    flag_received = int(letter_list[3])             # Flag bit in integer format  --- local
    print("message: ", dir_received, ",", lat_received, ",", lon_received, ",", flag_received)
    hazard_location = Hazard(dir_received, lat_received,lon_received, flag_received)
    if(fromAhead(hazard_location)): #message is from a car up ahead going the same direction.
        identify_hazard(hazard_location, False) #change hazard reference to old message, if identified. Updates Hazard flag if apparent. 
        
        
def fromAhead(hazard_location):
    global currDirection, currLat, currLon
    with lock:
        if(hazard_location.direction == currDirection):           
            # check if the transmitter's location is behind or in front -- use GPS latitude and/or longtitude
            # DIRECTION KEY: 0 = South, 1 = North, 2 = West, 3=East
            # SOUTH DIRECTION
            if(currDirection == 0):
                if (hazard_location.lon- currLat < 0):    # CAR MOVING TOWARD HAZARD
                    return True
            # NORTH DIRECTION
            if(currDirection == 1):
                if (hazard_location.lat - currLat > 0):    # CAR MOVING TOWARD HAZARD
                    return True                    
            # WEST DIRECTION
            elif(currDirection == 2):
                if (hazard_location.lon - currLon < 0):    # CAR MOVING TOWARD HAZARD
                    return True
            # EAST DIRECTION
            elif(currDirection == 3):
                if (hazard_location.lon - currLon < 0):    # CAR MOVING TOWARD HAZARD
                    return True
            return False

    
def identify_hazard(hazard_location, transmitting):
    global HazardArray, display_hazard
    if(len(HazardArray) == 0):
        HazardArray.append(hazard_location)
        return hazard_location # no messages to identify, its new.
    else:
        #arrLength = len(HazardArray) 
        x = 0
        while(x < len(HazardArray)):
            check = HazardArray[x]
            if(not fromAhead(check)): #TODO remove old data
                HazardArray.pop(x)
                continue
            elif((hazard_location.lat - 0.004) <= check.lat <= (hazard_location.lat + 0.004) and (hazard_location.lon - 0.004) <= check.lon <= (hazard_location.lon + 0.004)):  #within a quarter mile 
                    if(transmitting): #transmit code response (increment hazard once if indentified and return
                        if(check.flag_counter < 3):
                            check.flag_counter += 1 
                        return check
                    elif(check.flag_counter < hazard_location.flag_counter): #if hazard in array has a flag count > than what is alr in array, ignore it.
                        if(hazard_location.flag_counter > 2 and check.flag_counter != hazard_location.flag_counter): #if received message has a warning hazard threshold and has user has not been warned with it yet.
                            # WARN USER
                            display_hazard = check
                            display_on = True
                            #dot(40)
                            #hazard_fig()
                            warn_user()
                        check.flag_counter = hazard_location.flag_counter   # UPDATE COUNT VALUE IN HAZARD ARRAY
                    return check # return the identified message
            else:
                print("iterating through hazard array but not identified")
            x += 1
        return(hazard_location) #hazard not existing in array, treat it as a new message
    
    

def warn_user():
    global tim
    print("starting timer")
    tim = Timer(period=500, mode=Timer.PERIODIC, callback=alarm)
    #tim.init(period=1000, mode=Timer.PERIODIC, callback=alarm)
    #plays tune for 1s (period) per note.
    
    # one shot firing after 1000ms
    #tim.init(mode=Timer.ONE_SHOT, period=1000, #callback=speaker_off)
    
def alarm(t):
    global alarm_seq, tim
    print(alarm_seq)
    play_note(tune[alarm_seq])
    alarm_seq += 1
    if(alarm_seq == len(tune)):
        print("ending timer")
        tim.deinit()
        alarm_seq = 0
    

def play_note(note_name):
    global speaker
    frequency = note_freq[note_name]
    if note_name == "R":
        print("turning off speaker")
        speaker.duty_u16(0)
    else:
        speaker.duty_u16(int(65535/2))
    
    speaker.freq(frequency)
    
    
def disp_linger(t):
    global display_timer
    #turn off display
    #LCD OFF
    display.clearLCD()
    display_timer.deinit()
    
def turnon_display(hazard_location):
        
    def get_digit(number, n):
        return number // 10**n % 10
    global display_timer       
    #GPIO ON
    display.hazard_fig()
    display.dot(215)
    display_timer = Timer(period=1000, mode=Timer.PERIODIC, callback=update_display)

def update_display(t):
    global display_timer
  #  if(not display_on):
        #LCD.fill(LCD.WHITE) #use a transistor to disconnect display
        #gpio 28 = 0
  #      print("shutting down display.")
  #      return
    if(not fromAhead(hazard_location)):
        #TODO set 0.0 at the top
        display_timer = Timer(period=5000, mode=Timer.ONE_SHOT, callback=disp_linger)
        display.LCD0(145)
        display.LCD0(230)
        return
    else:# hazard ahead and display on
        #int(lat)\
        #update based on number distance
        with lock:        
            meanEarthRadius = DecimalNumber(str(3957.756))#miles
            dist = (math.acos(math.cos(math.radians(90 - currLat)) * math.cos(math.radians(90- hazard_location.lat)) + math.sin(math.radians(90 - currLat)) * math.sin(math.radians(90 - hazard_location.lat)) * math.cos(math.radians(currLon - hazard_location.lon))) * meanEarthRadius)  
            print(dist, " miles")
            display.LCD9(145)
            display.LCD5(230)
            #show on display                     
        return
        #LCD 0.0
        #print LCD 0.0 for 5s and then delete

asyncio.run(sensor_thread())
