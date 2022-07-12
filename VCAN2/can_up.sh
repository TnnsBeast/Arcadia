sudo modprobe can_raw
sudo modprobe mttcan
sudo modprobe vcan
sudo ip link set can0 up type can bitrate 250000
sudo ip link set up can0
sudo ip link add dev vcan1 type vcan
sudo ip link set vcan1 up