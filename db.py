
import sqlite3
import logging
import datetime

__all__ = ['setup', 'save']

class Database(object):
    def __init__(self):
        self.database = 'dummy.db'
        self.connection = None
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',filename='app.log',level=logging.DEBUG)          

    def connect(self):
        try:
            self.connection =  sqlite3.connect(self.database) 
            cursor = self.connection.cursor()
            logging.info('Database created and successfully connected')
            cursor.close()

        except sqlite3.Error as error:
            logging.error('Error while connecting to sqlite: %s', error)

    def create_some_table(self):
        try:
            query = '''CREATE TABLE IF NOT EXISTS some_table (
                            id INTEGER PRIMARY KEY,
                            future TEXT NOT NULL,
                            date datetime);'''

            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            logging.info('Table some_table created')

            cursor.close()

        except sqlite3.Error as error:
            logging.error('Error while creating a table: %s', error)  

    def insert(self, file=None):
        try:
            query = """INSERT INTO `some_table`
                          ('future', 'date') 
                           VALUES 
                          (?, ?)"""
            data = (file, datetime.datetime.now())
            cursor = self.connection.cursor()
            count = cursor.execute(query, data)
            self.connection.commit()
            logging.info('Record inserted successfully into some_table: %s', cursor.rowcount)
            cursor.close()

        except sqlite3.Error as error:
            logging.error('Failed to insert data into sqlite table %s', error)

    def disconnect(self):
        try:
            if (self.connection):
                self.connection.close()
                logging.info('The database connection is closed')  
        except Exception as e:
            logging.error('Failed to close database connection %s', error)


            
def setup():
    db = Database()
    db.connect()
    db.create_some_table()
    db.disconnect()

def save(file):
    db = Database()
    db.connect()
    db.insert()
    db.disconnect()