# -*- coding: utf-8 -*-
# ZY

import socket
import threading

from zyutils.date_utils import ZYDateThread


class LongServerThread(threading.Thread):
    def __init__(self, port):
        super(LongServerThread, self).__init__()
        self.port = port

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # sock.bind((socket.gethostname(), self.port))
        sock.bind(('0.0.0.0', self.port))
        sock.listen(5)
        print('socket server started!')

        while True:
            print('waiting...')
            connection, address = sock.accept()  # 监听有无新客户

            try:
                username = "ID" + str(address[1])
                thread = ZYDateThread(connection, username)  # #如果有新的客户就新建一个线程。处理这个客户的请求，同时往clinets列表添加一个用户
                thread.start()  # 运行新启的client线程里的run()方法
                # clients[username] = connection
                print(username)
            except socket.timeout:
                print('websocket connection timeout!')
