'''
Author: Y.Y. Daniel 626986815@qq.com
Date: 2025-01-10 18:52:25
LastEditors: Y.Y. Daniel 626986815@qq.com
LastEditTime: 2025-01-10 21:40:39
FilePath: /dxlr01_controller_python/src/data_processor.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from time import sleep
from src.mySqlite import *
import threading
import datetime
import re

class DataProcessor:
    def __init__(self):
        self.sqliteConnector = SqliteConnector()
        self.temp = []
        self.humi = []
        autosaveThread = threading.Thread(target=self.__autosave__, daemon=True)
        autosaveThread.start()
        self.listLock = threading.Lock()
        self.sqliteLock = threading.Lock()

    def processData(self, text: str):
        pattern = r'H(\d+\.\d+)T(\d+\.\d+)'
        match = re.match(pattern, text)
        if match:
            tempF = float(match.group(2))
            humiF = float(match.group(1))
            with self.listLock:
                self.temp.append(tempF)
                self.humi.append(humiF)

    # 当秒针归0时，自动获取过去一分钟内的温度、湿度最大值作为上一分钟的值，写进数据库，清空温湿度缓冲区
    # 当分针为0或30时，自动获取过去半小时内的数据，计算这些数据的平均值，写入数据库
    def __autosave__(self):
        while True:
            curTime = datetime.datetime.now()
            # 秒针归零自动保存短期数据
            if curTime.second == 0:
                if len(self.humi) > 0 and len(self.temp) > 0:
                    with self.listLock:
                        self.temp.sort(reverse=True)
                        highestTemp = self.temp[0]
                        self.humi.sort(reverse=True)
                        highestHumi = self.humi[0]
                        self.temp.clear()
                        self.humi.clear()
                    # curTime.minute = curTime.minute - 1
                    curTime = curTime - datetime.timedelta(minutes = 1)
                    # curTime.microsecond = 0
                    curTime = curTime.replace(microsecond=0)
                    with self.sqliteLock:
                        self.sqliteConnector.save60minData(curTime, highestTemp, highestHumi)
                    # curTime.minute = curTime.minute + 1
                    curTime = curTime + datetime.timedelta(minutes = 1)
                    sleep(1)

            # 分针归0或30自动保存长期数据
            if (curTime.minute == 0 or curTime.minute == 30) and curTime.second == 0:
                with self.sqliteLock:
                    datas = self.sqliteConnector.get30minData(curTime.timestamp())

                with self.sqliteLock:
                    self.sqliteConnector.save24hData(curTime, datas[0], datas[1])
                sleep(1)
            sleep(0.1)