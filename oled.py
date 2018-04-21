import RPi.GPIO as GPIO
import time
import matplotlib.image as mpimg

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

    def displayAsc(self, ascStr='example', pos=[0,0], fontPrefix='fonts/ASC', fontSize=16):

        with open(fontPrefix +str(fontSize), 'rb') as fi:
            fontList =fi.read()
        
        # modelList =[]
        for charNum in range(len(ascStr)):
            fontAddress =ord(ascStr[charNum])*fontSize
            for block in range(fontSize/8):
                blockModel =[]
                # generate model of a block
                for line in range(8):
                    lineModel =0
                    for part in range(fontSize/16):
                        lineModel =lineModel +ord(fontList[fontAddress +part +line*fontSize/16 +block*fontSize/2])*(2**(8*(fontSize/16-1-part)))
                    blockModel.append(lineModel)

                # display a block
                for column in range(fontSize/2):
                    colValue =0
                    self.setPos(pos[0]+fontSize/2-1-column, pos[1]+block)
                    for line in range(8):
                        colValue =colValue +(blockModel[line]%2)*(2**line)
                        blockModel[line] =blockModel[line]/2
                    self.writeByte(colValue,1)

            #reach the end of this line
            if pos[0] and not(pos[0]%(128-fontSize/2)):
                pos[0] =0
                pos[1] = pos[1] +fontSize/8
            else:
                pos[0] =pos[0] +fontSize/2

            if pos[1] >=(8-fontSize/8):
                print 'reach the end'
                break
        return 1

    def displayChn(self, chnStr=u'\u6837\u672C', pos=[0,0], fontPrefix='fonts/HZK', fontSize=16):

        #conculate quweis for chars
        quwei =[]
        for everyChar in chnStr:
            quwei.append([ord(everyChar.encode('gbk')[0])-160, ord(everyChar.encode('gbk')[1])-160])
        print quwei

        #load font file as array
        with open(fontPrefix +str(fontSize), 'rb') as fi:
            fontList =fi.read()
        modelList =[]
        for everyChar in quwei:
            fontAddress =(94*(everyChar[0]-1)+everyChar[1]-1)*(fontSize*fontSize/8)
            fontModel =[]
            # model of every line
            for line in range(fontSize):
                # model of every column part
                lineModel =0
                for everyPart in range(fontSize/8):
                    lineModel =lineModel +ord(fontList[fontAddress+line*fontSize/8+everyPart])*(2**(8*(fontSize/8-1-everyPart)))
                fontModel.append(lineModel)
            modelList.append(fontModel)

        #dispaly (8pixs as a group)
        for everyChar in modelList:
            for group in range(fontSize/8):
                for column in range(fontSize):
                    self.setPos(pos[0]+fontSize-1-column, pos[1]+group)
                    colValue =0
                    for line in range(8):
                        colValue =colValue+(everyChar[line+group*8]%2)*(2**line)
                        everyChar[line+group*8] =everyChar[line+group*8]/2
                    # print colValue
                    self.writeByte(colValue,1)
            # set positon for next char
            if pos[0] >=(128-fontSize) and pos[1] >=(8-fontSize/8):
                print 'reach the end'
                break
            if pos[0] and not(pos[0]%(128-fontSize)):
                pos[0] =0
                pos[1] =pos[1] +fontSize/8
            else:
                pos[0] =pos[0] +fontSize
        return 1

    def displayImage(self, fileName='git.png'):
        raPic = mpimg.imread(fileName)
        raPic.shape
        duPic = range(8192)
        #binarization image
        for j in range(128):
            for i in range(64):
                if (raPic[i,j,1]+raPic[i,j,2]+raPic[i,j,0] > 1.5):
                    duPic[j*64+i] = 1
                else:
                    duPic[j*64+i] = 0
        #display
        for x in range(128):
            for y in range(8):
                Dat = 1*duPic[x*64+y*8+0]+2*duPic[x*64+y*8+1]+4*duPic[x*64+y*8+2]+8*duPic[x*64+y*8+3]+16*duPic[x*64+y*8+4]+32*duPic[x*64+y*8+5]+64*duPic[x*64+y*8+6]+128*duPic[x*64+y*8+7]
                self.setPos(x,y)
                self.writeByte(Dat, 1)
    #    time.sleep(0.1)
    #    GPIO.cleanup()
        # print 'Display OK'
