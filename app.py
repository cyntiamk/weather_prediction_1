import os
import pandas as pd 

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
import json
import requests
# Dependencies
import openweathermapy as ow

# import api_key from config file
from config import api_key

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/weather', methods=['GET', 'POST'])
def query_owm():

	selected_city = request.args.get('selected_city')

	data = []
	url = "http://api.openweathermap.org/data/2.5/weather?"
	units = "imperial"
	query_url = url + "appid=" + api_key + "&q=" + selected_city +"&units="+ units

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
	

if __name__ == "__main__":
	app.run(debug=True)