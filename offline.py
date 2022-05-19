from PIL import Image
from feature_extractor import DbFeatures, parseJson
from database_manual import selectallFromTable, getCategoriesJSON, getProductsJSON
from time import perf_counter
from pathlib import Path
import numpy as np
import threading
import shutil
import os
import json

if __name__ == '__main__':
    featureClass = DbFeatures()
    featureThreads = list()
    try:
        shutil.rmtree('static/imageStorageTemp')
    except:
        print("directory was already removed, continuing w execution")
    try:
        os.mkdir('static/imageStorageTemp')
    except:
        print("directory was already created, continuing w execution")
    
    parseJson()

    start_time = perf_counter()
    for i in range(5):
        x = threading.Thread(target=featureClass.getFeature, args=(i,))
        featureThreads.append(x)
        x.start()
    for y in featureThreads:
        y.join()
    end_time = perf_counter()
    print("Total time: ", end_time - start_time)
    featureClass.features = np.array(featureClass.features)

    with open('static/featureStorage.npy', 'wb+') as fs:
        np.save(fs, featureClass.features)
    
    shutil.rmtree('static/imageStorageTemp')

