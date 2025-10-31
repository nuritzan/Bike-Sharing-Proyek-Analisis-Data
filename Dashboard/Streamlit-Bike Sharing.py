import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_style('whitegrid')  # Mengubah style menjadi lebih bersih


# Fungsi untuk memuat dan membersihkan data (Data Wrangling)
# Asumsi file 'Bike_Sharing.csv' sudah dibuat dari notebook
@st.cache_data
def load_and_clean_data():
    df = pd.read_csv("Bike_Sharing.csv")

    # Konversi kolom kategori
    df['mnth'] = pd.Categorical(df['mnth'], categories=
    ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                                ordered=True)

    df['season'] = df['season'].astype('category')
    df['yr'] = df['yr'].astype('category')
    df['weekday'] = pd.Categorical(df['weekday'], categories=
    ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], ordered=True)
    df['workingday'] = df['workingday'].astype('category')
    df['weathersit'] = df['weathersit'].astype('category')

    # Perbaikan mapping bulan karena di EDA ada 12 bulan (termasuk Des)
    # Cek kategori bulan di data Anda, jika tidak ada 'Dec' maka sesuaikan
    # Jika data hanya sampai Nov, gunakan:
    # categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov']

    return df


dataset = load_and_clean_data()

# --- Sidebar dan Header ---
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

st.sidebar.header('🚲 Bike Sharing Analysis')

with st.sidebar:
    st.write('Dashboard ini menyajikan hasil analisis data penyewaan sepeda.')
    # Tambahkan filter tahun jika ingin interaktif
    selected_year = st.selectbox(
        'Pilih Tahun',
        options=dataset['yr'].unique().tolist()
    )
    filtered_data = dataset[dataset['yr'] == selected_year]

# --- Judul Utama ---
st.title('🚴‍♂️ Tren & Faktor Pengaruh Penyewaan Sepeda')
st.caption('Analisis Data Bike Sharing 2011-2012')

# --- Key Metrics (Metrik Utama) ---
st.subheader("💡 Ikhtisar Data")

col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = dataset['cnt'].sum()
    st.metric("Total Seluruh Penyewaan", f"{total_rentals:,}".replace(",", "."))

with col2:
    avg_daily_rentals = dataset['cnt'].mean()
    st.metric("Rata-rata Penyewaan Harian", f"{avg_daily_rentals:,.2f}".replace(",", "."))

with col3:
    registered_percent = (dataset['registered'].sum() / total_rentals) * 100
    st.metric("Persentase Penyewa Terdaftar", f"{registered_percent:.2f}%")

st.divider()

# --- Visualisasi 1: Tren Penggunaan Sepeda Tahunan ---
st.subheader('📈 Tren Jumlah Pengguna Sepeda (2011 vs 2012)')
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

# --- Visualisasi 2 & 3 (Musim dan Cuaca) dalam Kolom ---
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
        palette=['#4c72b0', '#55a868'],  # Warna khusus untuk Registered dan Casual
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
    sns.barplot(
        x='weathersit',
        y='cnt',
        data=dataset,
        palette=['#FFD700', '#DAA520', '#A9A9A9'],  # Palet warna yang lebih berkesan
        errorbar=None,  # Mengganti ci=None
        ax=ax3
    )
    ax3.set_title("Rata-rata Penyewaan per Kondisi Cuaca")
    ax3.set_xlabel(None)
    ax3.set_ylabel("Rata-rata Penyewaan")
    plt.xticks(rotation=0)
    st.pyplot(fig3)

st.divider()

# --- Visualisasi 4 & 5 (Hari dan Hari Kerja/Libur) dalam Kolom ---
col_viz_4, col_viz_5 = st.columns(2)

with col_viz_4:
    st.subheader('📅 Persebaran Penyewaan Sepeda per Hari')

    fig4, ax4 = plt.subplots(figsize=(6, 4))
    sns.barplot(
        x='weekday',
        y='cnt',
        data=dataset,
        order=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
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
        palette=['#f44336', '#4CAF50'],  # Warna yang kontras
        errorbar=None,
        ax=ax5
    )

    ax5.set_title("Rata-rata Penyewaan: Hari Libur vs Hari Kerja")
    ax5.set_xlabel(None)
    ax5.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig5)

st.divider()

# --- Expander Kesimpulan (Conclusion) ---
st.subheader("⭐ Kesimpulan Utama dari Analisis")
with st.expander("Klik untuk melihat kesimpulan detail"):
    st.write(
        """
        1. **Tren Tahunan**:
           - **Tahun 2012** memiliki tren penggunaan sepeda yang lebih tinggi secara signifikan dibandingkan **Tahun 2011**.
           - Puncak pengguna tertinggi pada **2012** terjadi pada **September**, menunjukkan pergeseran dari puncak **Juni** pada **2011**.

        2. **Pengaruh Musim**:
           - **Musim Gugur (Fall)** mencatat total penyewaan tertinggi.
           - Penyewaan menurun sedikit di **Musim Dingin (Winter)**, turun drastis di **Musim Semi (Springer)**, dan kemudian naik kembali di **Musim Panas (Summer)**.
           - Mayoritas penyewa adalah **Terdaftar (Registered)** di semua musim.

        3. **Pengaruh Cuaca**:
           - **Cuaca Cerah/Sedikit Berawan (Clear/Partly Cloudy)** adalah kondisi cuaca dengan rata-rata penyewaan tertinggi.
           - Cuaca **Hujan Ringan/Salju (Light Rain/Snow)** memiliki rata-rata penyewaan terendah.

        4. **Pola Harian & Hari Kerja**:
           - Rata-rata penyewaan tertinggi terjadi pada **Hari Kamis (Thu)** dan **Jumat (Fri)**.
           - Rata-rata penyewaan terendah terjadi pada **Hari Minggu (Sun)**.
           - Secara umum, **Hari Kerja (Workingday)** memiliki rata-rata penyewaan harian yang **lebih tinggi** daripada **Hari Libur (Holiday)**.
        """
    )

st.caption("By: Muhammad Muthi' Nuritzan")