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
# 1. 自动解压数据文件
# --------------------------
if not os.path.exists("sp500_stocks.csv"):
    with zipfile.ZipFile("sp500_stocks.zip", "r") as zip_ref:
        zip_ref.extractall(".")

# 读取数据
df = pd.read_csv("sp500_stocks.csv")
df["Date"] = pd.to_datetime(df["Date"])

# 获取所有股票代码
unique_symbols = sorted(df["Symbol"].unique())

# --------------------------
# 2. 定义热门股票（加⭐标记）
# --------------------------
popular_symbols = ["AAPL", "MSFT", "AMZN", "GOOGL", "TSLA"]
symbol_options = [
    f"{sym} ⭐" if sym in popular_symbols else sym 
    for sym in unique_symbols
]

# --------------------------
# 3. 侧边栏设置：默认加载AAPL+完整时间范围
# --------------------------
st.sidebar.header("⚙️ Analysis Settings")

# 股票选择（默认选中AAPL，带⭐标记）
symbol_with_mark = st.sidebar.selectbox(
    "Select a stock symbol (⭐ = Popular, guaranteed data)", 
    options=symbol_options,
    index=symbol_options.index("AAPL ⭐")
)
symbol = symbol_with_mark.replace(" ⭐", "")  # 去掉标记，保留原始代码逻辑

# 时间范围选择（默认选中整个数据区间）
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()
start_date, end_date = st.sidebar.date_input(
    "Select date range",
    value=[min_date, max_date]
)

# --------------------------
# 4. 过滤数据 + 无数据兜底提示
# --------------------------
# 转换日期格式
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# 过滤数据
filtered_df = df[
    (df["Symbol"] == symbol) & 
    (df["Date"] >= start_date) & 
    (df["Date"] <= end_date)
]

# --------------------------
# 5. 主页面展示
# --------------------------
st.title("📈 S&P 500 Stock Analysis Dashboard")
st.markdown("""
### Welcome! 
This tool lets you explore stock price trends, technical indicators, and risk metrics.
""")

# 判断是否有数据
if filtered_df.empty:
    st.error(f"⚠️ No data found for **{symbol}** in the selected date range.")
    st.info("💡 Tip: Try selecting a different symbol (prefer ones with ⭐) or a wider date range.")
    
    # 一键加载示例数据按钮
    if st.button("Load Example Data (AAPL Full History)"):
        filtered_df = df[df["Symbol"] == "AAPL"]
        st.subheader("📊 Example: AAPL Full Historical Data")
        st.dataframe(filtered_df.head())
        
        # 这里可以直接复制你原来的绘图代码，用filtered_df画图
        st.line_chart(filtered_df.set_index("Date")["Close"])
else:
    # 正常显示数据和图表（你原来的代码直接放在这里）
    st.subheader(f"📊 {symbol} Stock Analysis")
    st.dataframe(filtered_df.head())
    
    # 示例：收盘价走势图（替换成你自己的图表代码即可）
    st.line_chart(filtered_df.set_index("Date")["Close"])
