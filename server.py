#!/usr/bin/env python

import rospy
import socket
import sys
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import MultiArrayDimension

rospy.init_node('tx2_communication_server', anonymous=True)
pub = rospy.Publisher('detection_results', Float64MultiArray, queue_size=1)



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
            #i = 0
            if data:
                msg = data.decode("utf-8")
                print(msg)

                split_msg = msg.replace('--',':')
                split_msg = split_msg.split(":")
                class_ID = split_msg[2]

                print(int(class_ID))
                accuracy = split_msg[4]
                left = split_msg[6]
                top = split_msg[8]
                right = split_msg[10]
                bottom = split_msg[12]
                width = split_msg[14]
                height = split_msg[16]
                center = split_msg[20]
                msg = center.replace('(','')
                msg = msg.replace(')','')
                msg = msg.replace(' ','')
                msg = msg.split(',')
 
                each = Float64MultiArray() 

                each.data = (float(class_ID),float(accuracy),float(width),float(height),float(msg[0]),float(msg[1]))

                pub.publish(each)


    def stop(self):
        self.connection.close()
        self.shutdown.set()


if __name__ == '__main__':
    # ip_addr = 'localhost'


    ip_addr = '192.168.1.212'
    port_num = 8889
    my_server = Server(ip_addr, port_num)
    my_server.run()
