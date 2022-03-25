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



# Makes a list of images in dir
def getImageNames():
    for img in os.listdir("./static/img"):
        listImgNames.append(img)
    
# Iterates through img list, gets img data, calls func to insert into table
# Denk wel handig om later de img file te verwijderen. Na het inserten naar database
# Verder deze func moet nog aangepast worden. Maak product object aan -> insert product to database

def getImgData():
    getImageNames()
    os.chdir("./static/img")
    for x in listImgNames:
        if ".png" in x or ".jpg" in x:
            with open(x,"rb") as z:
                data= z.read()
                insertImageTable(imgName= x, img=data)
                print("{} Added to Db".format(x))
        # elif ".jpg" in x:
        #     with open(x, "rb") as z:
        #         data = z.read()
        #         insertImageTable(imgName= x, img=data)
        #         print("{} Added to Db".format(x))

# Inserts name & imgdata into table.
def insertImageTable(imgName, img):
    os.chdir("..")
    os.chdir("..")
    with create_connection("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS testInsertImages(name TEXT, image BLOP)""")
        cursor.execute("""INSERT INTO testInsertImages(name, image) VALUES(?,?)""",(imgName, img))
        conn.commit()
        cursor.close()
    os.chdir("./static/img")


if __name__ == '__main__':
    #with create_connection("database.db") as db: #uncomment to drop table
    #   c = db.cursor()
    #   c.execute("""DROP TABLE Products;""")
    #createtable()
    #insertintotable('image', 'image_name', 20.5)
    #selectfromtable()
    getImgData()





