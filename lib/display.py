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
        LCD = LCD_3inch5()
        LCD.bl_ctrl(100)
        LCD.fill(LCD.WHITE)
        LCD.show_up()
        LCD.fill(LCD.WHITE)
        LCD.show_down()
        
    def clearLCD():
        LCD.fill(LCD.WHITE)
        dot(dotx)
        LCD.show_down()
      
    def hazard_fig(string):
        LCD.fill(LCD.WHITE)
        if(string == 'b'):
            LCD.fill_rect(145,3,175,175, LCD.BLUE)
        elif(string == 'l'):
            LCD.fill_rect(145,3,175,175, LCD.GREEN)
        elif(string == 'r'):
            LCD.fill_rect(145,3,175,175, LCD.RED)
        LCD.fill_rect(160,18, 145, 145, LCD.WHITE)
        LCD.fill_rect(225, 25, 15, 80, LCD.BLACK)
        LCD.fill_rect(225, 110, 15, 15 , LCD.BLACK)

        LCD.show_up()

    def LCD(isFirstDigit, digit):
        x = 0
        if(isFirstDigit):
            x = 145
        else:
            x = 230
        if (int(digit) == 0):
            LCD0(x)
        elif (int(digit) == 1):
            LCD1(x)
        elif (int(digit) == 2):
            LCD2(x)
        elif (int(digit) == 3):
            LCD3(x)
        elif (int(digit) == 4):
            LCD4(x)
        elif (int(digit) == 5):
            LCD5(x)
        elif (int(digit) == 6):
            LCD6(x)
        elif (int(digit) == 7):
            LCD7(x)
        elif (int(digit) == 8):
            LCD8(x)
        elif (int(digit) == 9):
            LCD9(x)
            
    def dot(x):
        LCD.fill_rect(x, segBottom, segWidth, segWidth, LCD.BLACK)
        
    def LCD1(x):
        LCD.fill_rect(x, segTop, segWidth * 2 + segHeight, segHeight * 2  + segWidth, LCD.WHITE)
        LCD.fill_rect(x + rSeg, segTop, segWidth, segHeight * 2 + segWidth,LCD.BLACK) #draws 2 right segments

    def LCD2(x):
        LCD.fill_rect(x, segTop, segWidth * 2 + segHeight, segHeight * 2  + segWidth, LCD.WHITE)
        LCD.fill_rect(x + rSeg, segTop, segWidth, segHeight + segWidth, LCD.BLACK) #draws top-right seg
        LCD.fill_rect(x, segTop + segHeight, segWidth, segHeight, LCD.BLACK) #draws bot-left seg
        LCD.fill_rect(x, segTop, segHeight, segWidth,  LCD.BLACK) #draws top-mid seg
        LCD.fill_rect(x, segTop + segHeight, segHeight, segWidth,  LCD.BLACK) #draws mid seg
        LCD.fill_rect(x, segTop + segHeight*2, segHeight + segWidth, segWidth ,  LCD.BLACK) #draws bot-mid seg

    def LCD3(x):
        LCD.fill_rect(x, segTop, segWidth * 2 + segHeight, segHeight * 2  + segWidth, LCD.WHITE)
        LCD.fill_rect(x + rSeg, segTop, segWidth, segHeight *2 + segWidth,LCD.BLACK) #draws 2 right segments
        #   LCD.fill_rect(x, segTop + segHeight, segWidth, segHeight, LCD.BLACK) #draws bot-left seg
        LCD.fill_rect(x, segTop, segHeight, segWidth,  LCD.BLACK) #draws top-mid seg
        LCD.fill_rect(x, segTop + segHeight, segHeight, segWidth,  LCD.BLACK) #draws mid seg
        LCD.fill_rect(x, segTop + segHeight*2, segHeight, segWidth,  LCD.BLACK) #draws bot-mid seg
      
    def LCD4(x):
        LCD.fill_rect(x, segTop, segWidth * 2 + segHeight, segHeight * 2  + segWidth, LCD.WHITE)
        LCD.fill_rect(x + rSeg, segTop, segWidth, segHeight * 2 + segWidth,LCD.BLACK) #draws 2 right segments
        LCD.fill_rect(x, segTop, segWidth, segHeight, LCD.BLACK) #draws top-left seg
        LCD.fill_rect(x, segTop + segHeight, segHeight, segWidth,  LCD.BLACK) #draws mid seg

    def LCD5(x):
        LCD.fill_rect(x, segTop, segWidth * 2 + segHeight, segHeight * 2  + segWidth, LCD.WHITE)
        LCD.fill_rect(x, segTop, segWidth, segHeight + segWidth, LCD.BLACK) #draws top-left seg
        LCD.fill_rect(x+ rSeg, segTop + segHeight, segWidth, segHeight, LCD.BLACK) #draws bot-right seg
        LCD.fill_rect(x, segTop, segHeight + segWidth, segWidth,  LCD.BLACK) #draws top-mid seg
        LCD.fill_rect(x, segTop + segHeight, segHeight, segWidth,  LCD.BLACK) #draws mid seg
        LCD.fill_rect(x, segTop + segHeight*2, segHeight + segWidth, segWidth,  LCD.BLACK) #draws bot-mid seg

    def LCD6(x):
        
        LCD.fill_rect(x, segTop, segWidth * 2 + segHeight, segHeight * 2  + segWidth, LCD.WHITE)
        LCD.fill_rect(x , segTop, segWidth, segHeight + segWidth, LCD.BLACK) #draws top-left seg
        LCD.fill_rect(x +rSeg, segTop + segHeight, segWidth, segHeight, LCD.BLACK) #draws bot-right seg
        LCD.fill_rect(x, segTop, segWidth, segHeight * 2 + segWidth,LCD.BLACK) #draws 2 left segments
        LCD.fill_rect(x, segTop, segHeight + segWidth, segWidth,  LCD.BLACK) #draws top-mid seg
        LCD.fill_rect(x, segTop + segHeight, segHeight, segWidth,  LCD.BLACK) #draws mid seg
        LCD.fill_rect(x, segTop + segHeight*2, segHeight + segWidth , segWidth,  LCD.BLACK) #draws bot-mid seg
      
    def LCD7(x):
        LCD.fill_rect(x, segTop, segWidth * 2 + segHeight, segHeight * 2  + segWidth, LCD.WHITE)    
        LCD.fill_rect(x + rSeg, segTop, segWidth, segHeight * 2 + segWidth,LCD.BLACK) #draws 2 right segments
        LCD.fill_rect(x, segTop, segHeight + segWidth, segWidth,  LCD.BLACK) #draws top-mid seg

    def LCD8(x):
        LCD.fill_rect(x, segTop, segWidth * 2 + segHeight, segHeight * 2  + segWidth, LCD.WHITE)
        LCD.fill_rect(x, segTop, segHeight + segWidth, segWidth,  LCD.BLACK) #draws top-mid seg
        LCD.fill_rect(x, segTop + segHeight, segHeight, segWidth,  LCD.BLACK) #draws mid seg
        LCD.fill_rect(x, segTop + segHeight*2, segHeight + segWidth , segWidth,  LCD.BLACK) #draws bot-mid seg
        LCD.fill_rect(x + rSeg, segTop, segWidth, segHeight + segWidth, LCD.BLACK) #draws top-right seg
        LCD.fill_rect(x, segTop + segHeight, segWidth, segHeight, LCD.BLACK) #draws bot-left seg
        LCD.fill_rect(x, segTop, segWidth, segHeight + segWidth, LCD.BLACK) #draws top-left seg
        LCD.fill_rect(x+ rSeg, segTop + segHeight, segWidth, segHeight, LCD.BLACK) #draws bot-right seg

    def LCD9(x):
        LCD.fill_rect(x, segTop, segWidth * 2 + segHeight, segHeight * 2  + segWidth, LCD.WHITE)
        LCD.fill_rect(x, segTop, segHeight + segWidth, segWidth,  LCD.BLACK) #draws top-mid seg
        LCD.fill_rect(x, segTop + segHeight, segHeight, segWidth,  LCD.BLACK) #draws mid seg
        LCD.fill_rect(x, segTop + segHeight*2, segHeight + segWidth , segWidth,  LCD.BLACK) #draws bot-mid seg
        LCD.fill_rect(x + rSeg, segTop, segWidth, segHeight + segWidth, LCD.BLACK) #draws top-right seg
        LCD.fill_rect(x, segTop, segWidth, segHeight + segWidth, LCD.BLACK) #draws top-left seg
        LCD.fill_rect(x+ rSeg, segTop + segHeight, segWidth, segHeight, LCD.BLACK) #draws bot-right seg
        
    def LCD0(x):
         LCD.fill_rect(x, segTop, segWidth * 2 + segHeight, segHeight * 2  + segWidth, LCD.WHITE)
         LCD.fill_rect(x, segTop, segHeight + segWidth, segWidth,  LCD.BLACK) #draws top-mid seg
         LCD.fill_rect(x, segTop + segHeight*2, segHeight + segWidth , segWidth,  LCD.BLACK) #draws bot-mid seg
         LCD.fill_rect(x + rSeg, segTop, segWidth, segHeight + segWidth, LCD.BLACK) #draws top-right seg
         LCD.fill_rect(x, segTop + segHeight, segWidth, segHeight, LCD.BLACK) #draws bot-left seg
         LCD.fill_rect(x, segTop, segWidth, segHeight + segWidth, LCD.BLACK) #draws top-left seg
         LCD.fill_rect(x+ rSeg, segTop + segHeight, segWidth, segHeight, LCD.BLACK) #draws bot-right seg
