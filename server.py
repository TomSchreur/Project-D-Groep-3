import numpy as np
import os
import threading
from PIL import Image
from feature_extractor import FeatureExtractor, DbFeatures
from datetime import datetime
from flask import Flask, request, render_template
from pathlib import Path
from database_manual import selectProducts, selectallProducts
from time import perf_counter
app = Flask(__name__)

# Read image features
fe = FeatureExtractor()
features = DbFeatures()
featureThreads = list()

start_time = perf_counter()
for i in range(5):
    x = threading.Thread(target=features.getFeature, args=(i,))
    featureThreads.append(x)
    x.start()
for y in featureThreads:
    y.join()
features.features = np.array(features.features)
end_time = perf_counter()
print("Total time: ", end_time - start_time)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['query_img']

        noPictureSelected = 'Geen bestand geselecteerd.'

        if file.filename == '':
            return render_template('index.html', noPictureSelected=noPictureSelected)

        # Save query image
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
        img.save(uploaded_img_path)

        # Run search
        query = fe.extract(img)
        dists = np.linalg.norm(features.features-query, axis=1)  # L2 distances to features
        ids = np.argsort(dists)[:30]  # Top 30 results

        scores = [(dists[id], features.products[id].image_path, features.products[id].name, features.products[id].getPrice(), features.products[id].tts_path) for id in ids]

        # get names, to search for products in db.
        # temp= [(img_paths[id]) for id in ids]
        # listpaths = []
        # for i in temp:
        #     listpaths.append(os.path.basename(i))
        # queryProduct = selectProducts(listpaths)
        # ProductPrices = [queryProduct[i][2] for i in range(30)]
        
        # pathMp3 =[]
        # for i in listpaths:
        #     pathMp3.append(Path('./static/mp3files/'+i.replace('.png','.mp3')))

        # scores = [(dists[id], img_paths[id], os.path.basename(img_paths[id])) for id in ids]
        # # Add prices and mp3paths, to tuple
        # for i in range(30):
        #     scores[i] = (scores[i] + (ProductPrices[i],)+(pathMp3[i],))

        return render_template('index.html',
                               query_path=uploaded_img_path,
                               scores=scores)
    else:
        return render_template('index.html')

# @app.route('/highcontrast', methods=['GET', 'POST'])
# def highContrastSwitch():
#     return render_template('highContrastIndex.html');

# @app.route('/', methods=['GET', 'POST'])
# def normalContrastSwitch():
#     return render_template('index.html');

@app.route('/high-contrast/', methods=['GET', 'POST'])
def highContrastSwitch():
    if request.method == 'POST':
        file = request.files['query_img']

        noPictureSelected = 'Geen bestand geselecteerd.'

        if file.filename == '':
            return render_template('highContrastIndex.html', noPictureSelected=noPictureSelected)

        # Save query image
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
        img.save(uploaded_img_path)

        # Run search
        query = fe.extract(img)
        dists = np.linalg.norm(features-query, axis=1)  # L2 distances to features
        ids = np.argsort(dists)[:30]  # Top 30 results
        scores = [(dists[id], features.products[id].image_path) for id in ids]

        return render_template('highcontrastIndex.html',
                               query_path=uploaded_img_path,
                               scores=scores)
    else:
        return render_template('highContrastIndex.html')    

@app.route('/')
def normalContrastSwitch():
  return render_template('index.html')


if __name__=="__main__":
    app.run("0.0.0.0")
