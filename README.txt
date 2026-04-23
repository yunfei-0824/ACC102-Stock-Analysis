# ACC102 Stock Analysis Project
S&P 500 Interactive Stock Analysis Tool | FINTECH Assignment

## Project Overview
This project delivers an interactive web application for analyzing S&P 500 stock data. It includes technical indicators, risk metrics, return visualization, and professional plotting dashboards built with Streamlit.

## Key Features
- Interactive stock selection & date range filtering
- Price trends with moving averages (MA5, MA20, MA60)
- Cumulative return & volatility analysis
- Technical indicators: RSI, MACD
- Risk analysis: drawdown, return distribution
- Weekday return pattern analysis

## Project Structure
The repository contains the following files:
- `app.py` – Main Streamlit application (core code)
- `sp500_stocks.zip` – Compressed dataset (< 25MB)
- `requirements.txt` – Python dependencies
- `README.md` – Project documentation

## How to Run (Teacher's Guide)
1. **Download and unzip** the dataset:
   - Download `sp500_stocks.zip`
   - Extract it to get `sp500_stocks.csv`

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt