import datetime
import sqlite3
import time

class SqliteConnector:
    def __init__(self):
        self.conn = sqlite3.connect("./db/historyData.db")
        self.cur = self.conn.cursor()
        self.cur.execute('''create table if not exists last24h
                         (time real primary key not null,
                         temp real,
                         humi real);''')
        self.cur.execute('''create table if not exists last60min
                         (time real primary key not null,
                         temp real,
                         humi real);''')
        self.conn.commit()

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def save60minData(self, curDateTime: datetime, temp, humi):
        self.cur.execute('''insert into last60min values
                    (?, ?, ?);''', curDateTime.timestamp(), temp, humi)
        self.conn.commit()
        print("向last60min插入数据完成。")

        # 获取表中项目的数量
        self.cur.execute('SELECT COUNT(*) FROM last60min;')
        count = self.cur.fetchone()[0]

        # 如果数量超过60个，则删除最早的项目，直到数量小于等于60
        while count > 60:
            self.cur.execute('DELETE FROM last60min WHERE time = (SELECT MIN(time) FROM last60min);')
            count -= 1

        self.conn.commit()

    def save24hData(self, curDateTime: datetime, temp, humi):
        self.cur.execute('''insert into last24h values
                    (?, ?, ?);''', curDateTime.timestamp(), temp, humi)
        self.conn.commit()

    def get60minData(self):
        return self.cur.execute("select * from last60min;")

    def get30minData(self, timestamp):
        cursor = self.cur.execute("seletc * from last60min where time between ? and ?;", (timestamp - 30 * 60, timestamp))
        temp = 0.0
        humi = 0.0
        count = 0
        for row in cursor:
            temp = temp + float(row[1])
            humi = humi + float(row[2])
            count = count + 1
        temp = temp / count
        humi = humi / count
        return [temp, humi]