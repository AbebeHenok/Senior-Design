from machine import Pin,SPI,PWM
import framebuf
from lcd import *


class LCD_DISPLAY:
    dig1 = 145 #x cordiniate of the first digit
    dig2 = 230 # x coordinate of the second digit
    dotx = 215
     #dimensions of a segment digit?
    rSeg = 50 #x coordinate of the 2 rightmost segments.
    #lSeg = 0 #x coordinate of the 2 leftmost segments.
    segWidth = 10 #segment width
    segHeight= 50 #segment height
    segTop = 5 #height where top segment starts
    segBottom = 105
   
    def __init__(self):
        self.disp = LCD_3inch5()
        self.disp.bl_ctrl(100)
        self.disp.fill(self.disp.WHITE)
        self.disp.show_up()
        self.disp.fill(self.disp.WHITE)
        self.disp.show_down()
        
    def clearLCD(self):
        self.disp.fill(self.disp.WHITE)
        self.disp.show_down()
      
    def hazard_fig(self, string):
        self.disp.fill(self.disp.WHITE)
        if(string == 'b'):
            self.disp.fill_rect(145,3,175,175, self.disp.BLUE)
        elif(string == 'l'):
            self.disp.fill_rect(145,3,175,175, self.disp.GREEN)
        elif(string == 'r'):
            self.disp.fill_rect(145,3,175,175, self.disp.RED)
        self.disp.fill_rect(160,18, 145, 145, self.disp.WHITE)
        self.disp.fill_rect(225, 25, 15, 80, self.disp.BLACK)
        self.disp.fill_rect(225, 110, 15, 15 , self.disp.BLACK)

        self.disp.show_up()

    def LCD(self, isFirstDigit, digit):
        x = 0
        if(isFirstDigit):
            x = 145
        else:
            x = 230
        if (int(digit) == 0):
            disp0(x)
        elif (int(digit) == 1):
            disp1(x)
        elif (int(digit) == 2):
            disp2(x)
        elif (int(digit) == 3):
            disp3(x)
        elif (int(digit) == 4):
            disp4(x)
        elif (int(digit) == 5):
            disp5(x)
        elif (int(digit) == 6):
            disp6(x)
        elif (int(digit) == 7):
            disp7(x)
        elif (int(digit) == 8):
            disp8(x)
        elif (int(digit) == 9):
            disp9(x)
            
    def dot(self, x):
        self.disp.fill_rect(x, self.segBottom, self.segWidth, self.segWidth, self.disp.BLACK)
        
    def LCD1(x):
        self.disp.fill_rect(x, segTop, segWidth * 2 + segHeight, segHeight * 2  + segWidth, self.disp.WHITE)
        self.disp.fill_rect(x + rSeg, segTop, segWidth, segHeight * 2 + segWidth,self.disp.BLACK) #draws 2 right segments

    def LCD2(x):
        self.disp.fill_rect(x, segTop, segWidth * 2 + segHeight, segHeight * 2  + segWidth, self.disp.WHITE)
        self.disp.fill_rect(x + rSeg, segTop, segWidth, segHeight + segWidth, self.disp.BLACK) #draws top-right seg
        self.disp.fill_rect(x, segTop + segHeight, segWidth, segHeight, self.disp.BLACK) #draws bot-left seg
        self.disp.fill_rect(x, segTop, segHeight, segWidth,  self.disp.BLACK) #draws top-mid seg
        self.disp.fill_rect(x, segTop + segHeight, segHeight, segWidth,  self.disp.BLACK) #draws mid seg
        self.disp.fill_rect(x, segTop + segHeight*2, segHeight + segWidth, segWidth ,  self.disp.BLACK) #draws bot-mid seg

    def LCD3(x):
        self.disp.fill_rect(x, segTop, segWidth * 2 + segHeight, segHeight * 2  + segWidth, self.disp.WHITE)
        self.disp.fill_rect(x + rSeg, segTop, segWidth, segHeight *2 + segWidth,self.disp.BLACK) #draws 2 right segments
        #   self.disp.fill_rect(x, segTop + segHeight, segWidth, segHeight, self.disp.BLACK) #draws bot-left seg
        self.disp.fill_rect(x, segTop, segHeight, segWidth,  self.disp.BLACK) #draws top-mid seg
        self.disp.fill_rect(x, segTop + segHeight, segHeight, segWidth,  self.disp.BLACK) #draws mid seg
        self.disp.fill_rect(x, segTop + segHeight*2, segHeight, segWidth,  self.disp.BLACK) #draws bot-mid seg
      
    def LCD4(x):
        self.disp.fill_rect(x, segTop, segWidth * 2 + segHeight, segHeight * 2  + segWidth, self.disp.WHITE)
        self.disp.fill_rect(x + rSeg, segTop, segWidth, segHeight * 2 + segWidth,self.disp.BLACK) #draws 2 right segments
        self.disp.fill_rect(x, segTop, segWidth, segHeight, self.disp.BLACK) #draws top-left seg
        self.disp.fill_rect(x, segTop + segHeight, segHeight, segWidth,  self.disp.BLACK) #draws mid seg

    def LCD5(x):
        self.disp.fill_rect(x, segTop, segWidth * 2 + segHeight, segHeight * 2  + segWidth, self.disp.WHITE)
        self.disp.fill_rect(x, segTop, segWidth, segHeight + segWidth, self.disp.BLACK) #draws top-left seg
        self.disp.fill_rect(x+ rSeg, segTop + segHeight, segWidth, segHeight, self.disp.BLACK) #draws bot-right seg
        self.disp.fill_rect(x, segTop, segHeight + segWidth, segWidth,  self.disp.BLACK) #draws top-mid seg
        self.disp.fill_rect(x, segTop + segHeight, segHeight, segWidth,  self.disp.BLACK) #draws mid seg
        self.disp.fill_rect(x, segTop + segHeight*2, segHeight + segWidth, segWidth,  self.disp.BLACK) #draws bot-mid seg

    def LCD6(x):
        
        self.disp.fill_rect(x, segTop, segWidth * 2 + segHeight, segHeight * 2  + segWidth, self.disp.WHITE)
        self.disp.fill_rect(x , segTop, segWidth, segHeight + segWidth, self.disp.BLACK) #draws top-left seg
        self.disp.fill_rect(x +rSeg, segTop + segHeight, segWidth, segHeight, self.disp.BLACK) #draws bot-right seg
        self.disp.fill_rect(x, segTop, segWidth, segHeight * 2 + segWidth,self.disp.BLACK) #draws 2 left segments
        self.disp.fill_rect(x, segTop, segHeight + segWidth, segWidth,  self.disp.BLACK) #draws top-mid seg
        self.disp.fill_rect(x, segTop + segHeight, segHeight, segWidth,  self.disp.BLACK) #draws mid seg
        self.disp.fill_rect(x, segTop + segHeight*2, segHeight + segWidth , segWidth,  self.disp.BLACK) #draws bot-mid seg
      
    def LCD7(x):
        self.disp.fill_rect(x, segTop, segWidth * 2 + segHeight, segHeight * 2  + segWidth, self.disp.WHITE)    
        self.disp.fill_rect(x + rSeg, segTop, segWidth, segHeight * 2 + segWidth,self.disp.BLACK) #draws 2 right segments
        self.disp.fill_rect(x, segTop, segHeight + segWidth, segWidth,  self.disp.BLACK) #draws top-mid seg

    def LCD8(x):
        self.disp.fill_rect(x, segTop, segWidth * 2 + segHeight, segHeight * 2  + segWidth, self.disp.WHITE)
        self.disp.fill_rect(x, segTop, segHeight + segWidth, segWidth,  self.disp.BLACK) #draws top-mid seg
        self.disp.fill_rect(x, segTop + segHeight, segHeight, segWidth,  self.disp.BLACK) #draws mid seg
        self.disp.fill_rect(x, segTop + segHeight*2, segHeight + segWidth , segWidth,  self.disp.BLACK) #draws bot-mid seg
        self.disp.fill_rect(x + rSeg, segTop, segWidth, segHeight + segWidth, self.disp.BLACK) #draws top-right seg
        self.disp.fill_rect(x, segTop + segHeight, segWidth, segHeight, self.disp.BLACK) #draws bot-left seg
        self.disp.fill_rect(x, segTop, segWidth, segHeight + segWidth, self.disp.BLACK) #draws top-left seg
        self.disp.fill_rect(x+ rSeg, segTop + segHeight, segWidth, segHeight, self.disp.BLACK) #draws bot-right seg

    def LCD9(x):
        self.disp.fill_rect(x, segTop, segWidth * 2 + segHeight, segHeight * 2  + segWidth, self.disp.WHITE)
        self.disp.fill_rect(x, segTop, segHeight + segWidth, segWidth,  self.disp.BLACK) #draws top-mid seg
        self.disp.fill_rect(x, segTop + segHeight, segHeight, segWidth,  self.disp.BLACK) #draws mid seg
        self.disp.fill_rect(x, segTop + segHeight*2, segHeight + segWidth , segWidth,  self.disp.BLACK) #draws bot-mid seg
        self.disp.fill_rect(x + rSeg, segTop, segWidth, segHeight + segWidth, self.disp.BLACK) #draws top-right seg
        self.disp.fill_rect(x, segTop, segWidth, segHeight + segWidth, self.disp.BLACK) #draws top-left seg
        self.disp.fill_rect(x+ rSeg, segTop + segHeight, segWidth, segHeight, self.disp.BLACK) #draws bot-right seg
        
    def LCD0(x):
         self.disp.fill_rect(x, segTop, segWidth * 2 + segHeight, segHeight * 2  + segWidth, self.disp.WHITE)
         self.disp.fill_rect(x, segTop, segHeight + segWidth, segWidth,  self.disp.BLACK) #draws top-mid seg
         self.disp.fill_rect(x, segTop + segHeight*2, segHeight + segWidth , segWidth,  self.disp.BLACK) #draws bot-mid seg
         self.disp.fill_rect(x + rSeg, segTop, segWidth, segHeight + segWidth, self.disp.BLACK) #draws top-right seg
         self.disp.fill_rect(x, segTop + segHeight, segWidth, segHeight, self.disp.BLACK) #draws bot-left seg
         self.disp.fill_rect(x, segTop, segWidth, segHeight + segWidth, self.disp.BLACK) #draws top-left seg
         self.disp.fill_rect(x+ rSeg, segTop + segHeight, segWidth, segHeight, self.disp.BLACK) #draws bot-right seg
