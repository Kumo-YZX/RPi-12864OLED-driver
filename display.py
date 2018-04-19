import RPi.GPIO as GPIO
from oled import Oled
import time

csPin = 11
dcPin = 12
sdinPin = 13
sclkPin = 15
rstPin = 16
chnWord =u'\u5317\u4eac'
if __name__ == "__main__":
    myScreen = Oled(csPin, dcPin, sdinPin, sclkPin, rstPin)
    myScreen.screenInit()
    myScreen.clearAll()
    myScreen.displayImage()
    myScreen.displayChn(chnStr =chnWord, pos=[0,0], fontFile='fonts/HZK32', fontSize=32)