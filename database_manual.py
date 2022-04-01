import sqlite3
import os
from Product_class import Product
import random
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
            image_path text NOT NULL UNIQUE,
            df_path text NOT NULL UNIQUE,
            price real NOT NULL,
            category text NOT NULL,
            tts_path text NOT NULL); """)

def insertintotable(cur, name, image_path, df_path, price, category, tts_path):
    with create_connection("database.db") as db:
        cur = db.cursor()
        cur.execute(""" INSERT INTO Products (name, image_path, df_path, price, category, tts_path) 
            VALUES(?,?,?,?,?);""",(name, image_path, df_path, price, category, tts_path))#id is autoincrement, so doesn't need to be defined

def selectallProducts():
    with create_connection("database.db") as db:
        cur = db.cursor()
        cur.execute("""SELECT * FROM Products;""")
        rows = cur.fetchall()
        for i in range(len(rows)):
            rows[i] = Product(*rows[i])
        return rows

# Selecteert producten uit db, die dezelfde naam hebben als de top30 vergeleken afbeeldingen
def selectProducts(names):
    listProductDetails=[]
    with create_connection("database.db") as db:
        cur = db.cursor()
        for n in names:
            cur.execute("SELECT * from Products WHERE name=(?);",(os.path.splitext(n)[0],))
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
        name = os.path.splitext(p)[0]
        image_path = dir + "/" + p
        df_path = "./static/feature/" + name + ".npy"
        price = float(random.randint(10,60))
        category = ""
        categories = ["Sweater & hoodies", "sport pants", "sweater", "Jeans", "shirt", "Sweater", "Shirt"]
        tts_path = "./static/mp3files/" + name + ".mp3"
        for cat in categories:
            if cat in name:
                category = cat
                continue
        cursor.execute("""INSERT OR IGNORE INTO Products (name, image_path, df_path, price, category, tts_path) VALUES(?,?,?,?,?,?)""",(name, image_path, df_path, price, category,tts_path))
    conn.commit()
    cursor.close()
    conn.close()



if __name__ == '__main__':
    #with create_connection("database.db") as db: #uncomment to drop table
    #   c = db.cursor()
    #   c.execute("""DROP TABLE Products;""")
    #createtable()
    #insertintotable('image', 'image_name', 20.5)
    #insertProductTable('./static/img')
    #insertProductTable('./static/zwart_truien')
    print(selectallProducts()[0].tts_path)
    #getImgData()
