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

def grab_json(city_name, city_csv_name):   
    data = []

    url = "http://api.openweathermap.org/data/2.5/weather?"
    units = "metric"
    city = url + "appid=" + api_key + "&q=" + city_name +"&units="+ units

    weather_response = requests.get(city)
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

    city_weather = {
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

    df = pd.DataFrame(city_weather)

    # if file does not exist write header 
    if not os.path.isfile(city_csv_name + '.csv'):
       df.to_csv(city_csv_name + '.csv', header='column_names')
    else: # else it exists so append without writing the header
       df.to_csv(city_csv_name + '.csv' , mode='a', header=False)

def run_all_json():
    ams_name = 'Amsterdam'
    ams_csv_name = 'amsterdam_recent'
    grab_json(ams_name, ams_csv_name)
    
    kyo_name = 'Kyoto'
    kyo_csv_name = 'kyoto_recent'
    grab_json(kyo_name, kyo_csv_name)
    
    nic_name = 'Nice'
    nic_csv_name = 'nice_recent'
    grab_json(nic_name, nic_csv_name)
    
    kau_name = 'Lihue'
    kau_csv_name = 'kauai_recent'
    grab_json(kau_name, kau_csv_name)
    
    sal_name = 'Salvador'
    sal_csv_name = 'salvador_recent'
    grab_json(sal_name, sal_csv_name)
    
    man_name = 'Manly'
    man_csv_name = 'manly_recent'
    grab_json(man_name, man_csv_name)

    irv_name = 'Irvine'
    irv_csv_name = 'irvine_recent'
    grab_json(irv_name, irv_csv_name)

while(True):
    run_all_json()
    time.sleep(3600)