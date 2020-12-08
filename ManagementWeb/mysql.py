import pymysql


class MySqlError(Exception):
    def __init__(self, arg):
        self.args = arg


class MySql:
    def __init__(self, Info):
        self.__db = pymysql.connect(host=Info['host'], user=Info['user'], passwd=Info['password'], db=Info['db'],
                                    port=3306, charset='utf8')
        self.__cursor = self.__db.cursor()


    def refresh(self):
        try:
            self.__db.ping()
        except:
            print('SQL error, try to reconnect')
            self.__cursor.close()
            self.__db.close()
            self.__db = pymysql.connect(host=Info['host'], user=Info['user'], passwd=Info['password'], db=Info['db'],
                                    port=3306, charset='utf8')
            self.__cursor = self.__db.cursor()


    def creat(self):
        self.refresh()
        sql1 = """
        CREATE TABLE `members` (
          `openid` text NOT NULL,
          `qq` bigint(20) NOT NULL,
          `stu_id` text NOT NULL,
          `name` text NOT NULL,
          `cn` text NOT NULL,
          `admin` int(11) NOT NULL,
          `other` text,
          PRIMARY KEY (`openid`(255))
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
        try:
            self.__cursor.execute(sql1)
            self.__db.commit()
        except:
            self.__db.rollback()
            self.__db.commit()
            raise MySqlError("Error happen when creat tables !")

    def fetchone(self, table, key, value):
        self.refresh()
        if isinstance(value, str):
            value = "'%s'" % value
        else:
            value = str(value)
        sql = "SELECT * from %s WHERE %s = %s" % (table, key, value)
        self.__cursor.execute(sql)
        result = self.__cursor.fetchone()
        if result is not None:
            return result
        else:
            return None

    def fetchall(self, table, key, value):
        self.refresh()
        if isinstance(value, str):
            value = "'%s'" % value
        else:
            value = str(value)
        sql = "SELECT * from %s WHERE %s = %s" % (table, key, value)
        try:
            self.__cursor.execute(sql)
            result = self.__cursor.fetchall()
            return result
        except Exception as e:
            raise MySqlError("Error happen when get date !")

    def getall(self, table):
        self.refresh()
        sql = "SELECT * from %s" % table
        try:
            self.__cursor.execute(sql)
            result = self.__cursor.fetchall()
            return result
        except:
            raise MySqlError("Error happen when get date !")

    def insert(self, table, data):
        self.refresh()
        KeyTable = ''
        ValueTable = ''
        for key, value in data.items():
            if isinstance(value, str):
                value = "'%s'" % value
            else:
                value = str(value)
            if value == '\'\'' or value is None or value == 'None':
                value = 'NULL'
            KeyTable += key + ', '
            ValueTable += value + ', '
        sql = "INSERT INTO %s" \
              "(%s) " \
              "VALUES" \
              "(%s)" % (table, KeyTable[:-2], ValueTable[:-2])
        self.__cursor.execute(sql)

    def update(self, table, key, value):
        self.refresh()
        if isinstance(value[1], str):
            value[1] = "'%s'" % value[1]
        else:
            value[1] = str(value[1])
        if isinstance(value[0], str):
            value[0] = "'%s'" % value[0]
        else:
            value[0] = str(value[0])
        if value[0] == '\'\'' or value[0] is None or value[0] == 'None':
            value[0] = 'NULL'
        sql = "UPDATE %s SET %s = %s WHERE %s = %s" % (table, key[0], value[0], key[1], value[1])
        self.__cursor.execute(sql)

    def remove(self, table, key, value):
        self.refresh()
        if isinstance(value, str):
            value = "'%s'" % value
        else:
            value = str(value)
        sql = "DELETE FROM %s WHERE %s = %s" % (table, key, value)
        self.__cursor.execute(sql)

    def commit(self):
        try:
            self.__db.commit()
        except:
            self.__db.rollback()
            self.__db.commit()
            raise MySqlError("Error happen when operate date !")

    def __del__(self):
        self.__cursor.close()
        self.__db.close()
