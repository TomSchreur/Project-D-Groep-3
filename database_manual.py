import sqlite3
import os
import sys
from sqlite3 import Error

#weet niet zeker of sqlite via pip moet gebeuren (bij mij niet). zoja, toevoegen bij requirements.txt
listImgNames=[]

def create_connection(db_file):
    #create a database connection to a SQLite database, creates the file if it doesn't exist
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def createtable():
    with create_connection("database.db") as db: #way to run queries to the database
        cur = db.cursor()
        cur.execute(""" CREATE TABLE IF NOT EXISTS Products (
            id integer PRIMARY KEY AUTOINCREMENT, 
            name text NOT NULL UNIQUE, 
            price real NOT NULL,
            category text NOT NULL); """)#temporary string for image

def insertintotable(cur, image, name, category):
    with create_connection("database.db") as db:
        cur = db.cursor()
        cur.execute(""" INSERT INTO Products (name,price,category) 
            VALUES(?,?,?);""",(image,name,category))#id is autoincrement, so doesn't need to be defined

def selectfromtable():
    with create_connection("database.db") as db:
        cur = db.cursor()
        cur.execute("""SELECT * FROM Products;""")
        rows = cur.fetchall()
        return rows

# Selecteert producten uit db, die dezelfde naam hebben als de top30 vergeleken afbeeldingen
def selectProducts(names):
    listProductDetails=[]
    with create_connection("database.db") as db:
        cur = db.cursor()
        for n in names:
            cur.execute("SELECT * from Products WHERE name=(?);",(n,))
            rows = cur.fetchall()
            if rows == []:
                continue
            else:
                listProductDetails.append(rows)
    removeNestedList = [v for sublist in listProductDetails for v in sublist]
    return removeNestedList

# Makes a list of images in dir
def getImageNames(dir):
    for img in os.listdir(dir):
        listImgNames.append(img)
    return listImgNames

# Image file naam, MOET gerelateerd zijn aan de product (bijv. een zwarte spijkerbroek -> filenaam: Dark Jeans (15))
# En dan bij de cursors.execute even de juiste categorie in parameters plaatsen.
def insertProductTable(dir):
    paths = getImageNames(dir)
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    for p in paths:
        cursor.execute("""INSERT OR IGNORE INTO Products(name, price, category) VALUES(?,?,?)""",(p, 50, 'Sweater'))
    conn.commit()
    cursor.close()
    conn.close()



if __name__ == '__main__':
    #with create_connection("database.db") as db: #uncomment to drop table
    #   c = db.cursor()
    #   c.execute("""DROP TABLE Products;""")
    #createtable()
    #insertintotable('image', 'image_name', 20.5)
    selectfromtable()
    #getImgData()
    #insertProductTable('./static/zwart_truien')