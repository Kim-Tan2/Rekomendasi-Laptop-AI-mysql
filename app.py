import streamlit as st
import pandas as pd
import joblib

from db_config import load_laptop_data
from weighted_product import weighted_product

# Load model KMeans
kmeans = joblib.load('model_cluster.pkl')

st.set_page_config(page_title="Rekomendasi Laptop AI", layout="centered")
st.title("🎯 Sistem Rekomendasi Laptop Berbasis AI")

# Input preferensi pengguna
st.header("Masukkan Preferensi Anda")
harga_max = st.number_input("Harga Maksimal (Rp)", value=10000000)
ram_min = st.number_input("RAM Minimal (GB)", value=8)
prosesor_min = st.number_input("Nilai Prosesor Minimal", value=5.0)
penyimpanan_min = st.number_input("Penyimpanan Minimal (GB)", value=256)

# Ambil data laptop dari database
df = load_laptop_data()

# Filter awal berdasarkan input
df_filtered = df[(df['harga'] <= harga_max) & 
                 (df['ram'] >= ram_min) & 
                 (df['prosesor'] >= prosesor_min) & 
                 (df['penyimpanan'] >= penyimpanan_min)].copy()

if not df_filtered.empty:
    # Tambahkan cluster dari model KMeans
    fitur = df_filtered[['harga', 'ram', 'prosesor', 'penyimpanan']]
    df_filtered['cluster'] = kmeans.predict(fitur)

    # Ambil cluster mayoritas
    target_cluster = df_filtered['cluster'].mode()[0]
    df_clustered = df_filtered[df_filtered['cluster'] == target_cluster]

    # Hitung WP Score
    weights = {'harga': 0.2, 'ram': 0.25, 'prosesor': 0.3, 'penyimpanan': 0.25}
    rekomendasi = weighted_product(df_clustered, weights)

    st.success("Berikut adalah rekomendasi laptop terbaik untuk Anda:")
    st.dataframe(rekomendasi[['nama', 'harga', 'ram', 'prosesor', 'penyimpanan', 'score']])
else:
    st.warning("Tidak ada laptop yang cocok dengan preferensi Anda.")
