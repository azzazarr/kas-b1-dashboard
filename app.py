import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. KONFIGURASI HALAMAN WEB
st.set_page_config(page_title="Dashboard Kas Kelas B1", layout="wide")

# ========================================================
#   MENU SAMPING (SIDEBAR) - FITUR SCAN QRIS
# ========================================================
st.sidebar.header("💳 Pembayaran Kas via QRIS")
st.sidebar.markdown("Pindai QRIS di bawah ini untuk membayar iuran kas kelas B1:")

# Menampilkan QRIS jika file fotonya diupload
qris_file = "qris_kelas.png"
if os.path.exists(qris_file):
    st.sidebar.image(qris_file, caption="QRIS Resmi Kas Kelas B1", use_container_width=True)
else:
    st.sidebar.warning("⚠️ File 'qris_kelas.png' belum ditemukan di GitHub.")
    st.sidebar.info("💡 Tip: Upload foto QRIS Anda ke GitHub dengan nama 'qris_kelas.png' agar muncul di sini.")

st.sidebar.markdown("""
**Cara Pembayaran:**
1. Scan QRIS menggunakan E-Wallet atau Mobile Banking Anda.
2. Masukkan nominal iuran kas yang ditentukan.
3. Kirim bukti transfer ke Bendahara Kelas untuk diperbarui di Excel!
""")
st.sidebar.markdown("---")

# ========================================================
#   HALAMAN UTAMA - DASHBOARD KAS KELAS B1
# ========================================================
st.title("📊 Web Dashboard Kas Otomatis - Kelas B1")
st.markdown("Rekapitulasi Arus Kas Masuk dan Keluar Secara Real-Time.")
st.markdown("---")

# Fungsi membaca data dari Excel
@st.cache_data(ttl=10)
def load_data():
    df = pd.read_excel("Kas_Kelas(B1).xlsx", sheet_name="Data_Kas")
    return df

try:
    df = load_data()

    # Logika Hitung Total Otomatis
    total_masuk = df[df['Jenis'] == 'Pemasukan']['Jumlah'].sum()
    total_keluar = df[df['Jenis'] == 'Pengeluaran']['Jumlah'].sum()
    sisa_saldo = total_masuk - total_keluar

    # Tampilan Kotak Ringkasan Utama (KPI)
    col1, col2, col3 = st.columns(3)
    col1.metric(label="🟢 TOTAL IURAN MASUK", value=f"Rp {total_masuk:,.0f}")
    col2.metric(label="🔴 TOTAL PENGELUARAN", value=f"Rp {total_keluar:,.0f}")
    col3.metric(label="🔵 SISA SALDO KAS AKTIF", value=f"Rp {sisa_saldo:,.0f}")

    st.markdown("---")

    # Pembagian Layout: Kiri Grafik, Kanan Tabel Data
    col_grafik, col_tabel = st.columns([1, 1])

    with col_grafik:
        st.subheader("📈 Tampilan Visual Arus Kas")
        df_chart = df.groupby('Jenis')['Jumlah'].sum().reset_index()
        fig = px.bar(df_chart, x='Jenis', y='Jumlah', color='Jenis',
                     color_discrete_map={'Pemasukan': '#2E7D32', 'Pengeluaran': '#C62828'})
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("📊 Pembagian Kas per Kategori")
        df_cat = df.groupby(['Kategori', 'Jenis'])['Jumlah'].sum().reset_index()
        fig_cat = px.bar(df_cat, x='Kategori', y='Jumlah', color='Jenis', barmode='group',
                         color_discrete_map={'Pemasukan': '#2E7D32', 'Pengeluaran': '#C62828'})
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_tabel:
        st.subheader("📋 Detail Log Riwayat Transaksi")
        st.dataframe(df[['No', 'Tanggal', 'Keterangan', 'Kategori', 'Jenis', 'Jumlah', 'Saldo Berjalan']], use_container_width=True)

except Exception as e:
    st.error("Gagal membaca file. Pastikan file 'Kas_Kelas(B1).xlsx' sudah diupload ke GitHub Anda dengan struktur kolom yang benar!")