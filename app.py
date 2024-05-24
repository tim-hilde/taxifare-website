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

date_columns = st.columns(2)

date = date_columns[0].date_input(
    "Select the date",
    datetime.date.today()
)

time = date_columns[1].time_input("Select the time of pickup",
            datetime.datetime.now())

def get_lat_lon(adress):
    url = "https://nominatim.openstreetmap.org/search"
    params={
        "q": f"{adress} New York",
        "format": "json"
    }
    response = requests.get(url, params=params)
    print(response.content)
    try:
        content = response.json()
        lat = content[0]["lat"]
        lon = content[0]["lon"]
        return float(lat), float(lon)
    except:
        return "Error getting location"

location_columns = st.columns(2)
pickup = get_lat_lon(location_columns[0].text_input("Fill in your pickup location", "Manhattan"))
dropoff = get_lat_lon(location_columns[1].text_input("Fill in your dropoff location", "Upper West Side"))
passenger_count = st.slider("Select number of passengers", min_value=1, max_value=10, value= 1)

if isinstance(pickup, str) | isinstance(dropoff, str):
    st.code(
        '''
        Error getting location
        '''
    )
else:
    pickup_lat, pickup_lon = pickup
    dropoff_lat, dropoff_lon = dropoff

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
