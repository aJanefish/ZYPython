# -*- coding: utf-8 -*-
# ZY
from zysocket.socket_utils import ZYSocketThread
from zyutils.zysocket import LongServerThread

if __name__ == '__main__':
    print("ZY SOCKET MAIN")
    flag = 2
    if flag == 1:  # Socket 长链接 支持python2.7
        LongServerThread(9000).start()
        pass
    elif flag == 2:  # Socket 传输
        ZYSocketThread(8989).start()
        pass
