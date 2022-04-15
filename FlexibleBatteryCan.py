import can
import time

class FlexibleBatteryCan:
    def __init__(self, can_port):
        self.bus = can.interface.Bus(bustype='socketcan', channel=can_port, bitrate=250000)
        self.allMessages = []
        self.allData = []
        self.messageHolder = []
        t_end = time.time() + 5
        while time.time() < t_end:
            self.messageHolder.append(self.bus.recv())

        self.batteryCount = 0
        for msg in self.messageHolder:
            if msg.data[0] == 32:
                if msg.data[3] > self.batteryCount:
                    self.batteryCount = msg.data[3]
            else:
                if msg.data[1] > self.batteryCount:
                    self.batteryCount = msg.data[1]
        
        for i in range(self.batteryCount):
            self.allMessages.append(['*','*','*','*','*'])
            self.allData.append(['*','*','*','*','*','*','*','*','*','*', '*'])
        

        self.updateALL()

    
    def updateALL(self):
        self.updateAllMessages()
        self.convertMessagesToData()
        
    def getBatteryCount(self):
        return self.batteryCount
    def getAllMessages(self):
        return self.allMessages
    def getAllData(self):
        return self.allData

    def checkIfAllMessagesPresent(self):
        for currentBatteryMessages in self.allMessages:
            for i in currentBatteryMessages:
                if i == '*':
                    return False
        return True


    def convertSOCData(self, batteryNumber):
        soc_msg = self.allMessages[batteryNumber][0]
        return soc_msg.data[7]


    
    def convertStatusData(self, batteryNumber):
        soc_msg = self.allMessages[batteryNumber][0]
        status = soc_msg.data[6]

        chargedata = bin(int(str(status), base=16))
        if (chargedata == '0b100'):
            return "Discharge Current Detected"
        elif (chargedata == '0b10'):
            return "Charging Current Detected"
        elif (chargedata == '0b0'):
            return "Not charging, discharging, fully charged or over-temperature condition"
        elif (chargedata == '0b1000000'):
            return "Fully Charged"


    def convertSOHData(self, batteryNumber):
        soh_msg = self.allMessages[batteryNumber][1]
        return soh_msg.data[3]



    def convertCycleCountData(self, batteryNumber):
        cyclecount_msg = self.allMessages[batteryNumber][2]
        if cyclecount_msg.data[4] < 15:
            cyclecountbyte1 = '0' + str(hex(cyclecount_msg.data[4]))[2]
        else:
            cyclecountbyte1 = str(hex(cyclecount_msg.data[4]))[2:]
        if cyclecount_msg.data[5] < 15:
            cyclecountbyte2 = '0' + str(hex(cyclecount_msg.data[5]))[2]
        else:
            cyclecountbyte2 = str(hex(cyclecount_msg.data[5]))[2:]
        return (int('0x' + cyclecountbyte2 + cyclecountbyte1, 16))


    def convertTempCData(self, batteryNumber):
        temp_msg = self.allMessages[batteryNumber][3]
        if temp_msg.data[2] < 15:
            tempbyte1 = '0' + str(hex(temp_msg.data[2]))[2]
        else:
            tempbyte1 = str(hex(temp_msg.data[2]))[2:]
        if temp_msg.data[3] < 15:
            tempbyte2 = '0' + str(hex(temp_msg.data[3]))[2]
        else:
            tempbyte2 = str(hex(temp_msg.data[3]))[2:]
        return (int('0x' + tempbyte2 + tempbyte1, 16) - 2731)/10



    def convertTempFData(self, batteryNumber):
        temp_msg = self.allMessages[batteryNumber][3]
        if temp_msg.data[2] < 15:
            tempbyte1 = '0' + str(hex(temp_msg.data[2]))[2]
        else:
            tempbyte1 = str(hex(temp_msg.data[2]))[2:]
        if temp_msg.data[3] < 15:
            tempbyte2 = '0' + str(hex(temp_msg.data[3]))[2]
        else:
            tempbyte2 = str(hex(temp_msg.data[3]))[2:]

        return (((int('0x' + tempbyte2 + tempbyte1, 16) - 2731)/10) * 1.8) + 32



    def convertByteCurrentData1(self, batteryNumber):
        bytecurrent_msg = self.allMessages[batteryNumber][4]
        return bytecurrent_msg.data[2]
    def convertByteCurrentData2(self, batteryNumber):
        bytecurrent_msg = self.allMessages[batteryNumber][4]
        return bytecurrent_msg.data[3]
    def convertByteCurrentData3(self, batteryNumber):
        bytecurrent_msg = self.allMessages[batteryNumber][4]
        return bytecurrent_msg.data[4]
    def convertByteCurrentData4(self, batteryNumber):
        bytecurrent_msg = self.allMessages[batteryNumber][4]
        return bytecurrent_msg.data[5]



    def updateAllMessages(self):
        for i in range(self.batteryCount):
            self.allMessages[i] = ['*','*','*','*','*']
        while self.checkIfAllMessagesPresent() == False:
            msg = self.bus.recv()
            if msg.data[0] == 32:
                batteryNumber = msg.data[3]
                self.allMessages[batteryNumber - 1][0] = msg
                #print "Assigned Battery " + str(batteryNumber) + " MSG 20"
            if msg.data[0] == 48:
                batteryNumber = msg.data[1]
                self.allMessages[batteryNumber - 1][1] = msg
                #print "Assigned Battery " + str(batteryNumber) + " MSG 30"
            if msg.data[0] == 49:
                batteryNumber = msg.data[1]
                self.allMessages[batteryNumber - 1][2] = msg
                #print "Assigned Battery " + str(batteryNumber) + " MSG 31"
            if msg.data[0] == 50:
                batteryNumber = msg.data[1]
                self.allMessages[batteryNumber - 1][3] = msg
                #print "Assigned Battery " + str(batteryNumber) + " MSG 32"
            if msg.data[0] == 51:
                batteryNumber = msg.data[1]
                self.allMessages[batteryNumber - 1][4] = msg
                #print "Assigned Battery " + str(batteryNumber) + " MSG 33"

    def convertMessagesToData(self):
        for batteryNumber in range(self.batteryCount):
            self.allData[batteryNumber][0] = self.allMessages[batteryNumber][0].timestamp
            self.allData[batteryNumber][1] = self.convertTempCData(batteryNumber)
            self.allData[batteryNumber][2] = self.convertTempFData(batteryNumber)
            self.allData[batteryNumber][3] = self.convertSOCData(batteryNumber)
            self.allData[batteryNumber][4] = self.convertStatusData(batteryNumber)
            self.allData[batteryNumber][5] = self.convertSOHData(batteryNumber)
            self.allData[batteryNumber][6] = self.convertCycleCountData(batteryNumber)
            self.allData[batteryNumber][7] = self.convertByteCurrentData1(batteryNumber)
            self.allData[batteryNumber][8] = self.convertByteCurrentData2(batteryNumber)
            self.allData[batteryNumber][9] = self.convertByteCurrentData3(batteryNumber)
            self.allData[batteryNumber][10] = self.convertByteCurrentData4(batteryNumber)
        
    
    def getTimeStamp(self, batteryNumber):
        return self.allData[batteryNumber - 1][0]
    def getTempC(self, batteryNumber):
        return self.allData[batteryNumber - 1][1]
    def getTempF(self, batteryNumber):
        return self.allData[batteryNumber - 1][2]
    def getSOC(self, batteryNumber):
        return self.allData[batteryNumber - 1][3]
    def getChargingStatus(self, batteryNumber):
        return self.allData[batteryNumber - 1][4]
    def getSOH(self, batteryNumber):
        return self.allData[batteryNumber - 1][5]
    def getCycleCount(self, batteryNumber):
        return self.allData[batteryNumber - 1][6]
    def getLowByteCurrent1(self, batteryNumber):
        return self.allData[batteryNumber - 1][7]
    def getLowByteCurrent2(self, batteryNumber):
        return self.allData[batteryNumber - 1][8]
    def getHighByteCurrent1(self, batteryNumber):
        return self.allData[batteryNumber - 1][9]
    def getHighByteCurrent2(self, batteryNumber):
        return self.allData[batteryNumber - 1][10]