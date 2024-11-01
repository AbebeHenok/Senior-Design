from machine import Pin,SPI,PWM
import framebuf
import time
import os
# from main_3inch5 import *
# from sdcard import *
from lcd import *


#dimensions of a segment digit?
rSeg = 50 #x coordinate of the 2 rightmost segments.
#lSeg = 0 #x coordinate of the 2 leftmost segments.
segWidth = 10 #segment width
segHeight= 50 #segment height
segTop = 5 #height where top segment starts
segBottom = 105

dig1 = 145 #x cordiniate of the first digit
dig2 = 230 # x coordinate of the second digit

dotx = 215


note_freq = {
  "A4": 440,
  "C5": 523,
  "D5": 587,
  "E5": 659,
  "R": 100
}
tune = [["D5", 0.5], ["C5", 0.5], ["D5", 0.5], ["R", 0.5], ["D5", 0.5], ["C5", 0.5], ["D5", 0.5],
         ["R", 0.5], ["D5", 0.5], ["C5", 0.5], ["A4", 0.5], ["C5", 0.5], ["E5", 0.5], ["C5", 0.5], ["D5", 2]]
speaker = machine.PWM(machine.Pin(14))  
def play_note(note_name, duration):
    frequancy = note_freq[note_name]
    if note_name == "R":
        speaker.duty_u16(0)
    else:
        speaker.duty_u16(int(65535/2))
    
    speaker.freq(frequancy)
    time.sleep(duration)
    
# "


def clearLCD():
    LCD.fill(LCD.WHITE)
    dot(dotx)
    LCD.show_down()
  
def hazard_fig():
    LCD.fill(LCD.WHITE)

    LCD.fill_rect(145,3,175,175, LCD.RED)
    LCD.fill_rect(160,18, 145, 145, LCD.WHITE)
    LCD.fill_rect(225, 25, 15, 80, LCD.BLACK)

    LCD.fill_rect(225, 110, 15, 15 , LCD.BLACK)

    LCD.show_up()

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
    
if __name__ == "__main__":  
    LCD = LCD_3inch5()
    LCD.bl_ctrl(100)
    LCD.fill(LCD.WHITE)
    LCD.show_up()
    LCD.fill(LCD.WHITE)
    LCD.show_down()
    print("here")
    
    
    prev = time.time()
    t3 = 10000
    while True:
        curr = time.time()
        
        if(curr - prev >= 1):
            prev = curr
            t3 -= 1000
            if(t3 == 9000):
                LCD.fill(LCD.WHITE)
                LCD0(dig1)
                dot(dotx)
                LCD1(dig2)
                LCD.show_down()
                
            elif(t3 == 8000):
                LCD.fill(LCD.WHITE)
                LCD2(dig1)
                dot(dotx)
                LCD3(dig2)
                LCD.show_down()
            elif(t3 == 7000):
                LCD.fill(LCD.WHITE)
                LCD4(dig1)
                dot(dotx)
                LCD5(dig2)
                LCD.show_down()
            elif (t3 == 6000):
                LCD.fill(LCD.WHITE)
                LCD6(dig1)
                dot(dotx)
                LCD7(dig2)
                LCD.show_down()
            elif(t3 == 5000):
                LCD.fill(LCD.WHITE)
                LCD8(dig1)
                dot(dotx)
                LCD9(dig2)
                LCD.show_down()    
