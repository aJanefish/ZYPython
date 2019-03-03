# -*- coding: utf-8 -*-
# ZY
import socket


class ZYSendUtils:
    def __init__(self):
        pass

    @staticmethod
    def send():
        s = socket.socket()         # 创建 socket 对象
        # host = socket.gethostname()  # 获取本地主机名
        host = '127.0.0.1'
        port = 8989                # 设置端口号
        print(host, port)
        s.connect((host, port))
        # s.send(bytes("{key=3}3".encode('utf-8')))
        s.send("{key = 3}")
        print(s.recv(1024))
        s.close()
