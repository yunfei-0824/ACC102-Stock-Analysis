# ACC102 Stock Analysis Project
S&P 500 Interactive Stock Analysis Tool

## Project Overview
This project provides an interactive web application for analyzing historical stock data of S&P 500 companies. Users can view price trends, technical indicators, risk metrics, and return performance through a friendly interface.

## Key Features
- Interactive stock selection and date range filtering
- Price trends and moving averages (MA5, MA20, MA60)
- Cumulative return and volatility analysis
- RSI and MACD technical indicators
- Max drawdown and risk distribution analysis
- Weekday return pattern analysis

## Files Included
- `app.py`: Main Streamlit application
- `sp500_stocks.zip`: Compressed stock dataset
- `requirements.txt`: Required packages
- `README.md`: Project documentation

## How to Run
The application automatically handles the data file. No manual extraction is needed.

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
2. Launch the interactive application
   ```bash
   streamlit run app.py
   
- Note: If the CSV file is missing, the app will automatically extract it from the included ZIP archive on first run.

## Data Description
Historical stock data including Date, Symbol, Open, High, Low, Close, Adj Close, Volume.
## Tools Used
- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
## Important Notes
The dataset is compressed into a ZIP file due to GitHub file size limits. Please unzip before running the application.
