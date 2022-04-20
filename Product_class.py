class Product:
    def __init__(self, id, name, image_path, df_path, price, category, tts_path): #creates a Product object with given values
        self.id = id
        self.name = name
        self.image_path = image_path
        self.df_path = df_path
        self.price = price
        self.category = category
        self.tts_path = tts_path
    
    def getPrice(self):
        pstr = str(self.price)
        cents = False
        eurostr = ""
        centstr = ""
        for i in range(len(pstr)):
            if cents and len(centstr) < 3:
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
