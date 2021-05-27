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
model = pickle.load(
    open(r'C:\Users\swaraj\Desktop\codes\rent-esti\finalized_model.pkl', 'rb'))

g_keys = googlemaps.Client(key='AIzaSyDB4cH3TcqXvyp2zIjhzJD3OcJmZlr0mOg')


@app.route('/', methods=['GET'])
def home():
    return render_template('boot-strp.html')


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
        prediction = model.predict(df)*0.85
        
        print(prediction)
        # [area,lat,longi,d,bhk,bathrooms]
        low = prediction-prediction/10
        high = prediction+prediction/10
        low1 = int(low[0]//100)
        high1 = int(high[0]//100)
        range = 'The lower range : {} \n higher range : {}'.format(
            low1*100, high1*100)
        details = "the co-ordinates latitude {} and longitude {}".format(
            lat[0], longi[0])
        prediction = prediction//100
        return render_template('boot-strp.html', prediction_text=r"The estimated rent : {} thousand  ".format(int(prediction[0]*100)), details=details, range=range)


if __name__ == '__main__':
    app.run(debug=True)
