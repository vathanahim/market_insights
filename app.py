import streamlit as st  # or the full path
from helper import helper_func as hf
import datetime
from dotenv import load_dotenv
import os

st.title('Market Insights')


load_dotenv()

api_key = os.getenv('API_KEY')
base_url = 'https://api.stlouisfed.org/fred/series/observations'
cur_date = datetime.datetime.now().strftime('%Y-%m-%d')

param = hf.create_api_param('DTWEXBGS', '2025-01-01', cur_date, api_key)
data = hf.get_data(base_url, param)
df = hf.convert_to_df(data)

st.write(df)

