import mysql.connector
from mysql.connector import Error

class DB:
    def __init__(self,host_name, user_name, user_password, db_name):
        self.host_name = host_name
        self.user_name = user_name
        self.user_password = user_password
        self.db_name = db_name

    def sql_connector(self):
        connection = None
        try:
            connection = mysql.connector.connect(
                host = self.host_name,
                user = self.user_name,
                passwd = self.user_password,
                database = self.db_name
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

        return connection


def connect_db():
    obj = DB('localhost','root','aditya@285','ATM')
    conn = obj.sql_connector()
    return conn

if __name__ == "__main__":
    connect_db()