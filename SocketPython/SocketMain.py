# -*- coding: utf-8 -*-
# ZY
from zyutils.zysocket import LongServerThread

if __name__ == '__main__':
    print("ZY SOCKET MAIN")
    flag = 1
    if flag == 1:  # Socket 长链接 支持python2.7
        LongServerThread(9000).start()
        pass
    elif flag == 2:
        pass
