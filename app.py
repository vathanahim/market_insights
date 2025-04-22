import streamlit as st  # or the full path
from helper import helper_func as hf
import datetime
from dotenv import load_dotenv
import os
import plotly.express as px
import pandas as pd

st.title('Market Insights')


load_dotenv()

api_key = os.getenv('API_KEY')
base_url = 'https://api.stlouisfed.org/fred/series/observations'
cur_date = datetime.datetime.now().strftime('%Y-%m-%d')

param = hf.create_api_param('DTWEXBGS', '2025-01-01', cur_date, api_key)
data = hf.get_data(base_url, param)
df = hf.convert_to_df(data)

with st.container(border=True):
    start_date, end_date = st.slider(
    "Select date range",
    min_value=df['date'].min().date(),
    max_value=df['date'].max().date(),
    value=(df['date'].min().date(), df['date'].max().date())
    )

    st.subheader('USD INDEX OVERTIME')
    filtered_df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]

    fig = px.line(filtered_df, x='date', y='value')
    fig.update_layout(
        title='USD INDEX OVERTIME',
        xaxis_title='Date',
        yaxis_title='Value',
        xaxis_tickformat='%Y-%m-%d'
    )
    st.plotly_chart(fig)


