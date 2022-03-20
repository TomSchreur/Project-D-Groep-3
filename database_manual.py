import sqlite3
from sqlite3 import Error

#weet niet zeker of sqlite via pip moet gebeuren (bij mij niet). zoja, toevoegen bij requirements.txt

def create_connection(db_file):
    #create a database connection to a SQLite database, creates the file if it doesn't exist
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def createtable(cur):
    with create_connection("database.db") as db: #way to run queries to the database
        cur = db.cursor()
        cur.execute(""" CREATE TABLE IF NOT EXISTS Products (
            id integer PRIMARY KEY AUTOINCREMENT, 
            image text NOT NULL, 
            name text NOT NULL, 
            price real NOT NULL); """)#temporary string for image

def insertintotable(cur, image, name, price):
    with create_connection("database.db") as db:
        cur = db.cursor()
        cur.execute(""" INSERT INTO Products (image,name,price) 
            VALUES(?,?,?);""",(image,name,price))#id is autoincrement, so doesn't need to be defined

def selectfromtable():
    with create_connection("database.db") as db:
        cur = db.cursor()
        cur.execute("""SELECT * FROM Products;""")
        rows = cur.fetchall()
        return rows


if __name__ == '__main__':
    #with create_connection("database.db") as db: #uncomment to drop table
    #   c = db.cursor()
    #   c.execute("""DROP TABLE Products;""")
    createtable()
    insertintotable('image', 'image_name', 20.5)
    selectfromtable()





