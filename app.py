import zipfile
import os

if not os.path.exists("sp500_stocks.csv"):
    with zipfile.ZipFile("sp500_stocks.zip", "r") as zip_ref:
        zip_ref.extractall(".")

import pandas as pd
df = pd.read_csv("sp500_stocks.csv")

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="S&P 500 Stock Analyzer", layout="wide")
st.title("📊 S&P 500 Stock  Analysis ")
st.markdown("---")

@st.cache_data
def load_data():
    df = pd.read_csv("sp500_stocks.csv")
    df.columns = df.columns.str.replace(" ", "_")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()
min_date = df["Date"].min()
max_date = df["Date"].max()

with st.sidebar:
    st.header("⚙️ Control Panel")
    symbols = sorted(df["Symbol"].unique())

    popular_symbols = ["NVDA", "MSFT", "AMZN", "GOOGL", "TSLA"]
    symbol_options = [f"{s} ⭐" if s in popular_symbols else s for s in symbols]

    default_idx = symbol_options.index("NVDA ⭐")
    selected_with_star = st.selectbox("Choose Stock Symbol (⭐ = Full Data)", symbol_options, index=default_idx)
    selected = selected_with_star.replace(" ⭐", "")

    st.info(f"Data Available: {min_date.date()} → {max_date.date()}")
    start = st.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
    end = st.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

start_ts = pd.Timestamp(start)
end_ts = pd.Timestamp(end)

data = df[
    (df["Symbol"] == selected) &
    (df["Date"] >= start_ts) &
    (df["Date"] <= end_ts)
].copy()
data = data.sort_values("Date").reset_index(drop=True)

if data.empty:
    st.error("❌ No data available for selected range.")
    st.stop()

data = data.dropna(subset=["Adj_Close"])

if len(data) == 0:
    st.error("❌ No valid price data available for this range.")
    st.stop()

data["daily_return"] = data["Adj_Close"].pct_change()
data["cum_return"] = (1 + data["daily_return"]).cumprod() - 1
data["vol_20d"] = data["daily_return"].rolling(20).std() * np.sqrt(252)

data["ma5"] = data["Adj_Close"].rolling(5).mean()
data["ma20"] = data["Adj_Close"].rolling(20).mean()
data["ma60"] = data["Adj_Close"].rolling(60).mean()

delta = data["Adj_Close"].diff()
gain = delta.mask(delta < 0, 0)
loss = -delta.mask(delta > 0, 0)
avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()
rs = avg_gain / avg_loss.replace(0, np.nan)
data["rsi"] = 100 - (100 / (1 + rs))

ema12 = data["Adj_Close"].ewm(span=12, adjust=False).mean()
ema26 = data["Adj_Close"].ewm(span=26, adjust=False).mean()
data["macd"] = ema12 - ema26
data["signal"] = data["macd"].ewm(span=9, adjust=False).mean()

cum_ret_clean = data["cum_return"].dropna()
drawdown = pd.Series(dtype="float64")
max_dd = np.nan

if len(cum_ret_clean) > 5:
    running_max = cum_ret_clean.cummax()
    drawdown = (cum_ret_clean - running_max) / running_max
    max_dd = drawdown.min()

st.subheader("📌 Performance Summary")
c1, c2, c3, c4 = st.columns(4)

if len(data) > 0 and not pd.isna(data['cum_return'].iloc[-1]):
    c1.metric("Total Return", f"{data['cum_return'].iloc[-1]:.2%}")
else:
    c1.metric("Total Return", "N/A")

if len(data) > 0 and not pd.isna(data['daily_return'].mean()):
    c2.metric("Avg Daily Return", f"{data['daily_return'].mean():.3%}")
else:
    c2.metric("Avg Daily Return", "N/A")

if len(data) > 0 and not pd.isna(data['vol_20d'].mean()):
    c3.metric("Annual Volatility", f"{data['vol_20d'].mean():.2%}")
else:
    c3.metric("Annual Volatility", "N/A")

if not np.isnan(max_dd):
    c4.metric("Max Drawdown", f"{max_dd:.2%}")
else:
    c4.metric("Max Drawdown", "N/A")

st.markdown("---")

st.subheader("Price and Moving Averages")
fig1, ax1 = plt.subplots(figsize=(16, 5))
ax1.plot(data["Date"], data["Adj_Close"], label="Adj Close")
ax1.plot(data["Date"], data["ma5"], label="MA5")
ax1.plot(data["Date"], data["ma20"], label="MA20")
ax1.plot(data["Date"], data["ma60"], label="MA60")
ax1.legend()
ax1.grid(alpha=0.3)
st.pyplot(fig1)

colA, colB = st.columns(2)
with colA:
    st.subheader("Cumulative Return")
    fig2, ax2 = plt.subplots(figsize=(8, 3.5))
    ax2.plot(data["Date"], data["cum_return"], color="darkred")
    ax2.grid(alpha=0.3)
    st.pyplot(fig2)

with colB:
    st.subheader("20-Day Volatility")
    fig3, ax3 = plt.subplots(figsize=(8, 3.5))
    ax3.plot(data["Date"], data["vol_20d"], color="orange")
    ax3.grid(alpha=0.3)
    st.pyplot(fig3)

colC, colD = st.columns(2)
with colC:
    st.subheader("RSI (14)")
    fig4, ax4 = plt.subplots(figsize=(8, 3.5))
    ax4.plot(data["Date"], data["rsi"], color="purple")
    ax4.axhline(70, c="red", ls="--")
    ax4.axhline(30, c="green", ls="--")
    ax4.grid(alpha=0.3)
    st.pyplot(fig4)

with colD:
    st.subheader("MACD")
    fig5, ax5 = plt.subplots(figsize=(8, 3.5))
    ax5.plot(data["Date"], data["macd"], label="MACD")
    ax5.plot(data["Date"], data["signal"], label="Signal")
    ax5.legend()
    ax5.grid(alpha=0.3)
    st.pyplot(fig5)

st.subheader("Risk & Distribution Analysis")
fig6, axes = plt.subplots(2, 2, figsize=(16, 8))

ret_drop = data["daily_return"].dropna()
if len(ret_drop) > 0:
    axes[0,0].hist(ret_drop, bins=50, color="skyblue", alpha=0.7)
axes[0,0].set_title("Daily Return Distribution")
axes[0,0].grid(alpha=0.3)

if len(drawdown) > 0:
    axes[0,1].plot(cum_ret_clean.index, drawdown, color="red")
axes[0,1].set_title("Drawdown Curve")
axes[0,1].grid(alpha=0.3)

price_clean = data["Adj_Close"].dropna()
if len(price_clean) > 0:
    axes[1,0].hist(price_clean, bins=50, color="orange", alpha=0.7)
axes[1,0].set_title("Price Distribution")
axes[1,0].grid(alpha=0.3)

wd_list = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
wdata = data.copy()
wdata["weekday"] = wdata["Date"].dt.day_name()
wd_ret = wdata.groupby("weekday")["daily_return"].mean().reindex(wd_list)
axes[1,1].bar(wd_ret.index, wd_ret.values, color="green", alpha=0.7)
axes[1,1].set_title("Weekday Average Return")
axes[1,1].grid(alpha=0.3)

plt.tight_layout()
st.pyplot(fig6)

st.success("✅ Analysis completed successfully!")
