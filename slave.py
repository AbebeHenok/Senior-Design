from machine import mem32,Pin, I2C
from display import LCD_DISPLAY
import time


if __name__ == "__main__":
    import utime
    from machine import mem32
    from i2cSlave import i2c_slave

    display = LCD_DISPLAY()
    led = Pin(25, Pin.OUT)
    backlight = Pin(13, Pin.IN)
    slavescl = Pin(0, Pin.PULL_UP)
    slavesda = Pin(1,  Pin.PULL_UP)
    #masterscl = Pin(3,  Pin.PULL_UP)
    #mastersda = Pin(2, Pin.PULL_UP)
    s_i2c = i2c_slave(0,sda=1,scl=0,slaveAddress=0x41)
    #masteri2c = I2C(1, freq=100000, scl=Pin(3), sda=Pin(2), timeout=100000)
    time.sleep(1)        
    #print(masteri2c.scan())
    
#receive z, turn lcd on
# recieve x, turn lcd off
    isFirstDigit = True
    try:
        #while True:
#                 #masteri2c.writeto(0x41, '1')
            #time.sleep(2)
            #led.toggle()
            #string = chr(s_i2c.get())
            string = 'o'
            if string == 'o':
                print("turning on display")
                backlight.on()
                display.clearLCD()
                display.dot()
                isFirstDigit = True               
            elif string == 'f':
                print("turning off display")
                backlight.off()
                display.clearLCD()

            elif string == 'l' or string == 'r' or string == 'b':
                isFirstDigit = True
                display.hazard_fig(string)
                
            else:
                if string == '0':   
                    print(isFirstDigit, string)
                    display.LCD(isFirstDigit, string)
                elif string == '1':
                    print(isFirstDigit, string)
                    display.LCD(isFirstDigit, string)
                elif string == '2':
                    print(isFirstDigit, string)
                    display.LCD(isFirstDigit, string)
                elif string == '3':
                    print(isFirstDigit, string)
                    display.LCD(isFirstDigit, string)
                elif string == '4':
                    print(isFirstDigit, string)
                    display.LCD(isFirstDigit, string)
                elif string == '5':
                    print(isFirstDigit, string)
                    display.LCD(isFirstDigit, string)
                elif string == '6':
                    print(isFirstDigit, string)
                    display.LCD(isFirstDigit, string)
                elif string == '7':
                    print(isFirstDigit, string)
                    display.LCD(isFirstDigit, string)
                elif string == '8':
                    print(isFirstDigit, string)
                    display.LCD(isFirstDigit, string)
                elif string == '9':
                    print(isFirstDigit, string)
                    display.LCD(isFirstDigit, string)
                else:
                    print("not number")
                isFirstDigit = not isFirstDigit
    except KeyboardInterrupt:
        pass
        

