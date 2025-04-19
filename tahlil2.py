import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
def setup_page():
    st.set_page_config(
        page_title="داشبورد مدیریتی سیستم",
        layout="wide",
   
    st.title(" داشبورد مدیریتی سیستم")
    st.markdown("---")
 
def load_data():
    users_data = {
        "کاربر": ["کاربر ۱", "کاربر ۲", "کاربر ۳", "کاربر ۴"],
        "دسترسی": ["مدیر", "کاربر", "کاربر", "مهمان"],
        "تعداد فعالیت": [45, 12, 8, 3],
        "آخرین ورود": ["1403-01-15", "1403-01-10", "1403-01-05", "1402-12-28"]
    }
    
    transactions_data = {
        "تاریخ": pd.date_range(start="1403-01-01", end="1403-01-30"),
        "مبلغ": [1000, 1500, 800, 1200, 2000] * 6,
        "نوع": ["فروش", "پرداخت", "فروش", "بازپرداخت", "فروش"] * 6
    }
    
    return pd.DataFrame(users_data), pd.DataFrame(transactions_data)

 
def create_sidebar_filters(users_df):
    with st.sidebar:
        st.header(" فیلترها")
        st.markdown("---")
       
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("تاریخ شروع", datetime(2024, 1, 1))
        with col2:
            end_date = st.date_input("تاریخ پایان", datetime(2024, 1, 30))
        
        user_type = st.multiselect(
            "نوع کاربر",
            options=users_df["دسترسی"].unique(),
            default=users_df["دسترسی"].unique()
        )
        
        return start_date, end_date, user_type

def display_summary_cards(users_df, transactions_df):
    st.subheader("خلاصه اطلاعات")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="تعداد کاربران",
            value=len(users_df),
            delta=f"{len(users_df)} نفر"
        )
    
    with col2:
        st.metric(
            label="مجموع تراکنش‌ها",
            value=f"{transactions_df['مبلغ'].sum():,} تومان",
            delta="30 روز اخیر"
        )
    
    with col3:
        st.metric(
            label="میانگین تراکنش",
            value=f"{transactions_df['مبلغ'].mean():,.0f} تومان",
            delta=f"از {len(transactions_df)} تراکنش"
        )
    
    st.markdown("---")

def display_charts(users_df, transactions_df):
    tab1, tab2, tab3 = st.tabs([کاربران" تراکنش‌ها", " گزارش‌ها"])
    
    with tab1:
        fig1 = px.bar(
            users_df,
            x="کاربر",
            y="تعداد فعالیت",
            color="دسترسی",
            title="فعالیت کاربران بر اساس سطح دسترسی",
            text="تعداد فعالیت"
        )
        fig1.update_layout(height=500)
        st.plotly_chart(fig1, use_container_width=True)
    
    with tab2:
        daily_transactions = transactions_df.groupby("تاریخ")["مبلغ"].sum().reset_index()
        fig2 = px.line(
            daily_transactions,
            x="تاریخ",
            y="مبلغ",
            title="تراکنش‌های روزانه",
            markers=True
        )
        fig2.update_layout(height=500)
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab3:
        fig3 = px.pie(
            transactions_df,
            names="نوع",
            title="توزیع انواع تراکنش‌ها",
            hole=0.4
        )
        fig3.update_layout(height=500)
        st.plotly_chart(fig3, use_container_width=True)
def display_data_tables(users_df, transactions_df):
    st.subheader(" اطلاعات کامل")
    
    with st.expander("جدول کاربران", expanded=True):
        st.dataframe(
            users_df,
            use_container_width=True,
            hide_index=True
        )
    
    with st.expander("جدول تراکنش‌ها", expanded=False):
        st.dataframe(
            transactions_df,
            use_container_width=True,
            hide_index=True
        )

def main():
    setup_page()
    users_df, transactions_df = load_data()
    
    start_date, end_date, user_type = create_sidebar_filters(users_df)
    
    filtered_users = users_df[users_df["دسترسی"].isin(user_type)]
    filtered_transactions = transactions_df[
        (transactions_df["تاریخ"] >= pd.to_datetime(start_date)) &
        (transactions_df["تاریخ"] <= pd.to_datetime(end_date))
    ]
    
      display_summary_cards(filtered_users, filtered_transactions)
    display_charts(filtered_users, filtered_transactions)
    display_data_tables(filtered_users, filtered_transactions)

if __name__ == "__main__":
    main() 