import random
class Product:
    def __init__(self, id, name, image_path, price, category_id, product_page, description, discount): #creates a Product object with given values
        self.id = id
        self.name = name
        self.image_path = image_path
        self.price = price
        self.category_id = category_id
        self.product_page = product_page
        self.description = description
        if discount == None:
            maxDiscount = 0.6
            self.discount = round(random.random(), 2)
            while self.discount > maxDiscount:
                self.discount = round(random.random(), 2) # can be anything above 0.0; currently a random float (0.xx)
        else:
            self.discount = discount
    
    def createDescription(self, categories):
        for category in categories:
            if category.id == self.category_id:
                self.description = "The product name is: " + self.name + ". The price is € " + getPrice(self.price,self.discount) + ". The product type is: " + category.product_type + " of category " + category.category
                break

class Category:
    def __init__(self, id, product_type, category):
        self.id = id
        self.product_type = product_type
        self.category = category

def getPrice(price, discount = 0):
    newPrice = price * (1 - discount)
    pstrRounded = str(round(newPrice, 2))
    pstr = str(newPrice)
    cents = False
    decimalCount = 0
    result = ""
    for i in range(len(pstrRounded)):
        if cents and pstrRounded[i] != ".":
            result += pstrRounded[i]
            decimalCount = decimalCount + 1
        elif pstrRounded[i] == ".":
            result += ","
            cents = True
        elif not cents:
            result += pstrRounded[i]
        else:
            break
    if decimalCount == 1:
        result += "0"
    cents = result[-2:]
    if cents == "00":
        result = result.replace(cents, "-", 1)
    return result