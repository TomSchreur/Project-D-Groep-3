from feature_extractor import DbFeatures, FeatureExtractor
from PIL import Image
from DbClasses import Product
import os
import shutil
import threading
from time import perf_counter
import numpy as np
from database_manual import *

class TestClass:
    def __init__(self, id, image_path):
        self.id = id
        self.image_path = image_path


def Extract():
    fe = FeatureExtractor()

    try:
        fe.extract(Image.open("./static/Testfolder/normalimage.png"))
        print("Feature of a correct image was succesfully created")
    except:
        print("Could not create feature from correct image")
    try:
        fe.extract("./TextToSpeech.py")
        print("Feature of an incorrect filetype was succesfully created")
    except:
        print("Could not create feature from incorrect filetype")
    try:
        fe.extract(Image.open("./static/Testfolder/largeimage.png"))
        print("Feature of a large image was succesfully created")
    except:
        print("Could not create feature from large image")
    try:
        fe.extract(Image.open("./static/Testfolder/smallimage.png"))
        print("Feature of a small image was succesfully created")
    except:
        print("Could not create feature from small image")

def GetFeature():
    try:
        shutil.rmtree('static/imageStorageTemp')
    except:
        print("directory was already removed, continuing w execution")
    try:
        os.mkdir('static/imageStorageTemp')
    except:
        print("directory was already created, continuing w execution")

    if os.path.exists("testdatabase.db"):
        os.remove("testdatabase.db")

    if trygetfeature():
        print("GetFeature() without a database was successfull")
    else:
        print("GetFeature() without a database was unsuccessfull")

    createTesttable()

    if trygetfeature():
        print("GetFeature() with an empty database was successfull")
    else:
        print("GetFeature() with an empty database was unsuccessfull")

    insertintoTetstable(["https://media.s-bol.com/q534ypoL4lG/550x715.jpg"])

    if trygetfeature():
        print("GetFeature() with a database with a valid image_path was successfull")
    else:
        print("GetFeature() with a database with a valid image_paths was unsuccessfull")

    with create_connection("testdatabase.db") as db:
        c = db.cursor()
        c.execute("""DELETE FROM Testtable;""")
        db.commit()

    insertintoTetstable(["https://www.google.com/"])

    if trygetfeature():
        print("GetFeature() with a database with an invalid image_path was successfull")
    else:
        print("GetFeature() with a database with an invalid image_paths was unsuccessfull")

    shutil.rmtree('static/imageStorageTemp')

def trygetfeature():
    try:
        featureClass = DbFeatures(selectallFromTesttable())
        for i in range(len(featureClass.products)):
            featureClass.products[i] = TestClass(*featureClass.products[i])
        featureThreads = list()
        start_time = perf_counter()
        for i in range(5):
            x = threading.Thread(target=featureClass.getFeature, args=(i,))
            featureThreads.append(x)
            x.start()
        for y in featureThreads:
            y.join()
        end_time = perf_counter()
        print("Total time:", end_time - start_time, "Seconds.")
        featureClass.features = np.array(featureClass.features)
        return True
    except:
        return False

    
if __name__ == '__main__':

    # Extract()
    GetFeature()