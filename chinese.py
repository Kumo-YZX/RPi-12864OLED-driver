from oled import Oled
import time
class chineseStr(object):

    def __init__(self, chineseStr =u'\u4e00\u5317\u4eac'):
        self.quwei =[]
        for everyChar in chineseStr:
            self.quwei.append([ord(everyChar.encode('gbk')[0])-160, ord(everyChar.encode('gbk')[1])-160])
        print self.quwei

    def getModel(self, fontFile='fonts\\HZK16', fontSize=16):
        with open(fontFile, 'rb') as fi:
            fontList =fi.read()
        self.modelList =[]
        for everyChar in self.quwei:
            fontAddress =(94*(everyChar[0]-1)+everyChar[1]-1)*(fontSize*2)
            fontModel =[]
            for i in range(0,32,2):
                fontModel.append(ord(fontList[fontAddress+i])*256+ord(fontList[fontAddress+i+1]))
            self.modelList.append(fontModel)
        return self.modelList
    
    def display(self, pos=[0,0]):
        csPin = 11
        dcPin = 12
        sdinPin = 13
        sclkPin = 15
        rstPin = 16
        myScreen = Oled(csPin, dcPin, sdinPin, sclkPin, rstPin)
        for everyChar in self.modelList:
            for group in range(16/8):
                for column in range(16):
                    myScreen.setPos(pos[0]+15-column, pos[1]+group)
                    colValue =0
                    for line in range(8):
                        colValue =colValue+(everyChar[line+group*8]%2)*(2**line)
                        everyChar[line+group*8] =everyChar[line+group*8]/2
                    print colValue
                    myScreen.writeByte(colValue,1)
            # set positon for next char
            pos[0] =pos[0] +16
        return 1

if __name__ =="__main__":
    myobj =chineseStr()
    for everyChar in myobj.getModel():
        for i in range(0, 16):
            print '{0:32}'.format(everyChar[i])





