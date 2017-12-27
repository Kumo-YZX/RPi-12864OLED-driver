import RPi.GPIO as GPIO
from oled import Oled
import time
import matplotlib.image as mpimg

csPin = 11
dcPin = 12
sdinPin = 13
sclkPin = 15
rstPin = 16

if __name__ == "__main__":
	myScreen = Oled(csPin, dcPin, sdinPin, sclkPin, rstPin)
	myScreen.screenInit()
	myScreen.clearAll()
	fileName = 'git.png'
	raPic = mpimg.imread(fileName)
	raPic.shape
	duPic = range(8192)
	for j in range(128):
		for i in range(64):
			if (raPic[i,j,1]+raPic[i,j,2]+raPic[i,j,0] > 1.5):
				duPic[j*64+i] = 1
			else:
				duPic[j*64+i] = 0
	for x in range(128):
		for y in range(8):
			Dat = 1*duPic[x*64+y*8+0]+2*duPic[x*64+y*8+1]+4*duPic[x*64+y*8+2]+8*duPic[x*64+y*8+3]+16*duPic[x*64+y*8+4]+32*duPic[x*64+y*8+5]+64*duPic[x*64+y*8+6]+128*duPic[x*64+y*8+7]
			myScreen.setPos(x,y)
			myScreen.writeByte(Dat, 1)
#	time.sleep(0.1)
#	GPIO.cleanup()
	print 'Display OK'