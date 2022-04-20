class Product:
    def __init__(self, id, name, image_path, price, category, tts_path, description, discount): #creates a Product object with given values
        self.id = id
        self.name = name
        self.image_path = image_path
        self.price = price
        self.category = category
        self.tts_path = tts_path
        self.description = description
        self.discount = discount
    
    def getPrice(self):
        newPrice = self.price * (1 - self.discount)
        pstr = str(newPrice)
        cents = False
        eurostr = ""
        centstr = ""
        for i in range(len(pstr)):
            if cents and len(centstr) < 2:
                centstr += pstr[i]
            elif pstr[i] == ".":
                eurostr += ","
                cents = True
            elif not cents:
                eurostr += pstr[i]
            else:
                continue
        if len(centstr) != 2:
            centstr += "0"
        if centstr == "00":
            centstr = "-"
        return eurostr + centstr
