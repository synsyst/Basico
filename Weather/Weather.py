import requests
import streamlit as st
from datetime import datetime, timezone, timedelta

# description of weather api http://www.7timer.info/doc.php

#### functions ####
def get_ip():
    url = "https://api.aruljohn.com/ip"
    response = requests.get(url)
    ip_address = response.text.strip()
    return ip_address

def get_lat_lon(ip_address):
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)
    data = response.json()
    
    if data["status"] == "success":
        lat = data["lat"]
        lon = data["lon"]
        return lat, lon
    else:
        return None, None

def get_weather_data(lat, lon):
    url = f"http://www.7timer.info/bin/api.pl?lon={lon}&lat={lat}&product=civil&output=json"
    response = requests.get(url)
    weather_data = response.json()
    init_time_str = weather_data["init"]
    init_datetime = datetime.strptime(init_time_str, "%Y%m%d%H").replace(tzinfo=timezone.utc) #this may already be UTC format as default, it seems to get warped to 12.00 when it should stay 06.00 even when we force it to be tzaware
    st.write(f"current init_datetime aware is {init_datetime}")
    return weather_data, init_datetime

def calculate_time_difference(init_datetime):
    #now = datetime.now().replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    st.write(f"current timezone aware is {now}")
    time_difference = now - init_datetime
    time_difference_hours = time_difference.total_seconds() // 3600
    st.write(f"difference is {time_difference_hours}")
    return time_difference_hours

def get_matching_weather_data(weather_data, time_difference_hours):
    timepoint_mod_3 = time_difference_hours-(time_difference_hours % 3) # give better name to variable after updating formula
    for data_point in weather_data['dataseries']:
        if data_point['timepoint'] == timepoint_mod_3:
            # Extract relevant data into a tuple
            return (
                data_point['timepoint'],
                data_point['cloudcover'],
                data_point['lifted_index'],
                data_point['prec_type'],
                data_point['prec_amount'],
                data_point['temp2m'],
                data_point['rh2m'],
                data_point['wind10m']['direction'],
                data_point['wind10m']['speed'],
                data_point['weather']
            )
    return None

def calculate_weather_time(init_datetime, timepoint):
    weather_time_now = init_datetime + timedelta(hours=timepoint)
    return weather_time_now

#### script ####

ip_address = get_ip()
latitude, longitude = get_lat_lon(ip_address)
weather_data, init_datetime = get_weather_data(latitude, longitude)
time_difference_hours = calculate_time_difference(init_datetime)
Weather_Data_Final = get_matching_weather_data(weather_data, time_difference_hours)

if Weather_Data_Final==None:
    st.write("No matching time was found, this is most likely a bug!")
    CurrentTimeForWeather = "None"
else:
    CurrentTimeForWeather = calculate_weather_time(init_datetime, Weather_Data_Final[0])

st.title("Weather application")
st.write(f"Your IP address is: {ip_address}")
st.write(f"The weather data is shown for roughly {CurrentTimeForWeather} in UTC")
st.write(f"*Weather data<br>Cloudcover = {Weather_Data_Final[1]}<br>Lifted Index = {Weather_Data_Final[2]}<br>Prec Type = {Weather_Data_Final[3]}<br>Prec Amount = {Weather_Data_Final[4]}<br>Temp2m = {Weather_Data_Final[5]}<br>rh2m = {Weather_Data_Final[6]}<br>wind direction = {Weather_Data_Final[7]}<br>wind speed = {Weather_Data_Final[8]}<br>General Weather Conditions are {Weather_Data_Final[9]}")

#debugging data
st.write(f"debugging: {latitude}, {longitude}, {init_datetime}, {time_difference_hours}, {CurrentTimeForWeather}")




