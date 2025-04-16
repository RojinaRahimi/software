import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# تنظیمات اولیه صفحه
st.set_page_config(page_title="داشبورد مدیریتی", layout="wide")
st.title("داشبورد مدیریتی سیستم")

# داده‌های نمونه
@st.cache_data
def load_sample_data():
    users = pd.DataFrame({
        "کاربر": ["کاربر ۱", "کاربر ۲", "کاربر ۳", "کاربر ۴"],
        "دسترسی": ["مدیر", "کاربر", "کاربر", "مهمان"],
        "تعداد فعالیت": [45, 12, 8, 3],
        "آخرین ورود": ["1403-01-15", "1403-01-10", "1403-01-05", "1402-12-28"]
    })
    
    transactions = pd.DataFrame({
        "تاریخ": pd.date_range(start="1403-01-01", end="1403-01-30"),
        "مبلغ": [1000, 1500, 800, 1200, 2000] * 6,
        "نوع": ["فروش", "پرداخت", "فروش", "بازپرداخت", "فروش"] * 6
    })
    
    return users, transactions

users_df, transactions_df = load_sample_data()

# نوار کناری برای فیلترها
with st.sidebar:
    st.header("فیلترها")
    start_date = st.date_input("تاریخ شروع", datetime(2024, 1, 1))
    end_date = st.date_input("تاریخ پایان", datetime(2024, 1, 30))
    user_type = st.multiselect("نوع کاربر", options=users_df["دسترسی"].unique())

# نمایش کارت‌های خلاصه اطلاعات
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("تعداد کاربران", len(users_df))
with col2:
    st.metric("مجموع تراکنش‌ها", f"{transactions_df['مبلغ'].sum():,} تومان")
with col3:
    st.metric("میانگین تراکنش", f"{transactions_df['مبلغ'].mean():,.0f} تومان")

# نمودارها
tab1, tab2, tab3 = st.tabs(["کاربران", "تراکنش‌ها", "گزارش‌ها"])

with tab1:
    fig1 = px.bar(users_df, x="کاربر", y="تعداد فعالیت", color="دسترسی",
                 title="فعالیت کاربران بر اساس سطح دسترسی")
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    fig2 = px.line(transactions_df.groupby("تاریخ")["مبلغ"].sum().reset_index(),
                  x="تاریخ", y="مبلغ", title="تراکنش‌های روزانه")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    fig3 = px.pie(transactions_df, names="نوع", title="توزیع انواع تراکنش‌ها")
    st.plotly_chart(fig3, use_container_width=True)

# جدول داده‌ها
st.subheader("اطلاعات کاربران")
st.dataframe(users_df)

st.subheader("اطلاعات تراکنش‌ها")
st.dataframe(transactions_df)