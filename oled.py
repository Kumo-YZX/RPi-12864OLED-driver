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
		self.writeByte((x&0x0f)|0x01, self.oledCmd)

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
		self.writeByte(0xAE, self.oledCmd)
		self.writeByte(0x00, self.oledCmd)
		self.writeByte(0x10, self.oledCmd)
		self.writeByte(0x40, self.oledCmd)
		self.writeByte(0x81, self.oledCmd)
		self.writeByte(0xCF, self.oledCmd)
		self.writeByte(0xA1, self.oledCmd)
		self.writeByte(0xC8, self.oledCmd)
		self.writeByte(0xA6, self.oledCmd)
		self.writeByte(0xA8, self.oledCmd)
		self.writeByte(0x3f, self.oledCmd)
		self.writeByte(0xD3, self.oledCmd)
		self.writeByte(0x00, self.oledCmd)
		self.writeByte(0xd5, self.oledCmd)
		self.writeByte(0x80, self.oledCmd)
		self.writeByte(0xD9, self.oledCmd)
		self.writeByte(0xF1, self.oledCmd)
		self.writeByte(0xDA, self.oledCmd)
		self.writeByte(0x12, self.oledCmd)
		self.writeByte(0xDB, self.oledCmd)
		self.writeByte(0x40, self.oledCmd)
		self.writeByte(0x20, self.oledCmd)
		self.writeByte(0x02, self.oledCmd)
		self.writeByte(0x8D, self.oledCmd)
		self.writeByte(0x14, self.oledCmd)
		self.writeByte(0xA4, self.oledCmd)
		self.writeByte(0xA6, self.oledCmd)
		self.writeByte(0xAF, self.oledCmd)

		self.writeByte(0xAF, self.oledCmd)
		self.clearAll()
		self.setPos(0, 0)