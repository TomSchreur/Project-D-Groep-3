class Product:
    def __init__(self, id, name, image_path, df_path, price, category): #creates a Product object with given values
        self.id = id
        self.name = name
        self.image_path = image_path
        self.df_path = df_path
        self.price = price
        self.category = category