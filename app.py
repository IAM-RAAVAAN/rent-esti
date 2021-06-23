from flask import Flask, render_template, request
import requests
import googlemaps
import sklearn
import pickle
import numpy as np
import pandas as pd

from geopy.distance import geodesic

app = Flask(__name__)
filename = 'newmodel.pkl'


model= pickle.load(open(filename,'rb'))
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
        value_add = int(request.form['Fuel_Type_Petrol'])

        geo_cod = g_keys.geocode(locality)
        lat = [geo_cod[0]['geometry']['location']['lat']]
        longi = [geo_cod[0]['geometry']['location']['lng']]
        latlong = zip(lat, longi)
        pune = (18.531442, 73.844562)
        d = geodesic(latlong, pune).km
        area = int(area)
        dic = [bhk]
        df = pd.DataFrame(dic)
        # df['bhk'] = bhk
        df['bath_clean'] = bathrooms
        df['lat'] = lat
        df['longi'] = longi
        df['distance_geo_py'] = d
        print(df)
        prediction1 = model.predict(df)*0.85
        # [area,lat,longi,d,bhk,bathrooms]
        prediction = prediction1*area
        x = prediction+value_add
        prediction= (x[0]//100)*100
        low = prediction-prediction/10
        low=(low//100)*100
        high = prediction+prediction/10
        high = (high//100)*100
        lower = 'lowest {} '.format(
            low)
        higher='higher {}'.format(high)
        details = " lat {} ".format(
            lat[0])
        longi = " longi {}".format(
             longi[0])
        rate = "the are {}".format(prediction1)
        y=(prediction//100)*100
        area='rate in this area is {}'.format(prediction1[0])

        return render_template('rent prediction.html', prediction_text=r"The estimated rent of the property is  {} ".format(x[0]), details=details, lower=lower, higher=higher, longi=longi, rate=area)


if __name__ == '__main__':
    app.run(debug=True)
