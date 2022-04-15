from FlexibleBatteryCan import FlexibleBatteryCan

test = FlexibleBatteryCan('can0')

for i in range(1,test.getBatteryCount() + 1):
    print "Battery ", i, " Percent Level: ", test.getSOC(i)
    #print "Battery ", i, " Temperature in C: ", test.getTempC(i)
    #print "Battery ", i, " Temperature in F: ", test.getTempF(i)
    print "Battery ", i, " State of Health: ", test.getSOH(i)
    print "Battery ", i, " Charging Status: ", test.getChargingStatus(i)
    #print "Battery ", i, " Cycle Count: ", test.getCycleCount(i)
    #print "Battery ", i, " Low Byte Current 1: ", test.getLowByteCurrent1(i)
    #print "Battery ", i, " Low Byte Current 2: ", test.getLowByteCurrent2(i)
    #print "Battery ", i, " High Byte Current 1: ", test.getHighByteCurrent1(i)
    #print "Battery ", i, " High Byte Current 2: ", test.getHighByteCurrent2(i)
    #print "Battery ", i, " Timestamp: ", test.getTimeStamp(i)
    print "------------------------------------"

#test.updateALL()

# for i in range(1,test.getBatteryCount() + 1):
#     print "Battery ", i, " Percent Level: ", test.getSOC(i)
#     print "Battery ", i, " Temperature in C: ", test.getTempC(i)
#     print "Battery ", i, " Temperature in F: ", test.getTempF(i)
#     print "Battery ", i, " State of Health: ", test.getSOH(i)
#     print "Battery ", i, " Charging Status: ", test.getChargingStatus(i)
#     print "Battery ", i, " Cycle Count: ", test.getCycleCount(i)
#     print "Battery ", i, " Low Byte Current 1: ", test.getLowByteCurrent1(i)
#     print "Battery ", i, " Low Byte Current 2: ", test.getLowByteCurrent2(i)
#     print "Battery ", i, " High Byte Current 1: ", test.getHighByteCurrent1(i)
#     print "Battery ", i, " High Byte Current 2: ", test.getHighByteCurrent2(i)
#     print "Battery ", i, " Timestamp: ", test.getTimeStamp(i)
#     print "------------------------------------"
