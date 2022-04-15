# Arcadia

First of all, for any CAN communication to work with the TX2, the following command line commands must be executed:

sudo modprobe can_raw
sudo modprobe mttcan
sudo ip link set can0 type can bitrate 250000
sudo ip link set up can0

Currently for our purposes, we only need to use one can port, so we can just setup can0. The TX2 has two CAN ports, so to intialize the second one (which once again is unecessary for us) execute the following as well:
sudo ip link set can1 type can bitrate 250000
sudo ip link set up can1


Every 3 seconds a "heartbeat" of 5 messages is sent out by each battery. Here is an example:

-------------------------------------------                 
  can0  5FF   [8]  20 81 21 01 00 00 00 38
  
  can0  5FF   [8]  30 01 38 64 DC 05 E8 03
  
  can0  5FF   [8]  31 01 4D CF 01 00 00 00
  
  can0  5FF   [8]  32 01 5F 0B 73 0B 72 0B
  
  can0  5FF   [8]  33 01 00 00 00 00 00 00
-------------------------------------------
  
For each message, the first value is D0, then D1, and so on until D7. 

D0, or data0 contains the message identifier, 20, and 30-33. In the code file, these data values are converted to 32, 48-51.

Message 20/32 is referred to as soc_msg.
Message 30/48 is reffered to as soh_msg.
Message 31/49 is reffered to as cyclecount_msg.
Message 32/50 is reffered to as temp_msg.
Message 33/51 is reffered to as bytecurrent_msg.

List of the data contained in each message:
Note: For values that are just numbers, they are always that number and are used for internal battery communication
      We only use Temp 1

20: 81, 21, Battery Number, Alarm1, Alarm2, Status, SOC

30: Battery Number, SOC, SOH, Max Discharge Current (D4 and D5), Max Regen Current (D6 and D7)

31: Battery Number, Pack Voltage (D2 and D3), Cycle Count (D4 and D5), Not Used, Not Used

32: Battery Number, Temp 1 (D2 and D3), Temp 2 (D4 and D5), Temp 3 (D6 and D7)

33: Battery Number, Low byte current 1, Low byte current 2, High byte current 1, High byte current 2, Not Used, Not Used




Some Examples:
Deconstruction of 30
    SOC (state of charge): D2
      D2: 38
      Hex value: 38
      Decimal value: 56
        Note: On Page 8, says the following
          Range: 0-100, %of remaining capacity
        So: 56%

  Max Discharge Current: D4 and D5
    D4: DC      D5: 05
    Hex value: 05DC
    Decimal value: 1500
      Note: On Page 5, says to do the following:
        1500/10 = 150A

  Max Regen Current
    D6: E8      D6: 03
    Hex value: 03E8
    Decimal value: 1000
      Note: On Page 5, says to do the following:
        1000/10 = 100A

Deconstruction of 32
  Temp 1: D2 and D3
    D2: 5F     D3: 0B
    Hex value: 0B5F
    Decimal value: 2911
      Note: On Page 8, says to do the following:
        Range: -40C to 120C
        (Value-2731)/10 = tempC
      So: 
        (2911-2731)/10 = 18 Degrees C = 64.4 Degrees F


Info of the battery we used (From manual - https://ceb8596f236225acd007-8e95328c173a04ed694af83ee4e24c15.ssl.cf5.rackcdn.com/docs/product/InsightBatteryManual_040121_210401_115955.pdf)

Model: 48V030-GC2
Nominal Voltage: 51.2V
30 Ah
1.536kWh
128Wh/kg
Continuous Discharge Current: 100A

