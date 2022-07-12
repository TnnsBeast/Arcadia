from BatterySim import BatterySim
from FlexibleBatteryCan import FlexibleBatteryCan
from threading import Thread
import time

def sim_battery():
    print "Battery Started"
    virtualBattery = BatterySim(1, 50, 100, 1, 1, 1, 1, "Charging", 25, 5, 5, 4)
    print "Battery Done"

def read_sim():
    print "Read Started"
    test = FlexibleBatteryCan('vcan1')
    print test.getSOC(1), test.getTempC(1), test.getTempF(1), test.getSOH(1), test.getChargingStatus(1), test.getCycleCount(1), test.getLowByteCurrent1(1), test.getLowByteCurrent2(1), test.getHighByteCurrent1(1), test.getHighByteCurrent2(1), test.getTimeStamp(1)
    print "------------------------------------"
    print "Read Done"

    #should be 51% charge becuase starts at 50 and is set to charging.
    print(test.getSOC(1) == 51)

sim_battery_thread = Thread(target = sim_battery)
read_sim_thread = Thread(target = read_sim)
read_sim_thread.start()
sim_battery_thread.start()






