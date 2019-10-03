#!/usr/bin/env python

#import rospy
import socket
#import sys
#from std_msgs.msg import Float64

#rospy.init_node('tx2_communication_server', anonymous=True)
#pub = rospy.Publisher('camera_obstacle', Float64, queue_size=15)


class Server():
    def __init__(self, ip_addr, port_num):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (ip_addr, port_num)
        self.sock.bind(server_address)
        self.sock.listen(1)

    def run(self):
        print('waiting for a connection')
        self.connection, client_address = self.sock.accept()
        print('connected')
        while True:
            data = self.connection.recv(1024)
            if data:
                msg = data.decode("utf-8")
                print(msg)
                split_msg = msg.replace('--',':')

                split_msg = split_msg.split(":")
                class_ID = split_msg[2]
                print(class_ID)
                accuracy = split_msg[4]
                print(accuracy)
                left = split_msg[6]
                print(left)
                top = split_msg[8]
                print(top)
                right = split_msg[10]
                print(right)
                bottom = split_msg[12]
                width = split_msg[14]
                height = split_msg[16]
                center = split_msg[18]
               # pub.publish(int(class_ID))
                # with open("/home/agv/catkin_ws/src/obstacles_log/socket.csv", "a") as log:
                #     log.write(msg)

    def stop(self):
        self.connection.close()
        self.shutdown.set()


if __name__ == '__main__':


    ip_addr = 'localhost'
    port_num = 8888
    my_server = Server(ip_addr, port_num)
    my_server.run()
