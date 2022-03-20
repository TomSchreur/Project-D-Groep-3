import database_manual

class Product:
    def __init__(self, id, image, name, price): #creates a Product object with given values
        self.id = id
        self.image = image
        self.name = name
        self.price = price
    
    def print_info(self): #prints all values of Product (mainly for testing)
        print(f"{self.id} {self.image} {self.name} {self.price}")

def db_to_Products(): #turns the result of a select query to the db into Product objects
    rows = database_manual.selectfromtable()
    for row in rows:
        Product(*row).print_info()

db_to_Products()
        