from FlexibleBatteryCan import FlexibleBatteryCan

test = FlexibleBatteryCan('can0')

for i in range(1,test.getBatteryCount() + 1):
    #get state of charge (% charged)
    print "Battery ", i, " Percent Level: ", test.getSOC(i)
    #get battery temperature in Celcius
    print "Battery ", i, " Temperature in C: ", test.getTempC(i)
    #get battery temperature in Farenheit
    print "Battery ", i, " Temperature in F: ", test.getTempF(i)
    #get battery state of health
    print "Battery ", i, " State of Health: ", test.getSOH(i)
    #get battery charging status
    print "Battery ", i, " Charging Status: ", test.getChargingStatus(i)
    #get battery cycle count
    print "Battery ", i, " Cycle Count: ", test.getCycleCount(i)
    #get battery low byte current 1
    print "Battery ", i, " Low Byte Current 1: ", test.getLowByteCurrent1(i)
    #get battery low byte current 2
    print "Battery ", i, " Low Byte Current 2: ", test.getLowByteCurrent2(i)
    #get battery high byte current 1
    print "Battery ", i, " High Byte Current 1: ", test.getHighByteCurrent1(i)
    #get battery high byte current 2
    print "Battery ", i, " High Byte Current 2: ", test.getHighByteCurrent2(i)
    #get timestamp of when battery data was last updated
    print "Battery ", i, " Timestamp: ", test.getTimeStamp(i)
    print "------------------------------------"

#update all data 
test.updateALL()

#get all values again to demonstrate update function works
for i in range(1,test.getBatteryCount() + 1):
    print "Battery ", i, " Percent Level: ", test.getSOC(i)
    print "Battery ", i, " Temperature in C: ", test.getTempC(i)
    print "Battery ", i, " Temperature in F: ", test.getTempF(i)
    print "Battery ", i, " State of Health: ", test.getSOH(i)
    print "Battery ", i, " Charging Status: ", test.getChargingStatus(i)
    print "Battery ", i, " Cycle Count: ", test.getCycleCount(i)
    print "Battery ", i, " Low Byte Current 1: ", test.getLowByteCurrent1(i)
    print "Battery ", i, " Low Byte Current 2: ", test.getLowByteCurrent2(i)
    print "Battery ", i, " High Byte Current 1: ", test.getHighByteCurrent1(i)
    print "Battery ", i, " High Byte Current 2: ", test.getHighByteCurrent2(i)
    print "Battery ", i, " Timestamp: ", test.getTimeStamp(i)
    print "------------------------------------"
