from pyodbc import connect
class DbContext:
    def __init__(self):
        self.database = connect("Driver={SQL Server};Server=PHATLAM;Database=MobileStore;Trusted_Connection=Yes")
    
    def __del__(self):
        self.database.close()

    def save(self, sql, arr):
        cur = self.database.cursor()
        cur.execute(sql, arr)
        ret = cur.rowcount
        self.database.commit()
        cur.close()
        return ret

    def saveBatch(self, sql, arr):
        cur = self.database.cursor()
        cur.executemany(sql, arr)
        ret = cur.rowcount
        self.database.commit()
        cur.close()
        return ret

    def fetchOne(self, sql, arr):
        cur = self.database.cursor()
        cur.execute(sql, arr)
        v = cur.fetchone()
        cur.close()
        return v

    def fetchAll(self, sql, arr = None):
        cur = self.database.cursor()
        if arr:
            cur.execute(sql, arr)
        else:
            cur.execute(sql)
        a = cur.fetchall()
        cur.close()
        return a