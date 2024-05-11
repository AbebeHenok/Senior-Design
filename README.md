# Senior-Design

Discription - This program is implemented to run on Raspberry Pi Pico with a LoRa module, 6 DOF Accelerometer/Gyroscope,
and a GPS module. The program is meant to collect data from the GPS and Accelerometer/Gyroscope modules
and analyze drivers behavior on a highway. If the Accelerometer/Gyroscope module detects sudden changes, it will
raise the flagBit and increment the flagCounter. When a flagBit is raised, the program goes into the comm function
and will transmit the GPS coordinates, flagBit, and flagCounter values to other vehicles. 
