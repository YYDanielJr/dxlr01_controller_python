from queue import Queue
import threading
from threading import Thread
from src.dxlr01 import *

class YYDoraMessageManager:
    def __init__(self, loraModule: dxlr01):
        self.sendQueue = Queue()
        self.resendQueue = Queue()
        self.receiveQueue = Queue()
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

    def send(self, text: str):
        self.sendMutex.acquire()
        self.sendQueue.put(text)
        self.sendMutex.release()

    def resend(self, text: str):
        self.resendMutex.acquire()
        self.resendQueue.put(text)
        self.resendMutex.release()

    def __receive__(self):
        while True:
            recv = self.loraModule.readline()
            self.receiveMutex.acquire()
            self.receiveQueue.put(recv)
            self.receiveMutex.release()
            sleep(0.05)

    def getReceived(self) -> str:
        self.receiveMutex.acquire()
        if self.receiveQueue.empty():
            return str()
        else:
            return self.receiveQueue.get()