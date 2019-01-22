# Dependencies
import openweathermapy as ow
import pandas as pd
import requests
# import api_key from config file
from config import api_key

def query_owm(selected_city):
	data = []
	url = "http://api.openweathermap.org/data/2.5/weather?"
	units = "imperial"
	query_url = url + "appid=" + api_key + "&q=" + selected_city +"&units="+ units

	weather_response = requests.get(query_url)
	data.append(weather_response.json())

	current_dict = {
	    "City": (measure['name']),
	    "Description": (measure['weather'][0]['main']),
	    "Temperature(F)": (measure['main']['temp']),
	    "Humidity(%)": (measure['main']['humidity']),
	    "Wind_speed(m/s)": (measure['wind']['speed'])
	}
	return current_dict