from machine import mem32,Pin, I2C
from display import LCD_DISPLAY
import time
import gc
from i2cSlave import i2c_slave

value = []
display = LCD_DISPLAY()
slavescl = Pin(1, Pin.PULL_UP)
slavesda = Pin(0,  Pin.PULL_UP)
# isFirstDigit = True
s_i2c = i2c_slave(0,sda=0,scl=1,slaveAddress=0x41)
def populatelist():
    global value, display
#     print(value)
    while(len(value) < 4): #before list has receieved o, hazard type, dig1, dig2 AT LEAST ONCE
        string = chr(s_i2c.get())
        print(value)
        vallen = len(value)
        if(vallen == 0):
            if(string == 'o'):
                value.append(string)
                print(value)
        elif(vallen == 1):   
            if (string == 'l' or string == 'r' or string == 'b'):
                value.append(string)
                print(value)              
        elif(vallen == 2 or vallen == 3):   
            if(string == '0' or string == '1' or string == '2' or string == '3' or string == '4' or string == '5' or string == '6' or string == '7' or string == '8' or string == '9' or string == '0'):
                value.append(string)
                print(value)
            
    print("list populated", value)
    display.disp.bl_ctrl(100)
#         writewarning(val[0])
    display.hazard_fig(value[1])
    display.LCD(value[2], True)
    display.LCD(value[3], False)
#         lcd(val[2], True)
#         lcd(val[3], False)
    


if __name__ == "__main__":
    isFirstDigit = True
    display.disp.bl_ctrl(100)
    populatelist() #get an o, hazard type, and 2 digits before displaying it the first time.
    time.sleep(0.1)


    
    while True:
        string = chr(s_i2c.get()) #either update numbers or f, which means clear list and repopulate it again before writing to display once more.
        if(string == '0' or string == '1' or string == '2' or string == '3' or string == '4' or string == '5' or string == '6' or string == '7' or string == '8' or string == '9' or string == '0'):
            display.LCD(string, isFirstDigit)
            print("Upadating display ", string)
            isFirstDigit = not isFirstDigit
        elif(string == 'f'):
            value.clear()
            print("Turning off display")
            print("Clearing value, ", value)
            populatelist()
            isFirstDigit = True

