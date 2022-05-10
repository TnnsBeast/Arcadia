import rospy
from beginner_tutorials.msg import SmartBatteryStatus
from FlexibleBatteryCan import FlexibleBatteryCan

def talker():
    pub = rospy.Publisher('battery', SmartBatteryStatus, queue_size=10)
    rospy.init_node('battery_publisher', anonymous=True)
    r = rospy.Rate(10) #10hz
    msg = SmartBatteryStatus()

    while not rospy.is_shutdown():
        monitor = FlexibleBatteryCan('can0')
        for i in range(1, monitor.getBatteryCount() + 1):
        	#initialize message for current battery
        	msg = SmartBatteryStatus()

        	#set all values of message for current battery
	        msg.percentage = monitor.getSOC(i)
	        msg.temperature_celcius = monitor.getTempC(i)
	        msg.temperature_farenheit = monitor.getTempF(i)
	        msg.state_of_health = monitor.getSOH(i)
	        msg.cycle_count = monitor.getCycleCount(i)
	        msg.low_byte_current_1 = monitor.getLowByteCurrent1(i)
	        msg.low_byte_current_2 = monitor.getLowByteCurrent2(i)
	        msg.high_byte_current_1 = monitor.getHighByteCurrent1(i)
	        msg.high_byte_current_2 = monitor.getHighByteCurrent2(i)
	        msg.charging_status = monitor.getChargingStatus(i)
	        msg.battery_number = i

	        #publish message for current battery
	        rospy.loginfo(msg)
	        pub.publish(msg)
	        r.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
