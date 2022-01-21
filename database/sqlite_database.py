import psycopg2


class Connection:
    def __init__(self, host, database, user, password):
        self.__host = host
        self.__database = database
        self.__user = user
        self.__password = password

    def connect(self):
        connection = psycopg2.connect(
                         database=self.__database,
                         user=self.__user,
                         password=self.__password,
                         host=self.__host
        )
        return connection


class DBControl:
    def __init__(self, connection=None):
        self.__connection = connection
        connection.autocommit = True

    def add(self, data: tuple) -> None:
        with self.__connection.cursor() as curs:
            curs.execute(
                "INSERT INTO data (img, balance, description, region, price) VALUES (%s, %s, %s, %s, %s)", data
            )

    def readall(self):
        with self.__connection.cursor() as curs:
            curs.execute(
                "SELECT * FROM data"
            )
            data = curs.fetchall()
        return data

    def delete(self, data) -> None:
        with self.__connection.cursor() as curs:
            curs.execute("DELETE FROM data WHERE description = %s", (data,))

    def balance(self, position: tuple):
        with self.__connection.cursor() as curs:
            curs.execute(f"SELECT * FROM data WHERE balance BETWEEN '{position[0]}' AND '{position[1]}'")
            data = curs.fetchall()
        return data

    def region(self, position: tuple):
        with self.__connection.cursor() as curs:
            curs.execute(f"SELECT * FROM data WHERE region = '{position[0]}'", position)
            data = curs.fetchall()
        return data
