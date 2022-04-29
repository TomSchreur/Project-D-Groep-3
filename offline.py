from PIL import Image
from feature_extractor import DbFeatures
from database_manual import selectallFromTable
from time import perf_counter
from pathlib import Path
import numpy as np
import threading

if __name__ == '__main__':
    featureClass = DbFeatures()
    featureThreads = list()

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