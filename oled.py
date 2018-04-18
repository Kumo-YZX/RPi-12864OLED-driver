import RPi.GPIO as GPIO
import time

class Oled(object):
	def __init__(self, csPin, dcPin, sdinPin, sclkPin, rstPin):
		self.csPin = csPin
		self.dcPin = dcPin
		self.sdinPin = sdinPin
		self.sclkPin = sclkPin
		self.rstPin = rstPin
		self.oledCmd = 0
		self.oledData = 1
		print 'Init OK'

	def writeByte(self, dat, cmd):
		if(cmd):
			GPIO.output(self.dcPin, 1)
		else:
			GPIO.output(self.dcPin, 0)
		GPIO.output(self.csPin, 0)
		for i in range(8):
			GPIO.output(self.sclkPin, 0)
			if (dat & 0x80):
				GPIO.output(self.sdinPin, 1)
			else:
				GPIO.output(self.sdinPin, 0)
			GPIO.output(self.sclkPin, 1)
			dat = dat << 1
		GPIO.output(self.csPin, 1)
		GPIO.output(self.dcPin, 1)

	def setPos(self, x, y):
		self.writeByte(0xb0+y, self.oledCmd)
		self.writeByte(((x&0xf0)>>4)|0x10, self.oledCmd)
		self.writeByte((x&0x0f), self.oledCmd)

	def clearAll(self):
		for i in range(8):
			self.writeByte(0xb0+i, self.oledCmd)
			self.writeByte(0x00, self.oledCmd)
			self.writeByte(0x10, self.oledCmd)
			for j in range(128):
				self.writeByte(0, self.oledData)

	def screenInit(self):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		GPIO.setup(self.csPin, GPIO.OUT)
		GPIO.setup(self.dcPin, GPIO.OUT)
		GPIO.setup(self.sclkPin, GPIO.OUT)
		GPIO.setup(self.sdinPin, GPIO.OUT)
		GPIO.setup(self.rstPin, GPIO.OUT)
		GPIO.output(self.rstPin, 1)
		time.sleep(0.1)
		GPIO.output(self.rstPin, 0)
		time.sleep(0.2)
		GPIO.output(self.rstPin, 1)
		initCode =[0xAE,0x00,0x10,0x40,0x81,0xCF,0xA1,0xC8,0xA6,0xA8,0x3F,0XD3,0x00,0xD5,0x80,
				   0xD9,0xF1,0xDA,0x12,0xDB,0x40,0x20,0x02,0x8D,0x14,0xA4,0xA6,0xAF,0xAF]
		for every in initCode:
			self.writeByte(every, self.oledCmd)
		self.clearAll()
		self.setPos(0, 0)