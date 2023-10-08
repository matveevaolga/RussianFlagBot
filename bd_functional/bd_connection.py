import pymysql
from config import db_config


class DBConnection:
    def __init__(self):
        # создание объекта подключения
        self.connection = pymysql.connections.Connection(
            autocommit=True,
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["db_name"]
        )

    def open_connect(self):
        # подключение к бд
        self.connection.connect()

    def close_connect(self):
        # закрытие подключения
        if self.connection.open:
            self.connection.close()

    def get_cursor(self):
        # курсор для выполнения запросов к бд
        return self.connection.cursor()
