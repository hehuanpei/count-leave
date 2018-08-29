import sqlite3


def connectSql(dbName, isolation_level=True):
    if not isolation_level:
        sql = sqlite3.connect(dbName, isolation_level=None)
    else:
        sql = sqlite3.connect(dbName)

    return sql


def getCursor(dbName):

    return dbName.cursor()


def commitAndClose(sql, cursor=None):
    sql.commit()

    if cursor:
        cursor.close()

    sql.close()


class SqlManager(object):
    """方便的上下文管理，返回游标。"""
    def __init__(self, dbName, isolation_level=True):

        self.dbName = dbName
        self.isolation_level = isolation_level
        self.db = None
        self.cursor = None

    def __enter__(self):
        # print(self.dbName)
        self.db = connectSql(self.dbName)
        self.cursor = getCursor(self.db)

        return self.cursor

    def __exit__(self, except_type, value, tb):

        commitAndClose(self.db, self.cursor)

        return False



# def createGroups(cursor):


#     cursor.execute()



