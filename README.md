# Market Insights Dashboard

A Streamlit-based dashboard that visualizes key economic indicators including USD Index, Treasury Yields, Mortgage Rates, and Home Price Index if you're looking for the perfect time to purchase a house

## Features

- Real-time economic data visualization
- Interactive date range selection
- Side-by-side comparison of different economic indicators
- Key metrics and trend analysis
- Monthly and daily data handling

## Data Sources

The dashboard uses the FRED (Federal Reserve Economic Data) API to fetch:
- USD Index (DTWEXBGS)
- 10-Year Treasury Yield (DGS10)
- 30-Year Mortgage Rate (MORTGAGE30US)
- Home Price Index (CSUSHPISA)


## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Use the date range selectors to view data for specific periods

## Project Structure

```
market_insights/
├── app.py                 # Main Streamlit application
├── helper/
│   └── helper_func.py     # Helper functions for API calls and data processing
├── .env                   # Environment variables (not in version control)
├── .gitignore            # Git ignore file
└── requirements.txt      # Project dependencies
```

## Dependencies

- streamlit
- pandas
- plotly
- python-dotenv
- requests

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FRED API for providing economic data
- Streamlit for the web framework
- Plotly for interactive visualizations