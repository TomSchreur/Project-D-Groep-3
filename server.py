import numpy as np
import os
from PIL import Image
from feature_extractor import FeatureExtractor
from datetime import datetime
from flask import Flask, request, render_template
from pathlib import Path
from database_manual import selectProducts, selectallProducts
app = Flask(__name__)

# Read image features
fe = FeatureExtractor()
features = []
img_paths = []
img_names = []

#gets all necessary data from db
for product in selectallProducts():
    features.append(np.load(product.df_path))
    img_paths.append(product.image_path)
    img_names.append(product.name)
features = np.array(features)


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
        dists = np.linalg.norm(features-query, axis=1)  # L2 distances to features
        ids = np.argsort(dists)[:30]  # Top 30 results

        # get names, to search for products in db.
        temp= [(img_paths[id]) for id in ids]
        listpaths = []
        for i in temp:
            listpaths.append(os.path.basename(i))
        queryProduct = selectProducts(listpaths)
        ProductPrices = [queryProduct[i][4] for i in range(30)]

        scores = [(dists[id], img_paths[id], img_names[id]) for id in ids]
        # Add prices, to tuple
        for i in range(30):
            scores[i] = (scores[i] + (ProductPrices[i],))
        

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
        scores = [(dists[id], img_paths[id]) for id in ids]

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
