class Product:
    def __init__(self, id, name, image_path, price, category_id, tts_path, description, discount): #creates a Product object with given values
        self.id = id
        self.name = name
        self.image_path = image_path
        self.price = price
        self.category_id = category_id
        self.tts_path = tts_path
        self.description = description
        self.discount = discount

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