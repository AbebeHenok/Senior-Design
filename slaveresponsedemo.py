values = []
populatelist()
isFirstDigit = True

while True:
    string = get() 
    if(string == '0' or string == '1' or string == '2' or string == '3' or string == '4' or string == '5' or string == '6' or string == '7' or string == '8' or string == '9' or string == '0')
        lcd(string, True)
        isFirstDigit.toggle()
    elif(string == 'f'):
        backlightoff()
        list.empty()
        populatelist()
        isFirstDigit = True
    

def populatelist(self):
    global value
    while(len(value) < 6): #before list has receieved o, hazard type, dig1, dig2 AT LEAST ONCE
        string = get()
        vallen = len(value)
        if( (string == 'o' and vallen == 0) or ( (string == 'l' or string == 'r' or string == 'b') and vallen == 1) or ( (string == '0' or string == '1' or string == '2' or string == '3' or string == '4' or string == '5' or string == '6' or string == '7' or string == '8' or string == '9' or string == '0') and (vallen == 2 or vallen == 3)) )
            value.append(string)
    backlighton()
    writewarning()
    lcd(val[2], True)
    lcd(val[3], False)
    
