# Jetson_TX2
To run Objection Detection model:
1. git clone https://github.com/zhaozhijie1997/jetson-inference.git
2. Follow the instruction and build
3. Download SSD-Inception-v2 model 
4. Put under /bin/networks
5. Extract here
6. Add in the final.py file to the /build/aarch64/bin
7. Run it


This repo also contains a server.py file for the results receiver laptop.
1. Run ifconfig to find out the local ip address starting with 10.169......
2. Run netstat -tulpn | grep LISTEN to check for open ports
3. Then change the corresponding ip address and port no at both client and server side




This repo also contains a video recorder API to record raw video footage
Change corresponding save file address and name as you wish
