from queue import Queue
import threading
from threading import Thread
from src.dxlr01 import *

class YYDoraMessageManager:
    def __init__(self, loraModule: dxlr01):
        self.sendQueue = Queue()
        self.resendQueue = Queue()
        self.sendMutex = threading.Lock()
        self.resendMutex = threading.Lock()
        self.loraModule = loraModule
        manageThread = Thread(target=self.__queue_manager__, daemon=True)
        manageThread.start()

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
