import streamlit as st
import pandas as pd
import yfinance as yf
import datetime

# --- عنوان التطبيق ---
st.title("💱 عرض آخر 250 يوم من بيانات العملات الرقمية (Yahoo Finance)")

# --- قائمة العملات الشهيرة (يمكنك تعديلها بحرية) ---
crypto_list = {
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Binance Coin (BNB)": "BNB-USD",
    "Cardano (ADA)": "ADA-USD",
    "Solana (SOL)": "SOL-USD",
    "Ripple (XRP)": "XRP-USD",
    "Dogecoin (DOGE)": "DOGE-USD",
    "Litecoin (LTC)": "LTC-USD",
    "Avalanche (AVAX)": "AVAX-USD",
    "Shiba Inu (SHIB)": "SHIB-USD"
}

# --- اختيار العملة ---
selected_name = st.selectbox("🔹 اختر العملة:", list(crypto_list.keys()))
selected_symbol = crypto_list[selected_name]

# --- جلب البيانات من Yahoo Finance ---
st.info(f"⏳ يتم جلب بيانات {selected_name} من Yahoo Finance ...")

try:
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=365)  # سنة واحدة كحد أقصى
    data = yf.download(selected_symbol, start=start_date, end=end_date)

    if data.empty:
        st.error("⚠️ لم يتم العثور على بيانات لهذه العملة.")
    else:
        # --- إعادة ترتيب الأعمدة ---
        data.reset_index(inplace=True)
        data = data[["Date", "Open", "High", "Low", "Close", "Volume"]]

        # --- أخذ آخر 250 يوم ---
        last_250 = data.tail(250)

        # --- عرض النتائج ---
        st.success(f"✅ تم جلب بيانات {selected_name} بنجاح!")
        st.dataframe(last_250)

        # --- عرض آخر تاريخ ---
        last_date = last_250["Date"].max().strftime("%Y-%m-%d")
        st.info(f"📅 آخر تاريخ في البيانات: {last_date}")

except Exception as e:
    st.error(f"حدث خطأ أثناء جلب البيانات: {e}")
