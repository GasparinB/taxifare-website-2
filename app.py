import streamlit as st
import requests
import pandas as pd
import numpy as np
import os
'''
# 🚕/TaxiFareModel\🚕
'''
st.subheader('A machine learning algorithm that can predict taxi fares in NYC')
'''
## ------------------------------
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:
'''
st.checkbox('date and time')
st.checkbox('pickup lon and lat')
st.checkbox('dropoff lon and lat')

columns = st.columns(5)
pickup_date = columns[0].date_input(label='Pick Up Day')
pickup_time = columns[1].time_input('Time for your cab🚕')
origin_city = columns[2].text_input('Start Point')
destiny_city = columns[3].text_input('Destiny Point')
num_people = columns[4].number_input('Pasanger count',min_value=1,max_value=5,step=1)
url_origin = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{origin_city}.json'

PK_ACCESS_TOKEN = st.secrets['PK_ACCESS_TOKEN']
response_origin =requests.get(url_origin,params={'access_token':PK_ACCESS_TOKEN})
def get_coordinates(response,PK_ACC):
    if response.status_code == 200:
        data = response.json()
        features = data["features"]
        if features:
            coordinates = features[0]["center"]
            return coordinates
        else:
            st.write("No results found for the given city.")
            return None
    else:
        st.error('An error ocurred while trying to locate the city')

def get_taxifare(url,params):
    response = requests.get(url,params=params)
    if response.status_code == 200:
        pass
    else:
        st.write("Error occured")
url_destiny = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{destiny_city}.json'
response_destiny =requests.get(url_destiny,params={'access_token':PK_ACCESS_TOKEN})

if st.button('Sumbit'):
    st.write('sumbiting information----')
    st.write(f'{str(pickup_date)+" "+str(pickup_time)}')
    origin= get_coordinates(response_origin,PK_ACCESS_TOKEN)
    destiny = get_coordinates(response_destiny,PK_ACCESS_TOKEN)
    st.write(origin,destiny)
    params={
        'pickup_datetime':f'{str(pickup_date)+" "+str(pickup_time)}',
        'pickup_longitude':origin[0],
        'pickup_latitude':origin[1],
        'dropoff_longitude':destiny[0],
        'dropoff_latitude':destiny[1],
        'passenger_count':num_people
    }
    url = 'https://taxifare.lewagon.ai/predict'
    final_response = requests.get(url,params=params)
    if final_response.status_code == 200:
        final_response = final_response.json()
else:
    st.write('Click the button to sumbit the information')
    final_response={'fare':None}
'''
## Finally, we can display the prediction to the user
'''
f'''
Fare amount: ${final_response['fare']}
'''
