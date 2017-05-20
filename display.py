import RPi.GPIO as GPIO
from oled import OLED_Init, OLED_Clear, OLED_Set_Pos, OLED_WR_Byte
import time
import matplotlib.image as mpimg
import numpy as np

PinCS = 11
PinDC = 12
PinSDIN = 13
PinSCLK = 15
PinRst = 16
OLEDCMD = 0
OLEDDATA = 1

if __name__ == "__main__":
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	GPIO.setup(PinCS, GPIO.OUT)
	GPIO.setup(PinDC, GPIO.OUT)
	GPIO.setup(PinSCLK, GPIO.OUT)
	GPIO.setup(PinSDIN, GPIO.OUT)
	GPIO.setup(PinRst, GPIO.OUT)
	OLED_Init()
	OLED_Clear()
	FiNam = 'ba0429.pmg'
	RaPic = mpimg.imread(FiNam)
	RaPic.shape
	DuPic = range(8192)
	for j in range(128):
		for i in range(64):
			if (RaPic[i,j,1]+RaPic[i,j,2]+RaPic[i,j,3] > 1.5):
				DuPic[j*64+i] = 1
			else:
				DuPic[j*64+i] = 0
	for x in range(128):
		for y in range(8):
			Dat = 1*DuPic[x*64+y*8+0]+2*DuPic[x*64+y*8+1]+4*DuPic[x*64+y*8+2]+8*DuPic[x*64+y*8+3]+16*DuPic[x*64+y*8+4]+32*DuPic[x*64+y*8+5]+64*DuPic[x*64+y*8+6]+128*DuPic[x*64+y*8+7]
			OLED_Set_Pos(x,y)
			OLED_WR_Byte(Dat, 1)
#	time.sleep(0.1)
	GPIO.cleanup()
	print 'Done...'