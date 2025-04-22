import pandas as pd
import requests


def create_api_param(series_id, start_date, end_date, api_key):
    api_param = {
        'series_id': series_id,
        'observation_start': start_date,
        'observation_end': end_date,
        'file_type': 'json',
        'api_key': api_key
    }
    return api_param

def get_data(url, api_param):
    response = requests.get(url, params=api_param)
    if (response.status_code == 200):
        data = response.json()
    else:
        print(f"Error: {response.status_code}")
    return data

def convert_to_df(data):
    df = pd.json_normalize(data, 'observations')
    df = df[['date', 'value']]
    return df