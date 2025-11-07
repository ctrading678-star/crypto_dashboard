import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta

st.set_page_config(page_title="Crypto Dashboard", layout="wide")

st.title("📊 لوحة متابعة العملات الرقمية")

# قائمة أشهر 40 عملة رقمية (رموز Yahoo Finance)
crypto_symbols = {
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Binance Coin (BNB)": "BNB-USD",
    "Solana (SOL)": "SOL-USD",
    "Cardano (ADA)": "ADA-USD",
    "XRP (XRP)": "XRP-USD",
    "Dogecoin (DOGE)": "DOGE-USD",
    "Avalanche (AVAX)": "AVAX-USD",
    "Polkadot (DOT)": "DOT-USD",
    "Chainlink (LINK)": "LINK-USD",
    "Polygon (MATIC)": "MATIC-USD",
    "Litecoin (LTC)": "LTC-USD",
    "Shiba Inu (SHIB)": "SHIB-USD",
    "Uniswap (UNI)": "UNI-USD",
    "Bitcoin Cash (BCH)": "BCH-USD",
    "Stellar (XLM)": "XLM-USD",
    "Cosmos (ATOM)": "ATOM-USD",
    "VeChain (VET)": "VET-USD",
    "Internet Computer (ICP)": "ICP-USD",
    "Aave (AAVE)": "AAVE-USD",
    "Filecoin (FIL)": "FIL-USD",
    "Maker (MKR)": "MKR-USD",
    "The Graph (GRT)": "GRT-USD",
    "Algorand (ALGO)": "ALGO-USD",
    "Tezos (XTZ)": "XTZ-USD",
    "Decentraland (MANA)": "MANA-USD",
    "EOS (EOS)": "EOS-USD",
    "IOTA (IOTA)": "IOTA-USD",
    "Axie Infinity (AXS)": "AXS-USD",
    "SAND (The Sandbox)": "SAND-USD",
    "Fantom (FTM)": "FTM-USD",
    "NEAR Protocol (NEAR)": "NEAR-USD",
    "Curve DAO (CRV)": "CRV-USD",
    "THETA (THETA)": "THETA-USD",
    "OKB (OKB)": "OKB-USD",
    "Lido DAO (LDO)": "LDO-USD",
    "Injective (INJ)": "INJ-USD",
    "Rocket Pool (RPL)": "RPL-USD",
    "Aptos (APT)": "APT-USD",
    "Arbitrum (ARB)": "ARB-USD"
}

# --- اختيار العملة والفترة الزمنية ---
col1, col2 = st.columns(2)

with col1:
    selected_crypto = st.selectbox("🪙 اختر العملة الرقمية", list(crypto_symbols.keys()))

with col2:
    days = st.slider("📆 عدد الأيام السابقة", 7, 365, 90)

# --- تحميل البيانات ---
symbol = crypto_symbols[selected_crypto]
start_date = date.today() - timedelta(days=days)
end_date = date.today()

st.info(f"جلب البيانات من {start_date} إلى {end_date} ...")

data = yf.download(symbol, start=start_date, end=end_date)

if data.empty:
    st.error("⚠️ لم يتم العثور على بيانات لهذه العملة.")
else:
    st.subheader(f"💹 الرسم البياني لـ {selected_crypto}")
    
    # --- رسم الشموع اليابانية ---
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Candlestick'
    )])
    
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        template='plotly_dark',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # --- عرض الجدول ---
    st.subheader("📄 البيانات الخام")
    st.dataframe(data.tail(20))

