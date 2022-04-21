import sqlite3
import os
from DbClasses import Product, Category
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

def createProducttable():
    with create_connection("database.db") as db: #way to run queries to the database
        cur = db.cursor()
        cur.execute(""" CREATE TABLE IF NOT EXISTS Products (
            id integer PRIMARY KEY AUTOINCREMENT, 
            name text NOT NULL UNIQUE, 
            image_path text NOT NULL UNIQUE,
            price real NOT NULL,
            category_id integer NOT NULL,
            tts_path text NOT NULL,
            description text NOT NULL,
            discount real,
            FOREIGN KEY(category_id) REFERENCES Categories(id)
            ); """)

def createCategorytable():
    with create_connection("database.db") as db:
        cur = db.cursor()
        cur.execute(""" CREATE TABLE IF NOT EXISTS Categories (
            id integer PRIMARY KEY AUTOINCREMENT, 
            product_type text NOT NULL,
            category text NOT NULL UNIQUE
            ); """)

def insertintoProductstable(name, image_path, price, category_id, tts_path, description, discount):
    with create_connection("database.db") as db:
        cur = db.cursor()
        cur.execute(""" INSERT INTO Products (name, image_path, price, category_id, tts_path, description, discount) 
            VALUES(?,?,?,?,?,?,?);""",(name, image_path, price, category_id, tts_path, description, discount)) #id is autoincrement, so doesn't need to be defined

def insertintoCategorytable(product_type, category):
    with create_connection("database.db") as db:
        cur = db.cursor()
        cur.execute(""" INSERT INTO Categories (product_type, category) 
            VALUES(?,?);""",(product_type, category))

def selectallFromTable(table_name):
    with create_connection("database.db") as db:
        cur = db.cursor()
        # query = f"""SELECT * FROM {table_name}"""
        cur.execute(f"""SELECT * FROM {table_name}""")
        rows = cur.fetchall()
        for i in range(len(rows)):
            if(table_name == "Products"):
                rows[i] = Product(*rows[i])
            elif(table_name == "Categories"):
                rows[i] = Category(*rows[i])
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
        price = float(random.randint(10,60))
        categories = selectallFromTable("Categories")
        for category in categories:
            if category.category.upper() in name.upper():
                category_id = category.id
                break
        # category = ""
        # categories = ["Sweater & hoodies", "Sport Pants", "Sweater", "Jeans", "Shirt"]
        # for cat in categories:
        #     if cat.upper() in name.upper():
        #         category = cat.upper()
        #         continue
        tts_path = "./static/mp3files/" + name + ".mp3"
        description = "" # is empty rn, make this generate dynamically depending on product
        discount = round(random.random(), 2) # can be anything above 0.0; currently a random float (0.xx)
        cursor.execute("""INSERT OR IGNORE INTO Products (name, image_path, price, category_id, tts_path, description, discount) VALUES(?,?,?,?,?,?,?)""", (name, image_path, price, category_id, tts_path, description, discount))
    conn.commit()
    cursor.close()
    conn.close()

# "Sweater & hoodies", "sport pants", "Sweater", "Jeans", "Shirt"
def insertCategoryTable(dir):
    categories = ["Sweater & hoodies", "Sport Pants", "Sweater", "Jeans", "Shirt"] # expand later (make sure categories containing later categories like 'sweater & hoodies' and 'sweater' are earlier)
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    for c in categories:
        cursor.execute("""INSERT OR IGNORE INTO Categories (product_type, category) VALUES(?,?)""", ("Clothing", c.upper()))
    conn.commit()
    cursor.close()
    conn.close()
    

if __name__ == '__main__':
    with create_connection("database.db") as db: #uncomment to drop table
        c = db.cursor()
        c.execute("""DROP TABLE Products;""")
        c.execute("""DROP TABLE Categories""")
    createProducttable()
    createCategorytable()
    insertCategoryTable('./static/img')
    insertProductTable('./static/img')
    #print(selectallFromTable()[0].tts_path)
