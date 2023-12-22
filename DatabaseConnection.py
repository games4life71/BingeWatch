import sqlite3


class DatabaseConnection:
    def __init__(self, databasePath):
        self.databasePath = databasePath
        self.connection = None
    def connect(self):
        try:
           return  sqlite3.connect(self.databasePath)
        except sqlite3.Error as error:
            # TODO in future: log error
            print(error)

    def disconnect(self):
        try:
            sqlite3.connect(self.databasePath).close()
        except sqlite3.Error as error:
            # TODO in future: log error
            print(error)
