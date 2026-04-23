import zipfile
import os

if not os.path.exists("sp500_stocks.csv"):
    with zipfile.ZipFile("sp500_stocks.zip", "r") as zip_ref:
        zip_ref.extractall(".")

import pandas as pd
df = pd.read_csv("sp500_stocks.csv")

import streamlit as st
import pandas as pd
import zipfile
import os

# --------------------------
# 自动解压zip数据集
# --------------------------
if not os.path.exists("sp500_stocks.csv"):
    with zipfile.ZipFile("sp500_stocks.zip", "r") as zip_ref:
        zip_ref.extractall(".")

# 读取并处理日期
df = pd.read_csv("sp500_stocks.csv")
df["Date"] = pd.to_datetime(df["Date"])

# 获取全部股票代码
unique_symbols = sorted(df["Symbol"].unique())

# --------------------------
# 方案三：热门股票加⭐标记
# --------------------------
popular_symbols = ["NVDA", "AAPL", "MSFT", "AMZN", "GOOGL", "TSLA"]
symbol_options = [
    f"{sym} ⭐" if sym in popular_symbols else sym
    for sym in unique_symbols
]

# --------------------------
# 方案一：侧边栏默认NVDA + 完整时间区间
# --------------------------
st.sidebar.header("⚙️ Analysis Settings")

# 默认选中 NVDA ⭐
symbol_with_mark = st.sidebar.selectbox(
    "Select a stock symbol (⭐ = Popular, guaranteed data)",
    options=symbol_options,
    index=symbol_options.index("NVDA ⭐")
)
symbol = symbol_with_mark.replace(" ⭐", "")

# 时间默认全数据范围
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()
start_date, end_date = st.sidebar.date_input(
    "Select date range",
    value=[min_date, max_date]
)

# 日期格式转换
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# 筛选数据
filtered_df = df[
    (df["Symbol"] == symbol) &
    (df["Date"] >= start_date) &
    (df["Date"] <= end_date)
]

# --------------------------
# 页面主体展示
# --------------------------
st.title("📈 S&P 500 Stock Analysis Dashboard")
st.markdown("""
Welcome to the interactive stock analysis tool.
You can freely choose any stock symbol and custom date range in the sidebar.
Stocks marked with ⭐ are recommended with stable complete data.
""")

if filtered_df.empty:
    st.warning(f"No data available for {symbol} in the current date range.")
else:
    st.subheader(f"📊 Analysis Result: {symbol}")
    st.dataframe(filtered_df.head(20))
    st.line_chart(filtered_df.set_index("Date")["Close"])
