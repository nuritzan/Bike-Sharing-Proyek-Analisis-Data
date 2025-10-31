import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

# Mengatur style plot
sns.set_style('whitegrid')

# --- PENTING: st.set_page_config HARUS MENJADI PERINTAH STREAMLIT PERTAMA ---
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)
# -----------------------------------------------------------------------------

# Fungsi untuk memuat dan membersihkan data (Data Wrangling)
@st.cache_data
def load_and_clean_data():
    # Asumsi file 'Bike_Sharing.csv' sudah tersedia
    try:
        df = pd.read_csv("Dashboard/Bike_Sharing.csv")
    except FileNotFoundError:
        st.error("File 'Bike_Sharing.csv' tidak ditemukan. Pastikan Anda sudah menjalankan proyek EDA/notebook dan menyimpan file CSV.")
        return pd.DataFrame()

    # Konversi kolom kategori
    # Menggunakan kategori lengkap untuk visualisasi tren bulanan
    df['mnth'] = pd.Categorical(df['mnth'], categories=
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        ordered=True)
    
    df['season'] = df['season'].astype('category')
    df['yr'] = df['yr'].astype('category')
    df['weekday'] = pd.Categorical(df['weekday'], categories=
        ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], ordered=True)
    df['workingday'] = df['workingday'].astype('category')
    df['weathersit'] = df['weathersit'].astype('category')
    
    return df

dataset = load_and_clean_data()

# Cek jika data gagal dimuat, hentikan eksekusi
if dataset.empty:
    st.stop()


# --- Sidebar dan Filter ---
st.sidebar.header('🚲 Bike Sharing Analysis')
with st.sidebar:
    st.write('Dashboard ini menyajikan hasil analisis tren dan faktor penyewaan sepeda pada tahun 2011-2012.')
    
    # Filter Tahun (untuk contoh jika ingin memfilter visualisasi, tapi di sini kita tampilkan semua)
    st.info("Visualisasi utama menampilkan perbandingan antar tahun (2011 vs 2012).")
    
# --- Judul Utama ---
st.title('🚴‍♂️ Tren & Faktor Pengaruh Penyewaan Sepeda')
st.caption('Analisis Data Bike Sharing Tahun 2011-2012')

# -------------------------------------------------------------
## 💡 Ikhtisar Data (Key Metrics)

st.subheader("💡 Ikhtisar Data")

col1, col2, col3 = st.columns(3)

total_rentals = dataset['cnt'].sum()
avg_daily_rentals = dataset['cnt'].mean()
registered_percent = (dataset['registered'].sum() / total_rentals) * 100

with col1:
    st.metric("Total Seluruh Penyewaan", f"{total_rentals:,}".replace(",", "."))

with col2:
    st.metric("Rata-rata Penyewaan Harian", f"{avg_daily_rentals:,.2f}".replace(",", "."))

with col3:
    st.metric("Persentase Penyewa Terdaftar", f"{registered_percent:.2f}%")

st.divider()

# -------------------------------------------------------------
## 📈 Tren Penggunaan Sepeda Tahunan

st.subheader('📈 Tren Jumlah Pengguna Sepeda (2011 vs 2012)')

# Hitung rata-rata bulanan per tahun
monthly_counts = dataset.groupby(by=["mnth", "yr"]).agg({"cnt": "mean"}).reset_index()

fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.lineplot(
    data=monthly_counts,
    x="mnth",
    y="cnt",
    hue="yr",
    palette="viridis",
    marker="o",
    ax=ax1
)

ax1.set_title("Rata-rata Penyewaan Sepeda Per Bulan", fontsize=16)
ax1.set_xlabel("Bulan")
ax1.set_ylabel("Rata-rata Jumlah Penyewa")
ax1.legend(title="Tahun", loc="upper right")
plt.xticks(rotation=45)
st.pyplot(fig1)

st.divider()

# -------------------------------------------------------------
## 📊 Faktor-Faktor Kunci

col_viz_2, col_viz_3 = st.columns(2)

with col_viz_2:
    st.subheader('🍁 Pengaruh Musim Terhadap Penyewaan')
    season_pattern = dataset.groupby('season')[['registered', 'casual']].sum().reset_index()

    # Ubah data ke format panjang untuk seaborn barplot
    season_melted = season_pattern.melt(id_vars='season', var_name='Type', value_name='Count')
    
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.barplot(
        x='season', 
        y='Count', 
        hue='Type', 
        data=season_melted, 
        palette=['#4c72b0', '#55a868'], # Registered (Biru) dan Casual (Hijau)
        ax=ax2
    )
    
    ax2.set_title("Total Penyewaan (Terdaftar vs Kasual) per Musim")
    ax2.set_xlabel(None)
    ax2.set_ylabel("Total Penyewaan")
    ax2.legend(title='Jenis Penyewa')
    plt.xticks(rotation=0)
    st.pyplot(fig2)

with col_viz_3:
    st.subheader('🌧️ Pengaruh Cuaca Terhadap Penyewaan')
    
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    # Menggunakan palet yang menyiratkan baik (Clear) dan buruk (Rain)
    sns.barplot(
        x='weathersit',
        y='cnt',
        data=dataset,
        palette=['#FFD700', '#DAA520', '#A9A9A9'],
        errorbar=None, 
        ax=ax3
    )
    ax3.set_title("Rata-rata Penyewaan per Kondisi Cuaca")
    ax3.set_xlabel(None)
    ax3.set_ylabel("Rata-rata Penyewaan")
    plt.xticks(rotation=0)
    st.pyplot(fig3)

st.divider()

# -------------------------------------------------------------
## 🗓️ Pola Penyewaan Harian

col_viz_4, col_viz_5 = st.columns(2)

with col_viz_4:
    st.subheader('📅 Persebaran Rata-rata Penyewaan per Hari')
    
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    # Menggunakan order yang sudah didefinisikan di atas (Mon-Sun)
    sns.barplot(
        x='weekday',
        y='cnt',
        data=dataset,
        palette='Spectral',
        errorbar=None,
        ax=ax4
    )

    ax4.set_title("Rata-rata Penyewaan per Hari dalam Seminggu")
    ax4.set_xlabel(None)
    ax4.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig4)

with col_viz_5:
    st.subheader('⚖️ Perbandingan Hari Kerja vs Hari Libur')
    
    fig5, ax5 = plt.subplots(figsize=(6, 4))
    sns.barplot(
        x='workingday',
        y='cnt',
        data=dataset,
        palette=['#f44336','#4CAF50'], # Merah untuk Holiday, Hijau untuk Workingday
        errorbar=None,
        ax=ax5
    )

    ax5.set_title("Rata-rata Penyewaan: Hari Libur vs Hari Kerja")
    ax5.set_xlabel(None)
    ax5.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig5)

st.divider()

# -------------------------------------------------------------
## ⭐ Kesimpulan Utama dari Analisis

st.subheader("📝 Ringkasan Hasil Analisis")
with st.expander("Klik untuk melihat kesimpulan detail"):
    st.write(
        """
        ### Key Insight
        
        1. **Pertumbuhan tahunan yang kuat**:
           - **Tahun 2012** menunjukkan peningkatan signifikan dalam penyewaan dibandingkan 2011 yang mengindikasikan pertumbuhan bisnis yang sehat.
           - Puncak penggunaan bergeser ke **September** pada 2012.

        2. **Musim gugur adalah puncak bisnis**:
           - **Musim Gugur (Fall)** mencatat total penyewaan tertinggi.
           - **Musim Semi (Springer)** menunjukkan angka terendah yang kemungkinan disebabkan oleh transisi cuaca yang tidak menentu.

        3. **Cuaca cerah mendorong penyewaan**:
           - Rata-rata penyewaan tertinggi terjadi saat **Cuaca Cerah/Sedikit Berawan**.
           - Penyewaan menurun drastis saat **Hujan Ringan/Salju** yang menunjukkan sensitivitas terhadap kondisi cuaca buruk.

        4. **Penyewaan didominasi saat hari kerja**:
           - Rata-rata penyewaan harian tertinggi terjadi pada hari **Kamis (Thu)** dan **Jumat (Fri)**.
           - Secara keseluruhan, **Hari Kerja** memiliki rata-rata penyewaan yang lebih tinggi, hal ini menunjukkan mayoritas pengguna adalah komuter (diperkuat oleh data penyewa Registered yang tinggi).
        """
    )

st.caption("Dashboard dibuat oleh: Muhammad Muthi' Nuritzan | Dicoding ID: nuritzan")
