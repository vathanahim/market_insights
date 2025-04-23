import streamlit as st  # or the full path
from helper import helper_func as hf
import datetime
from dotenv import load_dotenv
import os
import plotly.express as px
import pandas as pd

# Set page config for better layout
st.set_page_config(
    page_title="Market Insights Dashboard",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stContainer {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title('Market Insights Dashboard')

load_dotenv()

api_key = os.getenv('API_KEY')
base_url = os.getenv('BASE_URL') 
cur_date = datetime.datetime.now().strftime('%Y-%m-%d')


# Define manual default dates
default_start = datetime.date.today() - datetime.timedelta(days=30)
default_end = datetime.date.today()

# Date input fields
col_date1, col_date2 = st.columns(2)
with col_date1:
    start_date = st.date_input(
        "Start Date",
        value=default_start,
        min_value=datetime.date(2000, 1, 1),
        max_value=default_end
    )
with col_date2:
    end_date = st.date_input(
        "End Date",
        value=default_end,
        min_value=start_date,
        max_value=datetime.date.today()
    )


# Use the selected dates for API calls
param_usd_index = hf.create_api_param('DTWEXBGS', start_date, end_date, api_key)
data_usd_index = hf.get_data(base_url, param_usd_index)
df_usd_index = hf.convert_to_df(data_usd_index)

ten_treasury_index = hf.create_api_param('DGS10', start_date, end_date, api_key)
data_treasury_index = hf.get_data(base_url, ten_treasury_index)
df_treasury_index = hf.convert_to_df(data_treasury_index)

mortgage_index = hf.create_api_param('MORTGAGE30US', start_date, end_date, api_key)
data_mortgage_index = hf.get_data(base_url, mortgage_index)
df_mortgage_index = hf.convert_to_df(data_mortgage_index)

home_price_index = hf.create_api_param('CSUSHPISA', '1900-01-01', end_date, api_key)
data_home_price_index = hf.get_data(base_url, home_price_index)
df_home_price_index = hf.convert_to_df(data_home_price_index)



def create_metrics(df, col, start_date, end_date, title:str):
    with col:
        with st.container(border=True):
            st.subheader(f'{title} Key Metrics')

        filtered_df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]
            
        # Calculate and display key metrics
        latest_value = filtered_df['value'].iloc[-1]
        previous_value = filtered_df['value'].iloc[0]
        change = ((latest_value - previous_value) / previous_value) * 100
        
        st.metric(
            label="Previous Value",
            value=f"{previous_value:.2f}"
        )
        st.metric(
            label="Current Value",
            value=f"{latest_value:.2f}",
            delta=f"{change:.2f}%"
        )
        
        # Display statistics
        st.write("**Statistics**")
        stats = filtered_df['value'].describe()
        st.write(f"Mean: {stats['mean']:.2f}")
        st.write(f"Min: {stats['min']:.2f}")
        st.write(f"Max: {stats['max']:.2f}")
        
        # Add a small trend indicator
        if change > 0:
            st.success("Upward Trend")
        else:
            st.error("Downward Trend")



def create_chart(df, start_date, end_date, title:str, subtitle:str, yaxis_title:str, xaxis_title:str):
    col1, col2 = st.columns([2, 1])

    with col1:
      
            # Only create slider if we have a valid date range
        min_date = df['date'].min().date()
        max_date = df['date'].max().date()
        if min_date < max_date:
            date_range = st.slider(
                "Select Date Range", 
                min_value=min_date, 
                max_value=max_date, 
                value=(min_date, max_date)
            )
            start_date, end_date = date_range
        else:
            st.warning("Not enough data points for date range selection")
            start_date, end_date = min_date, max_date
            

        with st.container(border=True):
            st.subheader(title)

            filtered_df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]
            
            # Enhanced Plotly chart with better styling
            fig = px.line(
                filtered_df, 
                x='date', 
                y='value',
                title=subtitle,
                template='plotly_white'
            )
            
            fig.update_layout(
                xaxis_title=xaxis_title,
                yaxis_title=yaxis_title,
                xaxis_tickformat='%Y-%m-%d',
                hovermode='x unified',
                showlegend=False,
                height=500,
                margin=dict(l=50, r=50, t=50, b=50),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            
            fig.update_traces(
                line=dict(width=2.5, color='#1f77b4'),
                hovertemplate='Date: %{x}<br>Value: %{y:.2f}<extra></extra>'
            )

            create_metrics(df, col2, start_date, end_date, title)
            
            return st.plotly_chart(fig, use_container_width=True)

def create_chart_monthly(df, start_date, end_date, title:str, subtitle:str, yaxis_title:str, xaxis_title:str):
    col1, col2 = st.columns([2, 1])

    with col1:
      
            # Only create slider if we have a valid date range
        min_date = df['date'].min().date()
        max_date = df['date'].max().date()
        if min_date < max_date:
            date_range = st.slider(
                "Select Date Range", 
                min_value=min_date, 
                max_value=max_date, 
                value=(min_date, max_date)
            )
            start_date, end_date = date_range
        else:
            st.warning("Not enough data points for date range selection")
            start_date, end_date = min_date, max_date
            

        with st.container(border=True):
            st.subheader(title)

            filtered_df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]
            
            # Enhanced Plotly chart with better styling
            fig = px.line(
                filtered_df, 
                x='date', 
                y='value',
                title=subtitle,
                template='plotly_white'
            )
            
            fig.update_layout(
                xaxis_title=xaxis_title,
                yaxis_title=yaxis_title,
                xaxis_tickformat='%Y-%m-%d',
                hovermode='x unified',
                showlegend=False,
                height=500,
                margin=dict(l=50, r=50, t=50, b=50),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            
            fig.update_traces(
                line=dict(width=2.5, color='#1f77b4'),
                hovertemplate='Date: %{x}<br>Value: %{y:.2f}<extra></extra>'
            )

            create_metrics(df, col2, start_date, end_date, title)
            
            return st.plotly_chart(fig, use_container_width=True)


def main():
    if start_date and end_date and start_date <= end_date:
        # First chart and metrics pair
        
        create_chart(df_usd_index, start_date, end_date, 'USD Index Over Time', 'USD Index Over Time', 'Index Value', 'Date')
        #Add some spacing between pairs
        st.markdown("---")
        create_chart(df_treasury_index, start_date, end_date, '10-Year Treasury Yield Over Time', '10-Year Treasury Yield Over Time', 'Yield Value', 'Date')
        st.markdown("---")
        create_chart(df_mortgage_index, start_date, end_date, '30-Year Mortgage Rate Over Time', '30-Year Mortgage Rate Over Time', 'Rate Value', 'Date')
        st.markdown("---")
        create_chart_monthly(df_home_price_index, start_date, end_date, 'Monthly Home Price Index Over Time', 'Monthly Home Price Index Over Time', 'Index Value', 'Date')
        st.success(f"Displaying data from {start_date} to {end_date}")
    else:
        st.info("Please select a valid date range to continue.")

if __name__ == "__main__":
    main()
