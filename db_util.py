import mysql


def get_database_connection():
    dataBase = mysql.connector.connect(
        host ="localhost",
        user ="henry",
        passwd ="henryadmin",
        database = "bookstore"
    )

    return dataBase
