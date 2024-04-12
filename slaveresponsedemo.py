from machine import Pin,SPI,PWM, mem32
import framebuf
from lcd import *

# from display import LCD_DISPLAY
import time
import gc
from i2cSlave import i2c_slave
class LCD_DISPLAY:

    def __init__(self):
        self.dig1 = 145 #self.x cordiniate of the first digit
        self.dig2 = 230 # self.x coordinate of the second digit
        self.dotx = 215
         #dimensions of a segment digit?
        self.rseg = 50 #self.x coordinate of the 2 rightmost segments.
        #lSeg = 0 #self.x coordinate of the 2 leftmost segments.
        self.segWidth = 10 #segment width
        self.segHeight= 50 #segment height
        self.segTop = 5 #height where top segment starts
        self.segBottom = 105
        self.disp = LCD_3inch5()
        self.disp.bl_ctrl(100)
        self.disp.fill(self.disp.WHITE)
        self.disp.show_up()
        self.disp.fill(self.disp.WHITE)
        self.disp.show_down()
        
    def clearLCD(self):
        self.disp.fill(self.disp.WHITE)
        self.disp.show_down()
        self.disp.show_up()
        
#     def hazard_fig(self, string):
#         self.disp.fill(self.disp.WHITE)
#         self.disp.show_up()
# #         self.disp.show_down()
# #         print("Rec should be white")
# #         time.sleep(1)
#         
#         if(string == 'b'):
#             self.disp.fill_rect(145,3,175,175, self.disp.BLUE)
#         elif(string == 'l'):
#             self.disp.fill_rect(145,3,175,175, self.disp.GREEN)
#         elif(string == 'r'):
#             self.disp.fill_rect(145,3,175,175, self.disp.RED)
#         self.disp.fill_rect(160,18, 145, 145, self.disp.WHITE)
#         self.disp.fill_rect(225, 25, 15, 80, self.disp.BLACK)
#         self.disp.fill_rect(225, 110, 15, 15 , self.disp.BLACK)
#         self.disp.show_down()
#         print("Done with hazard_fig")
# #         time.sleep(.1)
# #         self.disp.fill(self.disp.WHITE)
#         
# #         self.disp.show_down()
    def hazard_fig(self, string):
        #self.disp.fill(self.disp.WHITE)
      #  self.disp.show_up()        
        if(string == 'b'):
            self.disp.fill_rect(40,3,60,60, self.disp.BLUE)
        elif(string == 'l'):
            self.disp.fill_rect(40,3,60,60, self.disp.GREEN)
        elif(string == 'r'):
            self.disp.fill_rect(40,3,60,60, self.disp.RED)
        self.disp.show_down()    
    def dot(self):
        self.disp.fill_rect(self.dotx, self.segBottom, self.segWidth, self.segWidth, self.disp.BLACK)
        
    def LCD1(self, x):
#         self.disp.fill(self.disp.WHITE)
        self.disp.fill_rect(x, self.segTop, self.segWidth * 2 + self.segHeight, self.segHeight * 2  + self.segWidth, self.disp.WHITE)
        self.disp.fill_rect(x + self.rseg, self.segTop, self.segWidth, self.segHeight * 2 + self.segWidth,self.disp.BLACK) #draws 2 right self.segments
        
    def LCD2(self, x):
#         self.disp.fill(self.disp.WHITE)
        self.disp.fill_rect(self.x, self.segTop, self.segWidth * 2 + self.segHeight, self.segHeight * 2  + self.segWidth, self.disp.WHITE)
        self.disp.fill_rect(self.x + self.rseg, self.segTop, self.segWidth, self.segHeight + self.segWidth, self.disp.BLACK) #draws top-right self.seg
        self.disp.fill_rect(self.x, self.segTop + self.segHeight, self.segWidth, self.segHeight, self.disp.BLACK) #draws bot-left self.seg
        self.disp.fill_rect(self.x, self.segTop, self.segHeight, self.segWidth,  self.disp.BLACK) #draws top-mid self.seg
        self.disp.fill_rect(self.x, self.segTop + self.segHeight, self.segHeight, self.segWidth,  self.disp.BLACK) #draws mid self.seg
        self.disp.fill_rect(self.x, self.segTop + self.segHeight*2, self.segHeight + self.segWidth, self.segWidth ,  self.disp.BLACK) #draws bot-mid self.seg

    def LCD3(self, x):
#         self.disp.fill(self.disp.WHITE)
        self.disp.fill_rect(self.x, self.segTop, self.segWidth * 2 + self.segHeight, self.segHeight * 2  + self.segWidth, self.disp.WHITE)
        self.disp.fill_rect(self.x + self.rseg, self.segTop, self.segWidth, self.segHeight *2 + self.segWidth,self.disp.BLACK) #draws 2 right segments        #   self.disp.fill_rect(self.x, self.segTop + self.segHeight, self.segWidth, self.segHeight, self.disp.BLACK) #draws bot-left self.seg
        self.disp.fill_rect(self.x, self.segTop, self.segHeight, self.segWidth,  self.disp.BLACK) #draws top-mid self.seg
        self.disp.fill_rect(self.x, self.segTop + self.segHeight, self.segHeight, self.segWidth,  self.disp.BLACK) #draws mid self.seg
        self.disp.fill_rect(self.x, self.segTop + self.segHeight*2, self.segHeight, self.segWidth,  self.disp.BLACK) #draws bot-mid self.seg
      
    def LCD4(self, x):
#         self.disp.fill(self.disp.WHITE)
        self.disp.fill_rect(self.x, self.segTop, self.segWidth * 2 + self.segHeight, self.segHeight * 2  + self.segWidth, self.disp.WHITE)
        self.disp.fill_rect(self.x + self.rseg, self.segTop, self.segWidth, self.segHeight * 2 + self.segWidth,self.disp.BLACK) #draws 2 right self.segments
        self.disp.fill_rect(self.x, self.segTop, self.segWidth, self.segHeight, self.disp.BLACK) #draws top-left self.seg
        self.disp.fill_rect(self.x, self.segTop + self.segHeight, self.segHeight, self.segWidth,  self.disp.BLACK) #draws mid self.seg

    def LCD5(self, x):
#         self.disp.fill(self.disp.WHITE)
        self.disp.fill_rect(self.x, self.segTop, self.segWidth * 2 + self.segHeight, self.segHeight * 2  + self.segWidth, self.disp.WHITE)
        self.disp.fill_rect(self.x, self.segTop, self.segWidth, self.segHeight + self.segWidth, self.disp.BLACK) #draws top-left self.seg
        self.disp.fill_rect(self.x+ self.rseg, self.segTop + self.segHeight, self.segWidth, self.segHeight, self.disp.BLACK) #draws bot-right self.seg
        self.disp.fill_rect(self.x, self.segTop, self.segHeight + self.segWidth, self.segWidth,  self.disp.BLACK) #draws top-mid self.seg
        self.disp.fill_rect(self.x, self.segTop + self.segHeight, self.segHeight, self.segWidth,  self.disp.BLACK) #draws mid self.seg
        self.disp.fill_rect(self.x, self.segTop + self.segHeight*2, self.segHeight + self.segWidth, self.segWidth,  self.disp.BLACK) #draws bot-mid self.seg

    def LCD6(self, x):
#         self.disp.fill(self.disp.WHITE)
        self.disp.fill_rect(self.x, self.segTop, self.segWidth * 2 + self.segHeight, self.segHeight * 2  + self.segWidth, self.disp.WHITE)
        self.disp.fill_rect(self.x , self.segTop, self.segWidth, self.segHeight + self.segWidth, self.disp.BLACK) #draws top-left self.seg
        self.disp.fill_rect(self.x +self.rseg, self.segTop + self.segHeight, self.segWidth, self.segHeight, self.disp.BLACK) #draws bot-right self.seg
        self.disp.fill_rect(self.x, self.segTop, self.segWidth, self.segHeight * 2 + self.segWidth,self.disp.BLACK) #draws 2 left self.segments
        self.disp.fill_rect(self.x, self.segTop, self.segHeight + self.segWidth, self.segWidth,  self.disp.BLACK) #draws top-mid self.seg
        self.disp.fill_rect(self.x, self.segTop + self.segHeight, self.segHeight, self.segWidth,  self.disp.BLACK) #draws mid self.seg
        self.disp.fill_rect(self.x, self.segTop + self.segHeight*2, self.segHeight + self.segWidth , self.segWidth,  self.disp.BLACK) #draws bot-mid self.seg
      
    def LCD7(self, x):
#         self.disp.fill(self.disp.WHITE)
        self.disp.fill_rect(self.x, self.segTop, self.segWidth * 2 + self.segHeight, self.segHeight * 2  + self.segWidth, self.disp.WHITE)    
        self.disp.fill_rect(self.x + self.rseg, self.segTop, self.segWidth, self.segHeight * 2 + self.segWidth,self.disp.BLACK) #draws 2 right self.segments
        self.disp.fill_rect(self.x, self.segTop, self.segHeight + self.segWidth, self.segWidth,  self.disp.BLACK) #draws top-mid self.seg

    def LCD8(self, x):
#         self.disp.fill(self.disp.WHITE)
        self.disp.fill_rect(self.x, self.segTop, self.segWidth * 2 + self.segHeight, self.segHeight * 2  + self.segWidth, self.disp.WHITE)
        self.disp.fill_rect(self.x, self.segTop, self.segHeight + self.segWidth, self.segWidth,  self.disp.BLACK) #draws top-mid self.seg
        self.disp.fill_rect(self.x, self.segTop + self.segHeight, self.segHeight, self.segWidth,  self.disp.BLACK) #draws mid self.seg
        self.disp.fill_rect(self.x, self.segTop + self.segHeight*2, self.segHeight + self.segWidth , self.segWidth,  self.disp.BLACK) #draws bot-mid self.seg
        self.disp.fill_rect(self.x + self.rseg, self.segTop, self.segWidth, self.segHeight + self.segWidth, self.disp.BLACK) #draws top-right self.seg
        self.disp.fill_rect(self.x, self.segTop + self.segHeight, self.segWidth, self.segHeight, self.disp.BLACK) #draws bot-left self.seg
        self.disp.fill_rect(self.x, self.segTop, self.segWidth, self.segHeight + self.segWidth, self.disp.BLACK) #draws top-left self.seg
        self.disp.fill_rect(self.x+ self.rseg, self.segTop + self.segHeight, self.segWidth, self.segHeight, self.disp.BLACK) #draws bot-right self.seg

    def LCD9(self, x):
#         self.disp.fill(self.disp.WHITE)
        self.disp.fill_rect(self.x, self.segTop, self.segWidth * 2 + self.segHeight, self.segHeight * 2  + self.segWidth, self.disp.WHITE)
        self.disp.fill_rect(self.x, self.segTop, self.segHeight + self.segWidth, self.segWidth,  self.disp.BLACK) #draws top-mid self.seg
        self.disp.fill_rect(self.x, self.segTop + self.segHeight, self.segHeight, self.segWidth,  self.disp.BLACK) #draws mid self.seg
        self.disp.fill_rect(self.x, self.segTop + self.segHeight*2, self.segHeight + self.segWidth , self.segWidth,  self.disp.BLACK) #draws bot-mid self.seg
        self.disp.fill_rect(self.x + self.rseg, self.segTop, self.segWidth, self.segHeight + self.segWidth, self.disp.BLACK) #draws top-right self.seg
        self.disp.fill_rect(self.x, self.segTop, self.segWidth, self.segHeight + self.segWidth, self.disp.BLACK) #draws top-left self.seg
        self.disp.fill_rect(self.x+ self.rseg, self.segTop + self.segHeight, self.segWidth, self.segHeight, self.disp.BLACK) #draws bot-right self.seg
        
    def LCD0(self,x):
        # self.disp.fill_rect(self.x, self.segTop, segWidth * 2 + self.segHeight,  
         self.disp.fill_rect(self.x, self.segTop, self.segWidth * 2 + self.segHeight, self.segHeight * 2  + self.segWidth, self.disp.WHITE)
         self.disp.fill_rect(self.x, self.segTop, self.segHeight + self.segWidth, self.segWidth,  self.disp.BLACK) #draws top-mid self.seg
         self.disp.fill_rect(self.x, self.segTop + self.segHeight*2, self.segHeight + self.segWidth , self.segWidth,  self.disp.BLACK) #draws bot-mid self.seg
         self.disp.fill_rect(self.x + self.rseg, self.segTop, self.segWidth, self.segHeight + self.segWidth, self.disp.BLACK) #draws top-right self.seg
         self.disp.fill_rect(self.x, self.segTop + self.segHeight, self.segWidth, self.segHeight, self.disp.BLACK) #draws bot-left self.seg
         self.disp.fill_rect(self.x, self.segTop, self.segWidth, self.segHeight + self.segWidth, self.disp.BLACK) #draws top-left self.seg
         self.disp.fill_rect(self.x+ self.rseg, self.segTop + self.segHeight, self.segWidth, self.segHeight, self.disp.BLACK) #draws bot-right self.seg
         

    def LCD(self, digit, isFirstDigit):
        self.x = 0
        time.sleep(1)
        if(isFirstDigit):
            self.x = self.dig1
        else:
            self.x = self.dig2
#         print("self.x: ", self.x)
#         self.dot(self.dotx)
        if (digit == '0'):
           self.LCD0(self.x)
           self.disp.show_down()
        elif (digit == '1'):
           self.LCD1(self.x)
           self.disp.show_down()
        elif (digit == '2'):
           self.LCD2(self.x)
           self.disp.show_down()
        elif (digit == '3'):
           self.LCD3(self.x)
           self.disp.show_down()
        elif (digit == '4'):
           self.LCD4(self.x)
           self.disp.show_down()
        elif (digit == '5'):
           self.LCD5(self.x)
           self.disp.show_down()
        elif (digit == '6'):
           self.LCD6(self.x)
           self.disp.show_down()
        elif (digit == '7'):
           self.LCD7(self.x)
           self.disp.show_down()
        elif (digit == '8'):
           self.LCD8(self.x)
           self.disp.show_down()
        elif (digit == '9'):
           self.LCD9(self.x)
           self.disp.show_down()


value = []
slavescl = Pin(1, Pin.PULL_UP)
slavesda = Pin(0,  Pin.PULL_UP)
# isFirstDigit = True
s_i2c = i2c_slave(0,sda=0,scl=1,slaveAddress=0x41)
display = LCD_DISPLAY()
def main():

    t1 = time.time()
    counter = 0
    first = True;
    display.dot()
    try:
        while True:
            string = chr(s_i2c.get()) #either update numbers or f, which means clear list and repopulate it again before writing to display once more.
            if(string == '0' or string == '1' or string == '2' or string == '3' or string == '4' or string == '5' or string == '6' or string == '7' or string == '8' or string == '9' or string == '0'):
                display.LCD(string, isFirstDigit)
                print("Upadating display ", string)
                isFirstDigit = not isFirstDigit
            elif(string == 'f'):
                value.clear()
                print("Turning off display")
                display.disp.bl_ctrl(0)
                print("Clearing value, ", value)
                populatelist()
                isFirstDigit = True
    except KeyboardInterrupt:
        gc.collect()
        print("Done")
        pass

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
#     display.disp.fill(display.disp.WHITE)
#     time.sleep(1)
#         writewarning(val[0])
    display.hazard_fig(value[1])
    print("populate hazard_fig")
#     time.sleep(1)
    display.LCD(value[2], True)
    display.LCD(value[3], False)
#         lcd(val[2], True)
#         lcd(val[3], False)


if __name__ == "__main__":
    main()
    
