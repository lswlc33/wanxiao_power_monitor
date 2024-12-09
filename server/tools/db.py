import sqlite3


class WanxiaoDB:
    def __init__(self, db_name="wanxiao.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._createTable()

    def _createTable(self):
        # 表不存在时创建表
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS powerData (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recordTime TEXT,
                buildId INTEGER,
                levelId INTEGER,
                roomFullId TEXT,
                buildName TEXT,
                levelName TEXT,
                roomName TEXT,
                roomState TEXT
            )
        """
        )
        self.conn.commit()

    def insertData(self, data):
        self.cursor.execute(
            """
            INSERT INTO powerData (recordTime, buildId, levelId, roomFullId, buildName, levelName, roomName, roomState)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            data,
        )
        self.conn.commit()

    def getData(self, sqlcom):
        self.cursor.execute(sqlcom)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

    def rebuild(self):
        self.cursor.execute("DROP TABLE IF EXISTS powerData")
        self._createTable()


if __name__ == "__main__":
    # 重建表
    db = WanxiaoDB()
    # db.rebuild()

    sql = "DELETE FROM powerData WHERE buildName = '大创园';"
    db.getData(sql)
    db.conn.commit()
    print()
