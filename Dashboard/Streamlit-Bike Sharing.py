import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

# --- SETUP PAGE ---
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

# --- LOAD DATA ---
dataset = pd.read_csv("Bike_Sharing.csv")

# --- SIDEBAR ---
st.sidebar.title("🚲 Bike Sharing Dashboard")
st.sidebar.markdown("### Hello! 👋")
name = st.sidebar.text_input("Masukkan namamu:")
if name:
    st.sidebar.success(f"Halo, {name}! Selamat menjelajahi dashboard 🚴‍♂️")

year_filter = st.sidebar.selectbox("Pilih Tahun:", sorted(dataset['yr'].unique()))
dataset_filtered = dataset[dataset['yr'] == year_filter]

# --- HEADER ---
st.title("🚲 **Bike Sharing Analysis Dashboard**")
st.markdown(
    "Menampilkan hasil analisis penyewaan sepeda berdasarkan data tahun 2011–2012. "
    "Gunakan filter di sebelah kiri untuk eksplorasi lebih lanjut."
)

# --- METRICS SECTION ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Rata-rata Penyewaan", f"{dataset_filtered['cnt'].mean():,.0f}")
with col2:
    st.metric("Penyewaan Tertinggi", f"{dataset_filtered['cnt'].max():,.0f}")
with col3:
    st.metric("Penyewaan Terendah", f"{dataset_filtered['cnt'].min():,.0f}")

st.markdown("---")

# --- TABS UNTUK SETIAP VISUALISASI ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📈 Tren Bulanan", "🌤️ Musim", "🌦️ Cuaca", "🏖️ Hari Libur", "📅 Hari dalam Minggu"]
)

# 1️⃣ TREND
with tab1:
    monthly_counts = (
        dataset_filtered.groupby("mnth", as_index=False)["cnt"].mean()
        .assign(mnth=lambda x: pd.Categorical(x["mnth"],
                                              categories=['Jan','Feb','Mar','Apr','May','Jun',
                                                          'Jul','Aug','Sep','Oct','Nov','Dec'],
                                              ordered=True))
    )
    fig = px.line(monthly_counts, x="mnth", y="cnt", markers=True,
                  title=f"Tren Penyewaan Sepeda Tahun {year_filter}",
                  color_discrete_sequence=["#2E8B57"])
    st.plotly_chart(fig, use_container_width=True)
    st.info("📌 **Insight:** Puncak penyewaan biasanya terjadi di pertengahan hingga akhir tahun.")

# 2️⃣ SEASON
with tab2:
    season_pattern = dataset_filtered.groupby('season')[['registered', 'casual']].sum().reset_index()
    fig = px.bar(season_pattern, x='season', y=['registered', 'casual'], barmode='group',
                 title="Pengaruh Musim terhadap Jumlah Pengguna",
                 color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig, use_container_width=True)
    st.info("📌 **Insight:** Musim gugur memiliki jumlah penyewaan tertinggi, sedangkan musim semi terendah.")

# 3️⃣ WEATHER
with tab3:
    fig = px.bar(dataset_filtered, x='weathersit', y='cnt',
                 color='weathersit', title="Pengaruh Cuaca terhadap Penyewaan",
                 color_discrete_sequence=px.colors.sequential.YlOrBr)
    st.plotly_chart(fig, use_container_width=True)
    st.info("📌 **Insight:** Cuaca cerah mendorong lebih banyak penyewaan dibandingkan saat hujan atau berawan.")

# 4️⃣ HOLIDAY
with tab4:
    fig = px.bar(dataset_filtered, x='workingday', y='cnt',
                 color='workingday', title="Perbandingan Hari Kerja dan Libur",
                 color_discrete_sequence=["#FFB347", "#87CEEB"])
    st.plotly_chart(fig, use_container_width=True)
    st.info("📌 **Insight:** Penyewaan meningkat pada hari kerja dan menurun saat hari libur.")

# 5️⃣ WEEKDAY
with tab5:
    fig = px.bar(dataset_filtered, x='weekday', y='cnt',
                 title="Distribusi Penyewaan Berdasarkan Hari",
                 category_orders={"weekday": ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']},
                 color_discrete_sequence=["#1E90FF"])
    st.plotly_chart(fig, use_container_width=True)
    st.info("📌 **Insight:** Aktivitas penyewaan tertinggi terjadi pada hari kerja (Senin–Jumat).")

st.markdown("---")
st.caption("📊 Dashboard dikembangkan oleh Muhammad Muthi' Nuritzan | Universitas Brawijaya")