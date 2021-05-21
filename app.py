from flask import Flask, render_template, request
import requests
import googlemaps
import sklearn
import pickle
import numpy as np
import pandas as pd
import os

from geopy.distance import geodesic

app = Flask(__name__)
path = os.getcwd()
model = pickle.load(open('finalized_model.pkl', 'rb'))

g_keys = googlemaps.Client(key='AIzaSyDB4cH3TcqXvyp2zIjhzJD3OcJmZlr0mOg')


@app.route('/', methods=['GET'])
def home():
    return render_template('rent prediction.html')


@app.route('/prediction', methods=['POST'])
def predict():
    if request.method == 'POST':
        area = request.form['area']
        bhk = int(request.form['bhk'])
        bathrooms = int(request.form['bathrooms'])
        locality = str(request.form['locality'])

        geo_cod = g_keys.geocode(locality)
        lat = [geo_cod[0]['geometry']['location']['lat']]
        longi = [geo_cod[0]['geometry']['location']['lng']]
        latlong = zip(lat, longi)
        pune = (18.531442, 73.844562)
        d = geodesic(latlong, pune).km
        area = int(area)
        dic = {
            'area': area,
            'lati': lat
        }
        df = pd.DataFrame.from_dict(dic)

        df['longi'] = longi
        df['dis'] = d
        df['bhk'] = bhk
        df['bath'] = bathrooms
        prediction = model.predict(df)
        # [area,lat,longi,d,bhk,bathrooms]
        low = prediction-prediction/10
        high = prediction+prediction/10
        range = 'The rang of the property is from {} to {}'.format(
            low[0], high[0])
        details = "the co-ordinates latitude {} and longitude {}".format(
            lat[0], longi[0])
        return render_template('rent prediction.html', prediction_text=r"The estimated rent of the property is {}   ".format(prediction[0]), details=details, range=range)


if __name__ == '__main__':
    app.run(debug=True)
