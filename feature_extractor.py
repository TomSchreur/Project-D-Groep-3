from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
import numpy as np
from database_manual import selectProducts, selectallFromTable
import threading
from PIL import Image

# See https://keras.io/api/applications/ for details

class FeatureExtractor:
    def __init__(self):
        base_model = VGG16(weights='imagenet')
        self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

    def extract(self, img):
        """
        Extract a deep feature from an input image
        Args:
            img: from PIL.Image.open(path) or tensorflow.keras.preprocessing.image.load_img(path)

        Returns:
            feature (np.ndarray): deep feature with the shape=(4096, )
        """
        img = img.resize((224, 224))  # VGG must take a 224x224 img as an input
        img = img.convert('RGB')  # Make sure img is color
        x = image.img_to_array(img)  # To np.array. Height x Width x Channel. dtype=float32
        x = np.expand_dims(x, axis=0)  # (H, W, C)->(1, H, W, C), where the first elem is the number of img
        x = preprocess_input(x)  # Subtracting avg values for each pixel
        feature = self.model.predict(x)[0]  # (1, 4096) -> (4096, )
        return feature / np.linalg.norm(feature)  # Normalize

class DbFeatures:
    def __init__(self):
        self.products = selectallFromTable("Products")
        self.lock = threading.Lock()
        self.features = []
        self.fe = FeatureExtractor()
        self.productCount = 0
    
    def getFeature(self, threadId):
        with self.lock:
            while self.productCount < len(self.products):
                #with self.lock:
                product = self.products[self.productCount]
                self.productCount = self.productCount + 1
                feature = self.fe.extract(img = Image.open(product.image_path))
                #with self.lock:
                self.features.append(feature)
                print("loading: ", product.id, " using thread no. ", threadId)