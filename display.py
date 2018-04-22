from oled import Oled
import time
import sys

csPin = 11
dcPin = 12
sdinPin = 13
sclkPin = 15
rstPin = 16

def display():
    myScreen = Oled(csPin, dcPin, sdinPin, sclkPin, rstPin)
    myScreen.screenInit()
    myScreen.clearAll()
    lenCommand =len(sys.argv)
    for i in range(1,lenCommand,2):
        if str.upper(sys.argv[i]) =='IMAGE':
            myScreen.displayImage(fileName=sys.argv[i+1] if lenCommand>i+1 else 'git.png')
        elif str.upper(sys.argv[i]) =='CHN':
            myScreen.displayChn(chnStr =sys.argv[i+1].decode('utf8') if lenCommand>i+1 else u'\u6837\u672C')
        elif str.upper(sys.argv[i]) =='ASC':
            myScreen.displayAsc(ascStr=sys.argv[i+1] if lenCommand>i+1 else 'example')
        else:
            return 0
    return 1

if __name__ == "__main__":
    display()