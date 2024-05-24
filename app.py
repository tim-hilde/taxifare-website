import streamlit as st
import datetime
import requests
import pandas as pd

'''
# TaxiFare
'''

'''
#### Please information about your future fare
'''

date = st.date_input(
    "Select the date",
    datetime.date.today()
)

time = st.time_input("Select the time of pickup",
            datetime.datetime.now())

pickup_lon = st.number_input("Fill in pickup longitude", min_value=-90.0, max_value=90.0, value=-73.950655)
pickup_lat = st.number_input("Fill in pickup latitude", min_value=-90.0, max_value=90.0, value= 40.783282)
dropoff_lon = st.number_input("Fill in dropoff longitude", min_value=-90.0, max_value=90.0, value= -73.984365)
dropoff_lat = st.number_input("Fill in dropoff latitude", min_value=-90.0, max_value=90.0, value= 40.769802)
passenger_count = st.number_input("Fill in passenger count", min_value=1, max_value=100, value= 1)

st.map(
    pd.DataFrame(
        {
            "lat": [pickup_lat, dropoff_lat],
            "lon": [pickup_lon, dropoff_lon]
        }
    )
)

url = 'https://taxifare.lewagon.ai/predict'

params = {
    "pickup_datetime": f"{date} {time}",
    "pickup_longitude": pickup_lon,
    "pickup_latitude": pickup_lat,
    "dropoff_longitude": dropoff_lon,
    "dropoff_latitude": dropoff_lat,
    "passenger_count": passenger_count
}

if st.button("Calculate fare"):
    request = requests.get(url, params=params)
    fare = f"{round(request.json()['fare'], 2)} $"
    col, col0 = st.columns(2)
    col.metric("Your fare is", fare)
