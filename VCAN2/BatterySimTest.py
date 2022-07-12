from BatterySim import BatterySim
from FlexibleBatteryCan import FlexibleBatteryCan
from threading import Thread
import time


def read_sim():
    read_battery = FlexibleBatteryCan("vcan1")
    global soc_output
    soc_output = read_battery.getSOC(1)
    global status_output
    status_output = read_battery.getChargingStatus(1)
    global tempC_output
    tempC_output = read_battery.getTempC(1)
    global soh_output
    soh_output = read_battery.getSOH(1)
    global cycle_count_output
    soh_output = read_battery.getCycleCount(1)
    global bc1_output
    bc1_output = read_battery.getLowByteCurrent1(1)
    global bc2_output
    bc1_output = read_battery.getHighByteCurrent1(1)
    global bc3_output
    bc1_output = read_battery.getLowByteCurrent2(1)
    global bc4_output
    bc1_output = read_battery.getHighByteCurrent2(1)

soc_output = None
status_output = None
tempC_output = None
soh_output = None
cycle_count_output = None
bc1_output = None
bc2_output = None
bc3_output = None
bc4_output = None



read_sim_thread = Thread(target = read_sim)
read_sim_thread.start()
battery1 = BatterySim(1, 50, 100, 1, 1, 1, 1, "Charging", 25, 40)
for i in range(1, 5):
    battery1.publish()
    time.sleep(3)
print "SOC = 50? ", soc_output == 50
print "Status = Charging? ", status_output == "Charging Current Detected"
read_sim_thread.join()
print ""

battery1.soc = 55 #change soc to 55
read_sim_thread2 = Thread(target = read_sim)
read_sim_thread2.start()
for i in range(1, 5):
    battery1.publish()
    time.sleep(3)
print "SOC = 55? ", soc_output == 55
read_sim_thread2.join()
print ""

battery1.status_string = "Discharging" #change status to discharging
read_sim_thread3 = Thread(target = read_sim)
read_sim_thread3.start()
for i in range(1, 5):
    battery1.publish()
    time.sleep(3)
print "Status = Discharging? ", status_output == "Discharge Current Detected"
read_sim_thread3.join()
print ""


battery1.soc = 50 #change soc to 50
read_sim_thread4 = Thread(target = read_sim)
read_sim_thread4.start()
for i in range(1, 5):
    battery1.publish()
    time.sleep(3)
print "SOC = 50? ", soc_output == 50
read_sim_thread4.join()
print ""

battery1.soc = 100 #change soc to 100
battery1.status_string = "Fully Charged" #change status to fully charged because soc is 100 now
read_sim_thread5 = Thread(target = read_sim)
read_sim_thread5.start()
for i in range(1, 5):
    battery1.publish()
    time.sleep(3)
print "SOC = 100? ", soc_output == 100
print "Status = Fully Charged? ", status_output == "Fully Charged"
read_sim_thread5.join()

battery1.tempC = 200
read_sim_thread6 = Thread(target = read_sim)
read_sim_thread6.start()
for i in range(1, 5):
    battery1.publish()
    time.sleep(3)
print "TempC = 200? ", tempC_output == 200
read_sim_thread6.join()




