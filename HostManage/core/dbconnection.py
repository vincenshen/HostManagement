import pymysql
from HostManage.conf.settings import mysql


class DBConn(object):
    def __init__(self):
        self.__conn = None
        self.__cursor = None
        self.db_cursor = self.db_connect()

    def db_connect(self):
        conn = pymysql.connect(host=mysql["host"],
                               port=mysql["port"],
                               user=mysql["user"],
                               password=mysql["passwd"],
                               db=mysql["db"])
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        self.__conn = conn
        self.__cursor = cursor
        return cursor

    def host(self, user_name):
        self.db_cursor.execute("select h.ip,h.port,h.username,h.password from users u "
                          "left join user_to_host uh on u.id=uh.uid "
                          "left join hosts h on h.id=uh.hid "
                          "where u.username=%s", (user_name,))
        return self.db_cursor.fetchall()

    def auth(self, user_name, pass_word):
        self.db_cursor.execute("select * from users where username=%s and password=%s", (user_name, pass_word))
        if self.db_cursor.fetchall():
            return True

    def __del__(self):
        self.__conn.close()
        self.__cursor.close()


if __name__ == '__main__':
    conn = DBConn()
    host_list = conn.host("alex")
    for n, k in enumerate(host_list):
        print(n, ":", k["ip"])