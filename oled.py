import RPi.GPIO as GPIO
import time

PinCS = 11
PinDC = 12
PinSDIN = 13
PinSCLK = 15
PinRst = 16
OLEDCMD = 0
OLEDDATA = 1

def OLED_WR_Byte(dat, cmd):
	if(cmd):
		GPIO.output(PinDC,1)
	else:
		GPIO.output(PinDC,0)
	GPIO.output(PinCS,0)
	for i in range(8):
		GPIO.output(PinSCLK,0)
		if (dat & 0x80):
			GPIO.output(PinSDIN,1)
		else:
			GPIO.output(PinSDIN,0)
		GPIO.output(PinSCLK,1)
		dat = dat << 1
	GPIO.output(PinCS,1)
	GPIO.output(PinDC,1)

def OLED_Set_Pos (x,y):
	OLED_WR_Byte(0xb0+y,OLEDCMD)
	OLED_WR_Byte(((x&0xf0)>>4)|0x10,OLEDCMD)
	OLED_WR_Byte((x&0x0f)|0x01,OLEDCMD)

def OLED_Clear():
	for i in range(8):
		OLED_WR_Byte(0xb0+i,OLEDCMD)
		OLED_WR_Byte(0x00,OLEDCMD)
		OLED_WR_Byte(0x10,OLEDCMD)
		for j in range(128):
			OLED_WR_Byte(0,OLEDDATA)

def OLED_Init():
	GPIO.output(PinRst,1)
	time.sleep(0.1)
	GPIO.output(PinRst,0)
	time.sleep(0.2)
	GPIO.output(PinRst,1)
	OLED_WR_Byte(0xAE,OLEDCMD)
	OLED_WR_Byte(0x00,OLEDCMD)
	OLED_WR_Byte(0x10,OLEDCMD)
	OLED_WR_Byte(0x40,OLEDCMD)
	OLED_WR_Byte(0x81,OLEDCMD)
	OLED_WR_Byte(0xCF,OLEDCMD)
	OLED_WR_Byte(0xA1,OLEDCMD)
	OLED_WR_Byte(0xC8,OLEDCMD)
	OLED_WR_Byte(0xA6,OLEDCMD)
	OLED_WR_Byte(0xA8,OLEDCMD)
	OLED_WR_Byte(0x3f,OLEDCMD)
	OLED_WR_Byte(0xD3,OLEDCMD)
	OLED_WR_Byte(0x00,OLEDCMD)
	OLED_WR_Byte(0xd5,OLEDCMD)
	OLED_WR_Byte(0x80,OLEDCMD)
	OLED_WR_Byte(0xD9,OLEDCMD)
	OLED_WR_Byte(0xF1,OLEDCMD)
	OLED_WR_Byte(0xDA,OLEDCMD)
	OLED_WR_Byte(0x12,OLEDCMD)
	OLED_WR_Byte(0xDB,OLEDCMD)
	OLED_WR_Byte(0x40,OLEDCMD)
	OLED_WR_Byte(0x20,OLEDCMD)
	OLED_WR_Byte(0x02,OLEDCMD)
	OLED_WR_Byte(0x8D,OLEDCMD)
	OLED_WR_Byte(0x14,OLEDCMD)
	OLED_WR_Byte(0xA4,OLEDCMD)
	OLED_WR_Byte(0xA6,OLEDCMD)
	OLED_WR_Byte(0xAF,OLEDCMD)

	OLED_WR_Byte(0xAF,OLEDCMD)
	OLED_Clear
	OLED_Set_Pos(0,0)