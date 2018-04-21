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
    if len(sys.argv)>1 and str.upper(sys.argv[1]) =='IMAGE':
        myScreen.displayImage(fileName=sys.argv[2] if len(sys.argv)>2 else 'git.png')
    elif len(sys.argv)>1 and str.upper(sys.argv[1]) =='CHN':
        myScreen.displayChn(chnStr =sys.argv[2].decode('utf8') if len(sys.argv)>2 else u'\u6837\u672C')
    else:
        myScreen.displayAsc(ascStr=sys.argv[1] if len(sys.argv)>1 else 'example')

if __name__ == "__main__":
    display()