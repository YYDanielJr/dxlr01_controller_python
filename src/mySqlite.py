'''
Author: Y.Y. Daniel 626986815@qq.com
Date: 2025-01-10 18:52:25
LastEditors: Y.Y. Daniel 626986815@qq.com
LastEditTime: 2025-01-10 21:35:29
FilePath: /dxlr01_controller_python/src/mySqlite.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import datetime
import sqlite3
import time

class SqliteConnector:
    def __init__(self):
        conn = sqlite3.connect("./db/historyData.db")
        cur = conn.cursor()
        cur.execute('''create table if not exists last24h
                         (time real primary key not null,
                         temp real,
                         humi real);''')
        cur.execute('''create table if not exists last60min
                         (time real primary key not null,
                         temp real,
                         humi real);''')
        conn.commit()
        cur.close()
        conn.close()

    def save60minData(self, curDateTime: datetime, temp, humi):
        conn = sqlite3.connect("./db/historyData.db")
        cur = conn.cursor()
        cur.execute('''insert into last60min values
                    (?, ?, ?);''', (curDateTime.timestamp(), temp, humi))
        conn.commit()
        # print("*向last60min插入数据完成。")

        # 获取表中项目的数量
        cur.execute('SELECT COUNT(*) FROM last60min;')
        count = cur.fetchone()[0]

        # 如果数量超过60个，则删除最早的项目，直到数量小于等于60
        while count > 60:
            cur.execute('DELETE FROM last60min WHERE time = (SELECT MIN(time) FROM last60min);')
            count -= 1

        conn.commit()
        cur.close()
        conn.close()

    def save24hData(self, curDateTime: datetime, temp, humi):
        conn = sqlite3.connect("./db/historyData.db")
        cur = conn.cursor()
        cur.execute('''insert into last24h values
                    (?, ?, ?);''', (curDateTime.timestamp(), temp, humi))
        conn.commit()
        cur.close()
        conn.close()

    def get60minData(self):
        conn = sqlite3.connect("./db/historyData.db")
        cur = conn.cursor()
        ret = cur.execute("select * from last60min;")
        cur.close()
        conn.close()
        return ret

    def get30minData(self, timestamp):
        conn = sqlite3.connect("./db/historyData.db")
        cur = conn.cursor()
        cursor = cur.execute("select * from last60min where time between ? and ?;", (timestamp - 30 * 60, timestamp))
        temp = 0.0
        humi = 0.0
        count = 0
        for row in cursor:
            temp = temp + float(row[1])
            humi = humi + float(row[2])
            count = count + 1
        temp = temp / count
        humi = humi / count
        cur.close()
        conn.close()
        return [temp, humi]