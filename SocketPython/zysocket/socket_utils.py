# -*- coding: utf-8 -*-
# ZY
import threading

import socket


class ZYSocketDateThread(threading.Thread):
    def __init__(self, connection, name):
        super(ZYSocketDateThread, self).__init__()
        self.connection = connection
        self.name = name

    def run(self):
        data = self.connection.recv(1024)
        self.parse_headers(data)


        self.connection.send("200")
        self.connection.close()
        pass

    def parse_headers(self, data):
        print(type(data), data)
        print str(data)





class ZYSocketThread(threading.Thread):
    def __init__(self, port):
        super(ZYSocketThread, self).__init__()
        self.port = port

    def run(self):
        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # sock.bind((socket.gethostname(), self.port))
        sock = socket.socket()
        sock.bind(('127.0.0.1', self.port))
        sock.listen(5)
        print('ZYSocketThread server started!')

        while True:
            print('waiting...')
            connection, address = sock.accept()  # 监听有无新客户

            try:
                username = "ID" + str(address[1]) + ":" + str(address[0])
                print(username)
                thread = ZYSocketDateThread(connection, username)  # #如果有新的客户就新建一个线程。处理这个客户的请求，同时往clinets列表添加一个用户
                thread.start()  # 运行新启的client线程里的run()方法
                # clients[username] = connection

            except socket.timeout:
                print('websocket connection timeout!')
