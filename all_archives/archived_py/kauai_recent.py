# Dependencies
import csv
import openweathermapy as ow
import pandas as pd
import requests
import pprint
import time
from datetime import datetime
import os

# import api_key from config file
from config import api_key

def grab_kauai():
    data = []
    url = "http://api.openweathermap.org/data/2.5/weather?"
    units = "metric"
    kauai = url + "appid=" + api_key + "&q=" + 'Lihue'+"&units="+ units

    weather_response = requests.get(kauai)
    data.append(weather_response.json())

    date_obj = []
    temp = []
    max_temp = []
    min_temp = []
    humidity = []
    pressure = []
    wind_speed = []
    clouds = []
    description = []

    for measure in data:
        date_obj.append(measure['dt'])
        temp.append(measure['main']['temp'])
        max_temp.append(measure['main']['temp_max'])
        min_temp.append(measure['main']['temp_min'])
        pressure.append(measure['main']['pressure'])
        humidity.append(measure['main']['humidity'])
        wind_speed.append(measure['wind']['speed'])
        clouds.append(measure['clouds']['all'])
        description.append(measure['weather'][0]['main'])

    def calculate_dp(T, H):
        return T - ((100 - H) / 5)

    dew_point = []
    for T ,H in zip(temp, humidity):
        dp = calculate_dp(T,H)
        dew_point.append(dp)

    max_dew = []
    for T ,H in zip(max_temp, humidity):
        dp = calculate_dp(T,H)
        max_dew.append(dp)

    min_dew = []
    for T ,H in zip(min_temp, humidity):
        dp = calculate_dp(T,H)
        min_dew.append(dp)

    date = []
    for seconds in date_obj:
        timestamp = datetime.utcfromtimestamp(seconds)
        day = datetime.strftime(timestamp,'%Y-%m-%d %H:%M:%S')
        date.append(day) 

    kauai_weather = {
        "Date": date,
        "Mean_temp": temp,
        "Max_temp": max_temp,
        "Min_temp": min_temp,
        "Mean_dwp": dew_point,
        "Max_dwp": max_dew,
        "Min_dwp": min_dew,
        "Pressure": pressure,
        "Humidity": humidity,
        "Wind": wind_speed,
        "Clouds": clouds,
        "Description": description
    }

    kauai_recent = pd.DataFrame(kauai_weather)

    # if file does not exist write header 
    if not os.path.isfile('kauai_recent.csv'):
       kauai_recent.to_csv('kauai_recent.csv', header='column_names')
    else: # else it exists so append without writing the header
       kauai_recent.to_csv('kauai_recent.csv', mode='a', header=False)

while(True):
    grab_kauai()
    time.sleep(3600)

print("Retrieving data....")
    