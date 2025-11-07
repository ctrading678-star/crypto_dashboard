import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import date, timedelta

# =========================
# إعداد الصفحة
# =========================
st.set_page_config(page_title="📊 تحليل العملات الرقمية", layout="wide")
st.title("💰 لوحة تحليل العملات الرقمية (Crypto Dashboard)")

# =========================
# قائمة أشهر 40 عملة رقمية
# =========================
crypto_list = [
    "BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOGE-USD",
    "AVAX-USD", "TRX-USD", "DOT-USD", "MATIC-USD", "LTC-USD", "SHIB-USD", "UNI-USD",
    "BCH-USD", "LINK-USD", "XLM-USD", "ATOM-USD", "ETC-USD", "HBAR-USD",
    "ICP-USD", "APT-USD", "VET-USD", "FIL-USD", "NEAR-USD", "QNT-USD",
    "AAVE-USD", "GRT-USD", "ALGO-USD", "SAND-USD", "EGLD-USD", "AXS-USD",
    "MANA-USD", "THETA-USD", "FTM-USD", "XTZ-USD", "XMR-USD", "KAS-USD",
    "IMX-USD", "RUNE-USD"
]

# =========================
# واجهة المستخدم
# =========================
symbol = st.selectbox("🔸 اختر العملة:", crypto_list)

mode = st.radio("🗓️ اختر طريقة تحديد الفترة:", ["آخر عدد من الأيام", "تحديد تاريخين"])

if mode == "آخر عدد من الأيام":
    days = st.slider("عدد الأيام:", 7, 730, 350)
    start_date = date.today() - timedelta(days=days)
    end_date = date.today()
else:
    start_date = st.date_input("من تاريخ:", date.today() - timedelta(days=350))
    end_date = st.date_input("إلى تاريخ:", date.today())

interval = st.selectbox(
    "⏱️ اختر الإطار الزمني:",
    ["1h", "4h", "1d", "1wk", "1mo"],
    index=2,
    help="مثال: 1h = كل ساعة، 1d = يومي، 1wk = أسبوعي"
)

# =========================
# تحميل البيانات
# =========================
if st.button("📈 تحميل البيانات"):
    with st.spinner("⏳ جاري تحميل بيانات السوق..."):
        data = yf.download(symbol, start=start_date, end=end_date, interval=interval)

        # تنظيف البيانات والتحقق
        if data.empty:
            st.warning("⚠️ لم يتم العثور على بيانات للفترة أو الإطار الزمني المحدد.")
        else:
            # الاحتفاظ بآخر 350 صف فقط
            data = data.tail(350).copy()
            data.reset_index(inplace=True)

            # التأكد من وجود العمود 'Close'
            if "Close" not in data.columns:
                st.error("❌ لا يمكن الرسم: العمود 'Close' غير موجود في البيانات.")
                st.dataframe(data.head(), use_container_width=True)
            else:
                st.success(f"✅ تم تحميل {len(data)} نقطة من بيانات {symbol}")

                st.dataframe(data.tail(10), use_container_width=True)

                # إنشاء الرسم
                fig = px.line(
                    data,
                    x=data.columns[0],  # أول عمود عادة هو التاريخ
                    y="Close",
                    title=f"📉 حركة سعر {symbol} - آخر {len(data)} شمعة",
                    labels={"Close": "سعر الإغلاق", data.columns[0]: "التاريخ"}
                )

                st.plotly_chart(fig, use_container_width=True)

                # تحميل CSV
                csv = data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ تحميل البيانات كملف CSV",
                    data=csv,
                    file_name=f"{symbol}_data.csv",
                    mime="text/csv"
                )

