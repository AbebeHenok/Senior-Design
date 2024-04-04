from machine import Pin,SPI,PWM
import framebuf
from LCD import *


class LCD_DISPLAY:
    dig1 = 145 #x cordiniate of the first digit
    dig2 = 230 # x coordinate of the second digit
    dotx = 215
     #dimensions of a self.segment digit?
    rseg = 50 #x coordinate of the 2 rightmost self.segments.
    #lseg = 0 #x coordinate of the 2 leftmost self.segments.
    segWidth = 10 #self.segment width
    segHeight= 50 #self.segment height
    segTop = 5 #height where top self.segment starts
    segBottom = 105
    disp = LCD_3inch5()
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
        
    def dot(self):
        self.disp.fill_rect(self.dotx, self.segBottom, self.segWidth, self.segWidth, self.disp.BLACK)
        
    def LCD1(self, x):
        self.disp.fill_rect(x, self.segTop, self.segWidth * 2 + self.segHeight, self.segHeight * 2  + self.segWidth, self.disp.WHITE)
        self.disp.fill_rect(x + self.rseg, self.segTop, self.segWidth, self.segHeight * 2 + self.segWidth,self.disp.BLACK) #draws 2 right self.segments

    def LCD2(self, x):
        self.disp.fill_rect(x, self.segTop, self.segWidth * 2 + self.segHeight, self.segHeight * 2  + self.segWidth, self.disp.WHITE)
        self.disp.fill_rect(x + self.rseg, self.segTop, self.segWidth, self.segHeight + self.segWidth, self.disp.BLACK) #draws top-right self.seg
        self.disp.fill_rect(x, self.segTop + self.segHeight, self.segWidth, self.segHeight, self.disp.BLACK) #draws bot-left self.seg
        self.disp.fill_rect(x, self.segTop, self.segHeight, self.segWidth,  self.disp.BLACK) #draws top-mid self.seg
        self.disp.fill_rect(x, self.segTop + self.segHeight, self.segHeight, self.segWidth,  self.disp.BLACK) #draws mid self.seg
        self.disp.fill_rect(x, self.segTop + self.segHeight*2, self.segHeight + self.segWidth, self.segWidth ,  self.disp.BLACK) #draws bot-mid self.seg

    def LCD3(self, x):
        self.disp.fill_rect(x, self.segTop, self.segWidth * 2 + self.segHeight, self.segHeight * 2  + self.segWidth, self.disp.WHITE)
        self.disp.fill_rect(x + self.rseg, segTop, segWidth, segHeight *2 + segWidth,self.disp.BLACK) #draws 2 right segments        #   self.disp.fill_rect(x, self.segTop + self.segHeight, self.segWidth, self.segHeight, self.disp.BLACK) #draws bot-left self.seg
        self.disp.fill_rect(x, self.segTop, self.segHeight, self.segWidth,  self.disp.BLACK) #draws top-mid self.seg
        self.disp.fill_rect(x, self.segTop + self.segHeight, self.segHeight, self.segWidth,  self.disp.BLACK) #draws mid self.seg
        self.disp.fill_rect(x, self.segTop + self.segHeight*2, self.segHeight, self.segWidth,  self.disp.BLACK) #draws bot-mid self.seg
      
    def LCD4(self, x):
        self.disp.fill_rect(x, self.segTop, self.segWidth * 2 + self.segHeight, self.segHeight * 2  + self.segWidth, self.disp.WHITE)
        self.disp.fill_rect(x + self.rseg, self.segTop, self.segWidth, self.segHeight * 2 + self.segWidth,self.disp.BLACK) #draws 2 right self.segments
        self.disp.fill_rect(x, self.segTop, self.segWidth, self.segHeight, self.disp.BLACK) #draws top-left self.seg
        self.disp.fill_rect(x, self.segTop + self.segHeight, self.segHeight, self.segWidth,  self.disp.BLACK) #draws mid self.seg

    def LCD5(self, x):
        self.disp.fill_rect(x, self.segTop, self.segWidth * 2 + self.segHeight, self.segHeight * 2  + self.segWidth, self.disp.WHITE)
        self.disp.fill_rect(x, self.segTop, self.segWidth, self.segHeight + self.segWidth, self.disp.BLACK) #draws top-left self.seg
        self.disp.fill_rect(x+ self.rseg, self.segTop + self.segHeight, self.segWidth, self.segHeight, self.disp.BLACK) #draws bot-right self.seg
        self.disp.fill_rect(x, self.segTop, self.segHeight + self.segWidth, self.segWidth,  self.disp.BLACK) #draws top-mid self.seg
        self.disp.fill_rect(x, self.segTop + self.segHeight, self.segHeight, self.segWidth,  self.disp.BLACK) #draws mid self.seg
        self.disp.fill_rect(x, self.segTop + self.segHeight*2, self.segHeight + self.segWidth, self.segWidth,  self.disp.BLACK) #draws bot-mid self.seg

    def LCD6(self, x):
        
        self.disp.fill_rect(x, self.segTop, self.segWidth * 2 + self.segHeight, self.segHeight * 2  + self.segWidth, self.disp.WHITE)
        self.disp.fill_rect(x , self.segTop, self.segWidth, self.segHeight + self.segWidth, self.disp.BLACK) #draws top-left self.seg
        self.disp.fill_rect(x +self.rseg, self.segTop + self.segHeight, self.segWidth, self.segHeight, self.disp.BLACK) #draws bot-right self.seg
        self.disp.fill_rect(x, self.segTop, self.segWidth, self.segHeight * 2 + self.segWidth,self.disp.BLACK) #draws 2 left self.segments
        self.disp.fill_rect(x, self.segTop, self.segHeight + self.segWidth, self.segWidth,  self.disp.BLACK) #draws top-mid self.seg
        self.disp.fill_rect(x, self.segTop + self.segHeight, self.segHeight, self.segWidth,  self.disp.BLACK) #draws mid self.seg
        self.disp.fill_rect(x, self.segTop + self.segHeight*2, self.segHeight + self.segWidth , self.segWidth,  self.disp.BLACK) #draws bot-mid self.seg
      
    def LCD7(self, x):
        self.disp.fill_rect(x, self.segTop, self.segWidth * 2 + self.segHeight, self.segHeight * 2  + self.segWidth, self.disp.WHITE)    
        self.disp.fill_rect(x + self.rseg, self.segTop, self.segWidth, self.segHeight * 2 + self.segWidth,self.disp.BLACK) #draws 2 right self.segments
        self.disp.fill_rect(x, self.segTop, self.segHeight + self.segWidth, self.segWidth,  self.disp.BLACK) #draws top-mid self.seg

    def LCD8(self, x):
        self.disp.fill_rect(x, self.segTop, self.segWidth * 2 + self.segHeight, self.segHeight * 2  + self.segWidth, self.disp.WHITE)
        self.disp.fill_rect(x, self.segTop, self.segHeight + self.segWidth, self.segWidth,  self.disp.BLACK) #draws top-mid self.seg
        self.disp.fill_rect(x, self.segTop + self.segHeight, self.segHeight, self.segWidth,  self.disp.BLACK) #draws mid self.seg
        self.disp.fill_rect(x, self.segTop + self.segHeight*2, self.segHeight + self.segWidth , self.segWidth,  self.disp.BLACK) #draws bot-mid self.seg
        self.disp.fill_rect(x + self.rseg, self.segTop, self.segWidth, self.segHeight + self.segWidth, self.disp.BLACK) #draws top-right self.seg
        self.disp.fill_rect(x, self.segTop + self.segHeight, self.segWidth, self.segHeight, self.disp.BLACK) #draws bot-left self.seg
        self.disp.fill_rect(x, self.segTop, self.segWidth, self.segHeight + self.segWidth, self.disp.BLACK) #draws top-left self.seg
        self.disp.fill_rect(x+ self.rseg, self.segTop + self.segHeight, self.segWidth, self.segHeight, self.disp.BLACK) #draws bot-right self.seg

    def LCD9(self, x):
        self.disp.fill_rect(x, self.segTop, self.segWidth * 2 + self.segHeight, self.segHeight * 2  + self.segWidth, self.disp.WHITE)
        self.disp.fill_rect(x, self.segTop, self.segHeight + self.segWidth, self.segWidth,  self.disp.BLACK) #draws top-mid self.seg
        self.disp.fill_rect(x, self.segTop + self.segHeight, self.segHeight, self.segWidth,  self.disp.BLACK) #draws mid self.seg
        self.disp.fill_rect(x, self.segTop + self.segHeight*2, self.segHeight + self.segWidth , self.segWidth,  self.disp.BLACK) #draws bot-mid self.seg
        self.disp.fill_rect(x + self.rseg, self.segTop, self.segWidth, self.segHeight + self.segWidth, self.disp.BLACK) #draws top-right self.seg
        self.disp.fill_rect(x, self.segTop, self.segWidth, self.segHeight + self.segWidth, self.disp.BLACK) #draws top-left self.seg
        self.disp.fill_rect(x+ self.rseg, self.segTop + self.segHeight, self.segWidth, self.segHeight, self.disp.BLACK) #draws bot-right self.seg
        
    def LCD0(x):
         self.disp.fill_rect(x, self.segTop, self.segWidth * 2 + self.segHeight, self.segHeight * 2  + self.segWidth, self.disp.WHITE)
         self.disp.fill_rect(x, self.segTop, self.segHeight + self.segWidth, self.segWidth,  self.disp.BLACK) #draws top-mid self.seg
         self.disp.fill_rect(x, self.segTop + self.segHeight*2, self.segHeight + self.segWidth , self.segWidth,  self.disp.BLACK) #draws bot-mid self.seg
         self.disp.fill_rect(x + self.rseg, self.segTop, self.segWidth, self.segHeight + self.segWidth, self.disp.BLACK) #draws top-right self.seg
         self.disp.fill_rect(x, self.segTop + self.segHeight, self.segWidth, self.segHeight, self.disp.BLACK) #draws bot-left self.seg
         self.disp.fill_rect(x, self.segTop, self.segWidth, self.segHeight + self.segWidth, self.disp.BLACK) #draws top-left self.seg
         self.disp.fill_rect(x+ self.rseg, self.segTop + self.segHeight, self.segWidth, self.segHeight, self.disp.BLACK) #draws bot-right self.seg
         

    def LCD(self, isFirstDigit, digit):
        x = 0
        if(isFirstDigit):
            x = self.dig1
        else:
            x = self.dig2
        print("x: ", x)
        if (int(digit) == 0):
           self.LCD0(x)
        elif (int(digit) == 1):
           self.LCD1(x)
        elif (int(digit) == 2):
           self.LCD2(x)
        elif (int(digit) == 3):
           self.LCD3(x)
        elif (int(digit) == 4):
           self.LCD4(x)
        elif (int(digit) == 5):
           self.LCD5(x)
        elif (int(digit) == 6):
           self.LCD6(x)
        elif (int(digit) == 7):
           self.LCD7(x)
        elif (int(digit) == 8):
           self.LCD8(x)
        elif (int(digit) == 9):
           self.LCD9(x)
            
