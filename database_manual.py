import sqlite3
import os
import json
from DbClasses import Product, Category, getPrice
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
            price real NOT NULL,
            category_id integer NOT NULL,
            description text NOT NULL,
            discount real,
            product_page text NOT NULL,
            image_link text NOT NULL,
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

def insertintoProductstable(name, price, category_id, description, discount):
    with create_connection("database.db") as db:
        cur = db.cursor()
        cur.execute(""" INSERT INTO Products (name, price, category_id, description, discount, product_page, image_link) 
            VALUES(?,?,?,?,?,?,?);""",(name, price, category_id, description, discount, product_page, image_link)) #id is autoincrement, so doesn't need to be defined

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
def getProductsJSON():
    productList = []
    a = open('static/DbData.json', "r")
    jsonObj = json.loads(a.read())
    for i in jsonObj:
        for j in jsonObj[i]:
            for k, productInfo in jsonObj[i][j].items():
                productList.append(productInfo)
    a.close()
    return productList

def getCategoriesJSON():
    categoryList = []
    a = open('static/DbData.json', "r")
    jsonObj = json.loads(a.read())
    for i in jsonObj:
        for j in jsonObj[i]:
            categoryList.append({'ProductType': i, 'Category': j})
    a.close()
    return categoryList

# Alle relevante informatie staat in de DbData.json file
# En dan bij de cursors.execute even de juiste categorie in parameters plaatsen.
def insertProductTable():
    productArr = getProductsJSON()
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    for p in productArr:
        name = p["Name"]
        price = p["Price"]
        categories = selectallFromTable("Categories")
        discount = p["Discount"]
        product_page = p["ProductPage"]
        image_link = p["ImageLink"]
        description = ""
        category_id = 0
        for category in categories:
            if category.category.upper() in name.upper():
                category_id = category.id
                description = "The product name is: " + name + ". The price is € " + getPrice(price,discount) + ". The product type is: " + category.product_type + " of category " + category.category
                break
        cursor.execute("""INSERT OR IGNORE INTO Products (name, price, category_id, description, discount, product_page, image_link) VALUES(?,?,?,?,?,?,?)""", (name, price, category_id, description, discount, product_page, image_link))
    conn.commit()
    cursor.close()
    conn.close()

def insertCategoryTable():
    categories = getCategoriesJSON()
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    for c in categories:
        cursor.execute("""INSERT OR IGNORE INTO Categories (product_type, category) VALUES(?,?)""", (c["ProductType"], c["Category"]))
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
    insertCategoryTable()
    insertProductTable()

#categories = ["Sweater & Hoodies", "Sport Pants", "Sweater", "Jeans", "Shirt"] 
#create list
#for each product, add:
#   Product(0, *Product Name (website)*, *image link*, *Product price*, *see categories for id*, *generate description*, *generate discount*)
#foreach product in list, add to db