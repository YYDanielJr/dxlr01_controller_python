'''
Author: Y.Y. Daniel 626986815@qq.com
Date: 2024-08-01 17:23:42
LastEditors: Y.Y. Daniel 626986815@qq.com
LastEditTime: 2024-08-19 20:00:23
FilePath: /dxlr01_controller_python/main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

import sys
from src.dxlr01 import *
import threading
import json
from src.yydora.parser import *
from src.yydora.manager import *

def main() -> int:
    loraModule = dxlr01('com8', 9600, False)
    manager = YYDoraMessageManager(loraModule)
    # # writeThread = threading.Thread(target=loraModule.writeContinuously, name='continuouslyWrite')
    # # readThread = threading.Thread(target=loraModule.readContinuously, name='continuouslyRead')
    # # writeThread.start()
    # # readThread.start()
    # # writeThread.join()
    # # readThread.join()

    # # loraModule.getParams()
    # res = loraModule.testFun()
    # print("**********Test Result**********\n")
    # print(f"\tAverage time: {res} s.\n")
    # print("*******************************")

    # teststr = "Now we will have a test on long strings. We will test if the time is affordable when calculating crc32 of a long string. "
    # print(yydoraParser(teststr).decode())
    # print(yydoraUnparser(yydoraParser(teststr)))
    while True:
        print(manager.getReceived())
        sleep(1)

if __name__ == '__main__':
    main()