import numpy as np
import os
from PIL import Image
from feature_extractor import FeatureExtractor
from datetime import datetime
from flask import Flask, request, render_template, url_for, session
from pathlib import Path
from database_manual import selectProducts, selectallProducts
app = Flask(__name__)

#session data encryptionkey
app.secret_key = "hello"

# Read image features
fe = FeatureExtractor()
features = []

global item_amount
global img2
global uploaded_img_path

Products = selectallProducts()
#gets all necessary data from db
for product in Products:
    features.append(np.load(product.df_path))
features = np.array(features)


@app.route('/', methods=['GET', 'POST',])
def index():
    item_amount = 30
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
        scores = [(dists[id], Products[id].image_path, Products[id].name, Products[id].getPrice(), Products[id].tts_path) for id in ids]
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
        scores = [(dists[id], Products[id].image_path) for id in ids]

        return render_template('highcontrastIndex.html',
                               query_path=uploaded_img_path,
                               scores=scores)
    else:
        return render_template('highContrastIndex.html') 



if __name__=="__main__":
    app.run("0.0.0.0")
