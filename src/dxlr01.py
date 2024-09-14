'''
Author: Y.Y. Daniel 626986815@qq.com
Date: 2024-08-01 17:31:20
LastEditors: Y.Y. Daniel 626986815@qq.com
LastEditTime: 2024-08-19 20:02:58
FilePath: /dxlr01_controller_python/dxlr01.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

import time
from time import sleep
import serial
import logging
import threading
import sqlite3
import json

logger = logging.getLogger(__name__)
locker = threading.Lock()

class dxlr01:
    def testModule(self) -> bool:
        length = self.ser.write("+++\r\n".encode())
        sleep(0.5)
        recv = self.ser.readline()
        if recv == b'Entry AT\r\n':
            length = self.ser.write("+++\r\n".encode())
            sleep(0.5)
            recv = self.ser.readline()
            if recv == b'Exit AT\r\n':
                return True
            else:
                print("Received bytes when trying to +++, but not a standard reply: " + recv.decode())
                return False
        elif recv == b'Exit AT\r\n':
            return True
        else:
            print("Received bytes when trying to +++, but not a standard reply: " + recv.decode())
            return False
    
    def __init__(self, serialPath, baudRate):
        self.serialPath = serialPath
        self.baudrate = baudRate
        self.ser = serial.Serial(serialPath, baudRate)
        if self.ser.is_open:
            logger.info("Successfully opened serial on {} with baudrate {}. Now we will test if the dxlr01 module is available for use.".format(serialPath, baudRate))
            if self.testModule():
                logger.info("Module test passed. This module is ready to use.")
                print("Module test passed. This module is ready to use.\n")
                sleep(0.1)
                self.ser.readline() # 把重新启动时向串口发送的Power on过滤掉
            else:
                logger.error("Module test failed. Please check if this module is correct.")
        else:
            logger.error("Unable to open serial on {}".format(serialPath))
            
            
    ##########
    def testFun(self) -> float:
        sum = 0.0
        self.ser.write("Ready\r\n".encode())
        if self.ser.readline() == b"Ready\r\n":
            for i in range(0, 10):
                str = "{'number': msg_count,'date': datetime.datetime.now().timestamp(),'temp': random.randrange(20, 25),'humi': random.randrange(45, 50),'illu': random.randrange(3000, 3100)}"
                t1 = time.perf_counter()
                self.ser.write(f"{str}\r\n".encode())
                while True:
                    recv = self.ser.readline()
                    if recv == f"{str}\r\n".encode():
                        t2 = time.perf_counter()
                        print("Successfully sent one piece of message.")
                        sum = sum + t2 - t1
                        break
        return sum / 10.0
        
    ##########
    
    def runATCommand(self, command:str) -> list:
        ret = list()
        length = self.ser.write("+++\r\n".encode())
        sleep(0.1)
        if length > 0:
            recv = self.ser.readline()
            if recv == b'Entry AT\r\n':
                length = self.ser.write(f"{command}\r\n".encode())
                sleep(0.5)
                while self.ser.in_waiting > 0:
                    temp = self.ser.readline()
                    ret.append(temp.decode())
                    sleep(0.1)
                self.ser.write("AT+CHANNEL\r\n".encode())
                sleep(0.1)
                temp = self.ser.readline()
                ret.append(temp.decode())
                self.ser.write("+++\r\n".encode())
                sleep(0.1)
                self.ser.readline()
                return ret
            else:
                print("Received bytes when trying to +++, but not a standard reply: " + recv.decode())
                return list()
                # 此处之后需要改变为异常处理
        else:
            print("Nothing received.")
            return list()
            # 此处之后需要改变为异常处理
        
    def runATCommands(self, commands:list) -> int:
        length = self.ser.write("+++\r\n".encode())
        sleep(0.1)
        if length > 0:
            recv = self.ser.readline()
            if recv == b'Entry AT\r\n':
                for i in commands:
                    length = self.ser.write(f"{i}\r\n".encode())
                    sleep(0.1)
                    while self.ser.in_waiting > 0:
                        self.ser.readline()
                    sleep(0.1)
                self.ser.write("+++\r\n".encode())
                sleep(0.1)
                self.ser.readline()
                return 0
            else:
                print("Received bytes when trying to +++, but not a standard reply: " + recv.decode())
                return -1
                # 此处之后需要改变为异常处理
        else:
            print("Nothing received.")
            return -2
            # 此处之后需要改变为异常处理
    
    def getParams(self):
        paramsList = list()
        try:
            paramsList = self.runATCommand("AT+HELP")
        except:
            print("Can't send AT command to LoRa module.")
        
        # print("Received AT+HELP")
        # 以下为测试代码
        # for i in paramsList:
        #     print(i)
        jsonData = {}
        for i in paramsList:
            if "MODE:" in i:
                self.mode = int(i[5:len(i) - 2])
                jsonData["mode"] = self.mode
            if "LEVEL:" in i:
                self.level = int(i[6])
                jsonData["level"] = self.level
            if "SLEEP:" in i:
                self.sleep = int(i[6:len(i) - 2])
                jsonData["sleep"] = self.sleep
            if "+CHANNEL=" in i:
                # 频率和信道等效，我们使用信道。
                self.channel = i[9:len(i) - 2]
                jsonData["channel"] = self.channel
            if "MAC:" in i:
                self.mac = [i[4:6], i[7:9]]
                jsonData["mac"] = self.mac
            if "Bandwidth:" in i:
                self.bandwidth = int(i[10:len(i) - 2])
                jsonData["bandwidth"] = self.bandwidth
            if "Spreading Factor:" in i:
                self.spreadingFactor = int(i[len("Spreading Factor:"):len(i) - 2])
                jsonData["spreading factor"] = self.spreadingFactor
            if "Coding rate:" in i:
                self.codingRate = int(i[len("Coding rate:"):len(i) - 2])
                jsonData["coding rate"] = self.codingRate
            if "CRC:" in i:
                self.crc = int(i[4])
                jsonData["crc"] = self.crc
            if "Preamble:" in i:
                self.preamble = int(i[len("Preamble:"):len(i) - 2])
                jsonData["preamble"] = self.preamble
            if "IQ:" in i:
                self.iq = int(i[3])
                jsonData["iq"] = self.iq
            if "Power:" in i:
                self.power = int(i[6:len(i) - 5])
                jsonData["power"] = self.power
        with open("current_dxlr01_params.json", "w+") as f:
            json.dump(jsonData, f)
    
    def loadProfile(self, profilePath = "profile.json"):
        loadList = []
        with open(profilePath, "r+") as file:
            profile = json.load(file)
            if profile.get("mode") != None:
                loadList.append(f'AT+MODE{profile.get("mode")}\r\n')
            if profile.get("channel") != None:
                loadList.append(f'AT+CHANNEL{profile.get("channel")}\r\n')
            if profile.get("level") != None:
                loadList.append(f'AT+LEVEL{profile.get("level")}\r\n')
            if profile.get("sleep") != None:
                loadList.append(f'AT+SLEEP{profile.get("sleep")}\r\n')
        
        if loadList:
            if self.runATCommands(loadList) == 0:
                print("Load profiles successfully. ")
            
            
    def writeContinuously(self):
        while True:
            locker.acquire()
            self.ser.write(b"Sending message from Python client.\r\n")
            print("A message has sent.")
            if locker.locked():
                locker.release()
            sleep(2)
    
    def readContinuously(self):
        sqliteConnection = sqlite3.connect('database.db')
        sqliteCur = sqliteConnection.cursor()
        sqliteCur.execute("CREATE TABLE IF NOT EXISTS test(id INTEGER PRIMARY KEY,message TEXT);")
        sqliteConnection.commit()
        # sqliteCur.execute("select * from test order by id desc limit 0,1;")
        # sqliteConnection.commit()
        
        receiveCount = 100
        while True:
            locker.acquire()
            isReadable = self.ser.in_waiting
            if locker.locked():
                locker.release()
            if isReadable > 0:
                try:
                    print("*****Read ONE MESSAGE*****")
                    locker.acquire()
                    str = self.ser.readline()
                    if locker.locked():
                        locker.release()
                    if str:
                        receiveCount = receiveCount + 1
                        str = str.decode('utf-8')
                        sqliteCur.execute('insert into test values({}, \"{}\");'.format(receiveCount, str))
                        sqliteConnection.commit()
                        print("A message has been received and stored in database.")
                except:
                    continue
            else:
                sleep(0.1)