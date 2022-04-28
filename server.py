import numpy as np
import os
import threading
from PIL import Image
import shutil
from feature_extractor import FeatureExtractor, DbFeatures
from datetime import datetime
from flask import Flask, request, render_template, url_for, session
from pathlib import Path
from database_manual import selectProducts, selectallFromTable
from time import perf_counter
from DbClasses import getPrice
from TextToSpeech import createTempProductMp3
app = Flask(__name__)

#session data encryptionkey
app.secret_key = "hello"

# Read image features
fe = FeatureExtractor()

# grab features from static/featureStorage.npy
with open('static/featureStorage.npy', 'rb') as fs:
    features = np.load(fs)

# get products from DB
Products = selectallFromTable("Products")

@app.route('/', methods=['GET', 'POST',])
def index():
    ttspressed=False
    if request.method == 'POST':
        # removes directory 'static/uploaded' & file contained inside
        # uploaded contains the last-uploaded image by user
        shutil.rmtree('static/uploaded')
        os.mkdir('static/uploaded')
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

        for id in ids:
            if((Products[id].name)+".mp3" in "./static/mp3files"):
                print('Mp3 already exists')
            else:
                createTempProductMp3(Products[id].description, Products[id].name)

        # establish scores to pass to HTML
        scores = [(dists[id], Products[id].image_path, Products[id].name, getPrice(Products[id].price, Products[id].discount), Products[id].tts_path) for id in ids]

        return render_template('index.html',
                               query_path=uploaded_img_path,
                               scores=scores) 

    else:
        return render_template('index.html')

@app.route('/text-to-speech/', methods=['GET', 'POST'])
def TTS():
    ttspressed = True
    if request.method == 'POST':
        # removes directory 'static/uploaded' & file contained inside
        # uploaded contains the last-uploaded image by user
        shutil.rmtree('static/uploaded')
        os.mkdir('static/uploaded')
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

        for id in ids:
            if((Products[id].name)+".mp3" in "./static/mp3files"):
                print('Mp3 already exists')
            else:
                createTempProductMp3(Products[id].description, Products[id].name)

        # establish scores to pass to HTML
        scores = [(dists[id], Products[id].image_path, Products[id].name, getPrice(Products[id].price, Products[id].discount), Products[id].tts_path) for id in ids]

        return render_template('index.html',
                               query_path=uploaded_img_path,
                               scores=scores) 

    else:
        return render_template('index.html')

@app.route('/more/', methods=['GET', 'POST'])
def more():
    uploaded_img_path = ""
    if "scores" in session:
        scores = session["scores"]

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
        shutil.rmtree('static/uploaded')
        os.mkdir('static/uploaded')
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
        session["scores"] = scores

        for id in ids:
            if((Products[id].name)+".mp3" in "./static/mp3files"):
                print('Mp3 already exists')
            else:
                createTempProductMp3(Products[id].description, Products[id].name)

        # establish scores to pass to HTML
        scores = [(dists[id], Products[id].image_path, Products[id].name, getPrice(Products[id].price, Products[id].discount), Products[id].tts_path) for id in ids]

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

        return render_template('highContrastIndex.html',
                               query_path=uploaded_img_path,
                               scores=scores)
    else:
        return render_template('highContrastIndex.html')  

if __name__=="__main__":
    app.run("0.0.0.0")
