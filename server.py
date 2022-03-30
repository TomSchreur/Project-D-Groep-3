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

Products = selectallProducts()
#gets all necessary data from db
for product in Products:
    features.append(np.load(product.df_path))
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

        scores = [(dists[id], Products[id].image_path, Products[id].name, Products[id].getPrice()) for id in ids]

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
        scores = [(dists[id], Products[id].image_path) for id in ids]

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
