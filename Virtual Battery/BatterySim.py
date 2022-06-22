import can
import time

bus = can.interface.Bus('vcan1', bustype='socketcan')

# These variables should be edited to change battery values.
# All values have a min of 0
num_batteries = 3
soc = 7 # %, so should be max 100
soh = 100 # %, so should be max 100
bc1 = 1 # bc = byte current. All bc max: 255 (FF)
bc2 = 1
bc3 = 1
bc4 = 1
status_string = "Discharging" # Status can be "Charging", "Discharging", "No Reading", or "Fully Charged"
tempC = 25 # Max : 6280 (FB FF - a fractional value would become FF FF, 6281 is too large)
cycle_count = 1000 # Max: 65535 (FF FF)
discharge_interval = 3 # Number of seconds it takes for the battery to lose 1% - must be 3 or more
charge_interval = 3 # Number of seconds it takes for the battery to charge 1% - must be 3 or more
# End of variables that should be edited

status = 0
if status_string == "Charging":
    status = 2
if status_string == "Discharging":
    status = 4
if status_string == "No Reading":
    status = 0
if status_string == "Fully Charged":
    status = 64

battery_temp_val = tempC * 10 + 2731
temp_byte1 = int(hex(battery_temp_val)[-2:], 16)
if len(hex(battery_temp_val)) == 5:
    temp_byte2 = int(hex(battery_temp_val)[-3], 16)
else:
    temp_byte2 = int(hex(battery_temp_val)[-4:-2], 16)

cycle_count_byte2 = 0
if len(hex(cycle_count)) < 5:
    cycle_count_byte1 = cycle_count
if len(hex(cycle_count)) == 5:
    cycle_count_byte1 = int(hex(cycle_count)[-2:], 16)
    cycle_count_byte2 = int(hex(cycle_count)[-3], 16)
if len(hex(cycle_count)) == 6:
    cycle_count_byte1 = int(hex(cycle_count)[-2:], 16)
    cycle_count_byte2 = int(hex(cycle_count)[-4:-2], 16)


start_time = time.time()
while True:
    current_time = time.time()
    if (status_string == "Charging"):
        if (soc == 100):
            print "DONE CHARGING"
            status_string = "Fully Charged"
            status = 64
        if (current_time - start_time) > charge_interval and soc < 100:
            soc = soc + 1
            start_time = current_time
            print soc
    if (status_string == "Discharging"):
        if (soc == 0):
            print "FULLY DISCHARGED"
        if (current_time - start_time) > discharge_interval and soc > 0:
            soc = soc - 1
            start_time = current_time
            print soc
    for i in range(1,num_batteries + 1):
        msg1 = can.Message(arbitration_id=0x5FF, data=[32,0,0,i,0,0,status,soc])
        bus.send(msg1)
        msg2 = can.Message(arbitration_id=0x5FF, data=[48,i,soc,soh,0,0,0,0])
        bus.send(msg2)
        msg3 = can.Message(arbitration_id=0x5FF, data=[49,i,0,0,cycle_count_byte1,cycle_count_byte2,0,0])
        bus.send(msg3)
        msg4 = can.Message(arbitration_id=0x5FF, data=[50,i,temp_byte1,temp_byte2,0,0,0,0])
        bus.send(msg4)
        msg5 = can.Message(arbitration_id=0x5FF, data=[51,i,bc1,bc2,bc3,bc4,0,0])
        bus.send(msg5)
    time.sleep(3) # Send heartbeat every 3 seconds to mimic actual batteries
    
""" 
Example Heartbeat
can0 5FF [8] 20 81 21 01 00 00 00 38

can0 5FF [8] 30 01 38 64 DC 05 E8 03

can0 5FF [8] 31 01 4D CF 01 00 00 00

can0 5FF [8] 32 01 5F 0B 73 0B 72 0B

can0 5FF [8] 33 01 00 00 00 00 00 00 
"""