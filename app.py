
import streamlit as st
import pandas as pd
import requests
from io import StringIO
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="B2B Digital Strategy Dashboard", layout="wide")
st.title("📊 B2B Strategic Insights from High-Volume Transactions")
st.markdown("This dashboard analyzes performance, trends, and partner insights from large-scale CSV files hosted on Google Drive.")

# --- Dropdown for Module Selection ---
module = st.selectbox("Choose Analysis Module", [
    "Executive Dashboard",
    "Partner Analytics",
    "Roadmap Insights",
    "Geo Engagement Overview",
    "Download Filtered Dataset"
])

# --- Load Data from Google Drive ---
@st.cache_data
def load_large_data_from_drive():
    url_oct = "https://drive.google.com/uc?export=download&id=1diBWJtQdM6EOn3Vf-5vF7NTvkibCxOA9"
    url_nov = "https://drive.google.com/uc?export=download&id=1Q4IGeFzVYqauOJ0DBHPRfCZAEcHltNmW"

    def fetch_csv(url):
        response = requests.get(url)
        return pd.read_csv(StringIO(response.content.decode('utf-8', errors='ignore')))

    df_oct = fetch_csv(url_oct)
    df_nov = fetch_csv(url_nov)

    df = pd.concat([df_oct, df_nov], ignore_index=True)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    return df

df = load_large_data_from_drive()

# --- Module 1: Executive Dashboard ---
if module == "Executive Dashboard":
    st.subheader("📈 Executive Summary Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${df['Amount'].sum():,.0f}")
    col2.metric("Total Companies", df['Company'].nunique())
    col3.metric("Avg. Deal Size", f"${df['Amount'].mean():,.0f}")

    fig = px.bar(df.groupby('Product')['Amount'].sum().reset_index(),
                 x='Product', y='Amount', title="Revenue by Product", color='Product')
    st.plotly_chart(fig, use_container_width=True)

# --- Module 2: Partner Analytics ---
elif module == "Partner Analytics":
    st.subheader("🏢 Top B2B Partners by Revenue")
    partner_revenue = df.groupby('Company')['Amount'].sum().reset_index().sort_values(by='Amount', ascending=False)
    st.dataframe(partner_revenue)

    fig = px.pie(partner_revenue, names='Company', values='Amount', title="Revenue Share by Partner")
    st.plotly_chart(fig, use_container_width=True)

# --- Module 3: Roadmap Insights ---
elif module == "Roadmap Insights":
    st.subheader("🗺️ Product Investment Roadmap Insights")
    product_trends = df.groupby(['Date', 'Product'])['Amount'].sum().reset_index()
    fig = px.line(product_trends, x='Date', y='Amount', color='Product', title="Product Revenue Over Time")
    st.plotly_chart(fig, use_container_width=True)

# --- Module 4: Geo Engagement Overview ---
elif module == "Geo Engagement Overview":
    st.subheader("🌍 Revenue Distribution by Country")
    fig = px.choropleth(df, locations='Country', locationmode='country names',
                        color='Amount', hover_name='Company',
                        color_continuous_scale='Viridis',
                        title="Geographic Engagement via Revenue")
    st.plotly_chart(fig, use_container_width=True)

# --- Module 5: Download Dataset ---
elif module == "Download Filtered Dataset":
    st.subheader("💾 Export Data")
    st.download_button("Download CSV", df.to_csv(index=False), file_name="b2b_data_filtered.csv")
