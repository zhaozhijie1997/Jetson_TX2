# run this on the ros side

import socket


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
                print(int(class_ID))
                accuracy = split_msg[4]
                print(float(accuracy))
                left = split_msg[6]
                print(float(left))
                top = split_msg[8]
                print(float(top))
                right = split_msg[10]
                print(float(right))
                bottom = split_msg[12]
                print(float(bottom))
                width = split_msg[14]
                print(float(width))
                height = split_msg[16]
                print(float(height))
                center = split_msg[20]
                msg = center.replace('(','')
                msg = msg.replace(')','')
                msg = msg.replace('(','')
                msg = msg.replace(' ','')
                msg = msg.split(',')
                a = [float(msg[0]),float(msg[1])]
                print(a)

                #center_(split_msg)coord = center.
                #print


    def stop(self):
        self.connection.close()
        self.shutdown.set()


if __name__ == '__main__':
    # ip_addr = 'localhost'


    ip_addr = '192.168.1.212'
    port_num = 8888
    my_server = Server(ip_addr, port_num)
    my_server.run()
