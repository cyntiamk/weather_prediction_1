import os
import pandas as pd 
import numpy as np
from datetime import datetime
from functools import reduce
import time
import csv

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
import json
import requests

import pickle
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score, mean_squared_error

# Dependencies
import openweathermapy as ow

# import api_key from config file
from config import api_key

# functions to create new feataures
def new_features(df, feature, N): 
    # total number of rows
    rows = df.shape[0]
    # a list representing number of days for prior measurements of feature
    # notice that the front of the list needs to be padded with N
    # None values to maintain the constistent rows length for each N
    numb_days_prior_measurements = [None]*N + [df[feature][i-N] for i in range(N, rows)]
    # make a new column name of feature_N and add to DataFrame
    col_name = "{}_{}".format(feature, N)
    df[col_name] = numb_days_prior_measurements

def create_recent_features(csv_path, city_initial, city_name):
    city = pd.read_csv(csv_path)
    city_date = []

    for day in city['Date']:
        timestamp = datetime.strptime(day,'%Y-%m-%d %H:%M:%S')
        day_only = datetime.strftime(timestamp,'%Y-%m-%d')
        city_date.append(day_only)
    date = pd.DataFrame(city_date)

    city['Date'] = date.values
    
    del city['Unnamed: 0']
    
    grouped_city = city.groupby('Date')
    city_mean = grouped_city[['Mean_temp','Mean_dwp']].mean()
    city_max = grouped_city[['Max_temp','Max_dwp']].max()
    city_min= grouped_city[['Min_temp','Min_dwp']].min()

    dfs = [city_mean, city_max, city_min]

    df_final = reduce(lambda left,right: pd.merge(left,right,on='Date'), dfs)
    city_organized = df_final[['Mean_temp','Max_temp','Min_temp','Mean_dwp','Max_dwp','Min_dwp']]
    city_renamed = city_organized.rename(columns={'Mean_temp': 'Avg_temp','Max_temp': 'Temp_max','Min_temp':'Temp_min',
                                           'Mean_dwp': 'Avg_dwp','Max_dwp': 'Max_dwp','Min_dwp': 'Min_dwp'})
    features_city = list(city_renamed.columns.values)
    #N is the number of days prior to the prediction, 3 days for this model
    for feature in features_city:  
        if feature != 'Date':
            for N in range(1, 4):
                new_features(city_renamed, feature, N)
    city_renamed.to_csv(city_name +'_recent_features.csv')

def run_feat():
	manly_path = 'recent_weather/manly_recent.csv'
	man_initial = 'Man'
	man_name = "Manly"
	create_recent_features(manly_path, man_initial, man_name)

	nice_path = 'recent_weather/nice_recent.csv'
	nic_initial = 'Nice'
	nic_name = "Nice"
	create_recent_features(nice_path, nic_initial, nic_name)

	kauai_path = 'recent_weather/kauai_recent.csv'
	kauai_initial = 'Kau'
	kauai_name = "Lihue"
	create_recent_features(kauai_path, kauai_initial, kauai_name)

	sal_path = 'recent_weather/salvador_recent.csv'
	sal_initial = 'Sal'
	sal_name = "Salvador"
	create_recent_features(sal_path, sal_initial, sal_name)

	kyo_path = 'recent_weather/kyoto_recent.csv'
	kyo_initial = 'Kyo'
	kyo_name = "Kyoto"
	create_recent_features(kyo_path, kyo_initial, kyo_name)

	ams_path = 'recent_weather/amsterdam_recent.csv'
	ams_initial = 'Ams'
	ams_name = "Amsterdam"
	create_recent_features(ams_path, ams_initial, ams_name)

	#irv_path = '../recent_weather/irvine_recent.csv'
	#irv_initial = 'Irv'
	#irv_name = "Irvine"
	#create_recent_features(irv_path, irv_initial, irv_name)  

def c_to_f(c):
    return ((c*9/5) + 32).round(1)

run_feat()   

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/weather', methods=['GET', 'POST'])
def query_owm():

	city = request.args.get('selected_city')

	data = []
	url = "http://api.openweathermap.org/data/2.5/weather?"
	units = "imperial"
	query_url = url + "appid=" + api_key + "&q=" + city +"&units="+ units

	weather_response = requests.get(query_url)
	data.append(weather_response.json())
	for measure in data:
	    current_dict = {
	        "City": (measure['name']),
	        "Description": (measure['weather'][0]['main']),
	        "Temperature": (measure['main']['temp']),
	        "Humidity": (measure['main']['humidity']),
	        "Wind_speed": (measure['wind']['speed'])
	    }
	
	current_df = pd.DataFrame(current_dict, index=[0])
	
	return current_df.to_json(orient='records')


@app.route('/prediction', methods=['GET','POST'])
def predicting_temp():

	city = request.args.get('selected_city')

	city_df = pd.read_csv(city +'_recent_features.csv').set_index('Date')
	sorted_city = city_df.sort_values('Date', ascending=False)
	clean_df = sorted_city.dropna()
	predictors = ['Avg_temp_1', 'Avg_temp_2', 'Avg_temp_3', 
	              'Temp_max_1', 'Temp_max_2', 'Temp_max_3',
	              'Temp_min_1','Temp_min_2', 'Temp_min_3', 
	              'Avg_dwp_1', 'Avg_dwp_2', 'Avg_dwp_3',
	              'Max_dwp_1',  'Max_dwp_2', 'Max_dwp_3',
	              'Min_dwp_1','Min_dwp_2','Min_dwp_3']

	X = clean_df[predictors]
	# import ridge model to predict temperature with recent features created
	model = pickle.load(open('ridge_temp_model.pkl', 'rb'))
	temp_c = model.predict(X)

	# apply function to convert temperature into Fahrenheit
	actual_f = c_to_f(clean_df['Avg_temp'])

	temp_f = c_to_f(temp_c)
	fahrenheit = []
	for i in range(0, len(temp_f)):
	    fahrenheit.append(int(temp_f.item(i)))
	# grab values and add to dataframe  
	clean_df['Actual_avg_temp'] = ''
	clean_df['Predicted_temp_next_day']= ''
	clean_df['Actual_avg_temp'] = actual_f
	clean_df['Predicted_temp_next_day'] = fahrenheit
	# Create new dataframe with only Average temperature collected and compare with predicted temperature 
	predictions_df = clean_df[['Actual_avg_temp','Predicted_temp_next_day']]
	# save prediction dataframe into csv
	predictions_df.to_csv(city + '_prediction.csv')
	return predictions_df[:1].to_json(orient='records')

if __name__ == "__main__":
	app.run(debug=True)
