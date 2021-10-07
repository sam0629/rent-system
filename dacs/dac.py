import pymysql

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'A127948715',
    'db': 'project',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor
}


class Dac:
    def __init__(self):
        self._config = config

    def _qry(self, sql, params=None):
        with pymysql.connect(**self._config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor

    def qry_all(self, sql, params=None):
        ''' 查詢全部 '''
        cursor = self._qry(sql, params)
        return cursor.fetchall()

    def qry_one(self, sql, params=None):
        ''' 查詢一筆 '''
        cursor = self._qry(sql, params)
        return cursor.fetchone()

    def exec_cmd(self, sql, params=None):
        '''執行命令 (新增、修改、刪除)'''
        with pymysql.connect(**self._config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
            conn.commit()

