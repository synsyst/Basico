import requests
import streamlit as st
from datetime import datetime, timezone, timedelta
import pytz

# description of weather api http://www.7timer.info/doc.php

#### functions ####
def get_ip(): # the ip is from the streamlit server and doesn't work for the user - think of something else, perhaps go back to the idea of the address instead.
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
    #st.write(f"current init_datetime aware is {init_datetime}")
    return weather_data, init_datetime

def calculate_time_difference(init_datetime):
    now = datetime.now(timezone.utc)
    #st.write(f"current timezone aware is {now}")
    time_difference = now - init_datetime
    time_difference_hours = time_difference.total_seconds() // 3600
    #st.write(f"difference is {time_difference_hours}")
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

#convert utc time to Danish time
def convert_to_copenhagen_time(utc_time):
    copenhagen_tz = pytz.timezone('Europe/Copenhagen')
    copenhagenTime = utc_time.astimezone(copenhagen_tz)
    formatted_time = copenhagenTime.strftime('%Y-%m-%d %H:%M')
    return formatted_time

#### weather mappings ####
cloud_cover_mapping = {
    1: "0%-6%",
    2: "6%-19%",
    3: "19%-31%",
    4: "31%-44%",
    5: "44%-56%",
    6: "56%-69%",
    7: "69%-81%",
    8: "81%-94%",
    9: "94%-100%"
}

wind_speed_mapping = {
    1: "Below 0.3m/s (calm)",
    2: "0.3-3.4m/s (light)",
    3: "3.4-8.0m/s (moderate)",
    4: "8.0-10.8m/s (fresh)",
    5: "10.8-17.2m/s (strong)",
    6: "17.2-24.5m/s (gale)",
    7: "24.5-32.6m/s (storm)",
    8: "Over 32.6m/s (hurricane)"
}

precipitation_amount_mapping = {
    0: "None",
    1: "0-0.25mm/hr",
    2: "0.25-1mm/hr",
    3: "1-4mm/hr",
    4: "4-10mm/hr",
    5: "10-16mm/hr",
    6: "16-30mm/hr",
    7: "30-50mm/hr",
    8: "50-75mm/hr",
    9: "Over 75mm/hr"
}

weather_type_mapping = {
    "clearday": "Total cloud cover less than 20%",
    "clearnight": "Total cloud cover less than 20%",
    "pcloudyday": "Total cloud cover between 20%-60%",
    "pcloudynight": "Total cloud cover between 20%-60%",
    "mcloudyday": "Total cloud cover between 60%-80%",
    "mcloudynight": "Total cloud cover between 60%-80%",
    "cloudyday": "Total cloud cover over 80%",
    "cloudynight": "Total cloud cover over 80%",
    "humidday": "Relative humidity over 90% with total cloud cover less than 60%",
    "humidnight": "Relative humidity over 90% with total cloud cover less than 60%",
    "lightrainday": "Precipitation rate less than 4mm/hr with total cloud cover more than 80%",
    "lightrainnight": "Precipitation rate less than 4mm/hr with total cloud cover more than 80%",
    "oshowerday": "Precipitation rate less than 4mm/hr with total cloud cover between 60%-80%",
    "oshowernight": "Precipitation rate less than 4mm/hr with total cloud cover between 60%-80%",
    "ishowerday": "Precipitation rate less than 4mm/hr with total cloud cover less than 60%",
    "ishowernight": "Precipitation rate less than 4mm/hr with total cloud cover less than 60%",
    "lightsnowday": "Precipitation rate less than 4mm/hr",
    "lightsnownight": "Precipitation rate less than 4mm/hr",
    "rainday": "Precipitation rate over 4mm/hr",
    "rainnight": "Precipitation rate over 4mm/hr",
    "snowday": "Precipitation rate over 4mm/hr",
    "snownight": "Precipitation rate over 4mm/hr",
    "rainsnowday": "Precipitation type to be ice pellets or freezing rain",
    "rainsnownight": "Precipitation type to be ice pellets or freezing rain"
}

#### script ####

ip_address = get_ip()
latitude, longitude = get_lat_lon(ip_address)
weather_data, init_datetime = get_weather_data("55.724026551241174", "12.580133211143076") #55.724026551241174, 12.580133211143076 for basico office
time_difference_hours = calculate_time_difference(init_datetime)
Weather_Data_Final = get_matching_weather_data(weather_data, time_difference_hours)

if Weather_Data_Final==None:
    st.write("No matching time was found, this is most likely a bug!")
    CurrentTimeForWeather = "None"
else:
    CurrentTimeForWeather = calculate_weather_time(init_datetime, Weather_Data_Final[0])

CopenhagenWeatherTime = convert_to_copenhagen_time(CurrentTimeForWeather)

st.title("Weather application")
st.write(f"Your IP address is: {ip_address}, or would be if Streamlit servers didn't overwrite visitor IP, so this IP is instead the streamlit server :), we map the weather function to location of Basico offices instead")
st.write(f"Time of forecast is {CopenhagenWeatherTime}")
st.write(f"Weather data<br>Cloudcover = {cloud_cover_mapping.get(Weather_Data_Final[1])}<br>Precipitation Type = {Weather_Data_Final[3]}<br>Precipitation Amount = {precipitation_amount_mapping.get(Weather_Data_Final[4])}<br>Temperature = {Weather_Data_Final[5]} Celcius<br>Relative Humidity = {Weather_Data_Final[6]}<br>Wind Direction = {Weather_Data_Final[7]}<br>Wind Speed = {wind_speed_mapping.get(Weather_Data_Final[8])}<br>General Weather Conditions = {weather_type_mapping.get(Weather_Data_Final[9])}", unsafe_allow_html=True)

#debugging data
#st.write(f"debugging: {latitude}, {longitude}, {init_datetime}, {time_difference_hours}, {CurrentTimeForWeather}")




