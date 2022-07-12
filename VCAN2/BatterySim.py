import can
import time

class BatterySim:
    def __init__(self, num_batteries, soc, soh, bc1, bc2, bc3, bc4, status_string, tempC, cycle_count):

        self.bus = can.interface.Bus('vcan1', bustype='socketcan')
        self.num_batteries = num_batteries
        self.soc = soc
        self.soh = soh
        self.bc1 = bc1
        self.bc2 = bc2
        self.bc3 = bc3
        self.bc4 = bc4
        self.status_string = status_string
        self.tempC = tempC
        self.cycle_count = cycle_count

    def publish(self):
        self.status = 0
        if self.status_string == "Charging":
            self.status = 2
        if self.status_string == "Discharging":
            self.status = 4
        if self.status_string == "No Reading":
            self.status = 0
        if self.status_string == "Fully Charged":
            self.status = 64

        self.battery_temp_val = self.tempC * 10 + 2731
        self.temp_byte1 = int(hex(self.battery_temp_val)[-2:], 16)
        if len(hex(self.battery_temp_val)) == 5:
            self.temp_byte2 = int(hex(self.battery_temp_val)[-3], 16)
        else:
            self.temp_byte2 = int(hex(self.battery_temp_val)[-4:-2], 16)

        self.cycle_count_byte2 = 0
        if len(hex(self.cycle_count)) < 5:
            self.cycle_count_byte1 = self.cycle_count
        if len(hex(self.cycle_count)) == 5:
            self.cycle_count_byte1 = int(hex(self.cycle_count)[-2:], 16)
            self.cycle_count_byte2 = int(hex(self.cycle_count)[-3], 16)
        if len(hex(self.cycle_count)) == 6:
            self.cycle_count_byte1 = int(hex(self.cycle_count)[-2:], 16)
            self.cycle_count_byte2 = int(hex(self.cycle_count)[-4:-2], 16)
        
        for i in range(1, self.num_batteries + 1):
            self.msg1 = can.Message(arbitration_id=0x5FF, data=[32,0,0,i,0,0,self.status,self.soc])
            self.bus.send(self.msg1)
            self.msg2 = can.Message(arbitration_id=0x5FF, data=[48,i,self.soc,self.soh,0,0,0,0])
            self.bus.send(self.msg2)
            self.msg3 = can.Message(arbitration_id=0x5FF, data=[49,i,0,0,self.cycle_count_byte1,self.cycle_count_byte2,0,0])
            self.bus.send(self.msg3)
            self.msg4 = can.Message(arbitration_id=0x5FF, data=[50,i,self.temp_byte1,self.temp_byte2,0,0,0,0])
            self.bus.send(self.msg4)
            self.msg5 = can.Message(arbitration_id=0x5FF, data=[51,i,self.bc1,self.bc2,self.bc3,self.bc4,0,0])
            self.bus.send(self.msg5)