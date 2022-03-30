class Product:
    def __init__(self, id, name, image_path, df_path, price, category): #creates a Product object with given values
        self.id = id
        self.name = name
        self.image_path = image_path
        self.df_path = df_path
        self.price = price
        self.category = category
    
    def getPrice(self):
        pstr = str(self.price)
        cents = False
        eurostr = ""
        centstr = ""
        for i in range(len(pstr)):
            if cents:
                centstr += pstr[i]
            elif pstr[i] == ".":
                eurostr += ","
                cents = True
            else:
                eurostr += pstr[i]
        if len(centstr) != 2:
            if centstr == "0":
                centstr = "-"
            else:
                centstr += "0"
        return eurostr + centstr
