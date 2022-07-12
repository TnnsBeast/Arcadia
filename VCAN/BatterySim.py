import can
import time

class BatterySim:
    def __init__(self, num_batteries, soc, soh, bc1, bc2, bc3, bc4, status_string, tempC, cycle_count, interval, repeat_times):

        bus = can.interface.Bus('vcan1', bustype='socketcan')
        status = 0
        if status_string == "Charging":
            status = 2
            charge_interval = interval
        if status_string == "Discharging":
            status = 4
            discharge_interval = interval
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
        for i in range(1, repeat_times + 1):
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