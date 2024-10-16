from queue import Queue
import threading
from threading import Thread
from src.dxlr01 import *
from src.yydora.parser import *

class YYDoraMessageManager:
    def __init__(self, loraModule: dxlr01):
        self.sendQueue = Queue()
        self.resendQueue = Queue()
        self.receiveQueue = Queue()
        self.receiveBufferQueue = Queue()
        self.sendMutex = threading.Lock()
        self.resendMutex = threading.Lock()
        self.receiveMutex = threading.Lock()
        self.loraModule = loraModule
        manageThread = Thread(target=self.__queue_manager__, daemon=True)
        manageThread.start()
        receiveThread = Thread(target=self.__receive__, daemon=True)
        receiveThread.start()

    def __queue_manager__(self):
        while not self.resendQueue.empty():
            self.resendMutex.acquire()
            self.loraModule.write(self.resendQueue.get())
            self.resendMutex.release()

        while not self.sendQueue.empty():
            self.sendMutex.acquire()
            self.loraModule.write(self.sendQueue.get())
            self.sendMutex.release()

        sleep(0.05)

    def send(self, text: bytes):
        self.sendMutex.acquire()
        self.sendQueue.put(text)
        self.sendMutex.release()

    def resend(self, text: bytes):
        self.resendMutex.acquire()
        self.resendQueue.put(text)
        self.resendMutex.release()

    def __receive__(self):
        while True:
            print("***receiving***")
            recv = self.loraModule.readline()
            if recv.isValid():
                # 只对非重传报文发送重传请求，正常发送的报文和接收到的重传报文直接入队
                # if recv.getPackageType() == 0 and (self.receiveBufferQueue.empty() or recv.getPackageNumber() == self.receiveBufferQueue.queue[0].getPackageNumber() + 1 or recv.getPackageNumber() == 0) or recv.getPackageType() == 3:
                if recv.getPackageType() == 0 or recv.getPackageType() == 3:
                    self.receiveMutex.acquire()
                    self.receiveQueue.put(recv)
                    self.receiveMutex.release()
                    if recv.getPackageType() == 0 and (not self.receiveBufferQueue.empty()):
                        self.receiveBufferQueue.get()
                    self.receiveBufferQueue.put(recv)
                else:
                    print("***关系不满足，不入队，进行重传***")
                    if recv.getPackageNumber() - self.receiveBufferQueue.queue[0].getPackageNumber() <= 0:
                        currentPackageNumber = recv.getPackageNumber() + 9999
                    lastPackageNumber = self.receiveBufferQueue.queue[0].getPackageNumber()
                    for i in range(lastPackageNumber + 1, currentPackageNumber):
                        self.resend(yydoraResendRequestParser(i % 9999, recv.getLongPackageNumber()))
            else:
                print("***NOT VALID***")
            sleep(0.05)

    def getReceived(self) -> str:
        self.receiveMutex.acquire(timeout=1)
        if self.receiveQueue.empty():
            self.receiveMutex.release()
            return str()
        else:
            ret = self.receiveQueue.get()
            self.receiveMutex.release()
            return ret.getText()