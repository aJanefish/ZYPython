# -*- coding: utf-8 -*-
# ZY
import base64
import hashlib
import json
import socket
import threading


class ZYDateThread(threading.Thread):
    def __init__(self, connection, username):
        print('new SGDateThread client joined! - ', username)
        super(ZYDateThread, self).__init__()
        self.connection = connection
        self.username = username
        self.errorTimes = 0

    def run(self):
        data = self.connection.recv(1024)  # 第一次连接，相当于握手??
        headers = self.parse_headers(data)
        token = self.generate_token(headers['Sec-WebSocket-Key'])
        # token = self.generate_token("Ba0THROjs68hOrs62JOMuw==")
        self.connection.send('\
HTTP/1.1 101 WebSocket Protocol Hybi-10\r\n\
Upgrade: WebSocket\r\n\
Connection: Upgrade\r\n\
Sec-WebSocket-Accept: %s\r\n\r\n' % token)
        while True:

            try:
                print('receive........')
                data = self.connection.recv(1024)
                if len(data) == 0:
                    self.errorTimes += 1
                    if self.errorTimes >= 10:
                        self.connection.close()

                        print("ws_debug socket id=", self.username, " closed")
                        break
                    continue

                self.errorTimes = 0
                if len(data) >= 150 or len(data) <= 50:
                    print("len(data):", len(data))
                    continue

                data = self.parse_data(data)  # 数据处理

                print("data1:", data)
                data = data[:data.find("}") + 1]  # 发现l树莓派下有时有乱码
                print("data2:", data)

                dicts = json.loads(data)
                print(dicts)

            except Exception as ex:
                # self.notify(message)
                #
                print("unexpected error ws_debug: ", str(ex))
                # self.connection.close()
                # clients.pop(self.username)
                # break

    def parse_data(self, msg):
        # print("msg:", msg)
        print("len(msg):", len(msg))
        try:
            v = ord(msg[1]) & 0x7f
            if v == 0x7e:
                p = 4
            elif v == 0x7f:
                p = 10
            else:
                p = 2
            mask = msg[p:p + 4]
            data = msg[p + 4:]
            # mList = [chr(ord(v) ^ ord(mask[k % 4])) for k, v in enumerate(data)]
            # print(mList)
            # print(type(mList))
            return ''.join([chr(ord(v) ^ ord(mask[k % 4])) for k, v in enumerate(data)])
        except:
            print("parse data error,   return the default string！")
            return '{"name":"zy","age":19}'

    def parse_headers(self, msg):
        headers = {}
        print(r"msg = ", msg)
        header, data = msg.split('\r\n\r\n', 1)
        for line in header.split('\r\n')[1:]:
            key, value = line.split(': ', 1)
            headers[key] = value
        headers['data'] = data
        return headers

    def generate_token(self, msg):
        key = msg + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        ser_key = hashlib.sha1(key).digest()
        return base64.b64encode(ser_key)
        # 通知客户端

    def carUrlThread(self, message):
        try:
            threads = threading.Thread(target=self.sendmessage, name='sendUrl', args=(message,))  # 线程对象.
            threads.start()  # 启动.
        except Exception as e:
            print("Error: sendUrl unable to start thread" + str(e))

    def sendmessage(self, message):
        s = socket.socket()  # 创建 socket 对象
        host = '127.0.0.1'  # socket.gethostname() # 获取本地主机名
        # host = socket.gethostname()
        port = 3888  # 设置端口号
        s.connect((host, port))
        s.send(message)
        s.close()
