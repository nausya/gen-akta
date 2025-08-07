import streamlit as st
from docxtpl import DocxTemplate
from datetime import datetime
import json
import os
import streamlit.components.v1 as components

st.set_page_config(page_title="Akta Notaris Dinamis", layout="wide")
st.title("📄 Aplikasi Akta Pendirian Badan Hukum")

DATA_FILE = "draft_data.json"

# Inisialisasi state
if "data" not in st.session_state:
    st.session_state.data = {
        "jenis_badan": "CV",
        "nama_badan": "",
        "alamat": "",
        "bidang_usaha": "",
        "nomor_akta": "",
        "tanggal_akta": str(datetime.today().date()),
        "jam_akta": "",
        "nama_notaris": "",
        "pengurus_list": []
    }

# Fungsi simpan & muat draft
def save_draft():
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.data, f)
    st.success("Draft berhasil disimpan!")

def load_draft():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            st.session_state.data = json.load(f)
        st.success("Draft berhasil dimuat!")

# TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📘 Umum", 
    "🏢 Alamat & Tujuan", 
    "👤 Kepengurusan", 
    "📄 Export", 
    "📚 Referensi KBLI"
])

# === Tab 1: Umum ===
with tab1:
    st.selectbox("Pilih Jenis Badan Hukum", ["CV", "PT", "Yayasan"], 
        index=["CV", "PT", "Yayasan"].index(st.session_state.data["jenis_badan"]), 
        key="jenis_badan")
    st.text_input("Nama Badan Hukum", key="nama_badan")
    st.text_input("Nomor Akta", key="nomor_akta")
    st.date_input("Tanggal Akta", key="tanggal_akta", 
        value=datetime.strptime(st.session_state.data["tanggal_akta"], "%Y-%m-%d"))
    st.text_input("Jam Akta", key="jam_akta")
    st.text_input("Nama Notaris", key="nama_notaris")

    col1, col2 = st.columns(2)
    with col1:
        st.button("💾 Simpan Draft", on_click=save_draft)
    with col2:
        st.button("📂 Muat Draft", on_click=load_draft)

# === Tab 2: Alamat & Tujuan ===
with tab2:
    st.text_area("Alamat Badan Hukum", key="alamat")
    st.text_area("Bidang Usaha / Maksud dan Tujuan", key="bidang_usaha")

# === Tab 3: Kepengurusan ===
with tab3:
    st.markdown("### Struktur Kepengurusan")
    for i, org in enumerate(st.session_state.data["pengurus_list"]):
        st.session_state.data["pengurus_list"][i]["jabatan"] = st.text_input(f"Jabatan #{i+1}", value=org["jabatan"], key=f"jabatan_{i}")
        st.session_state.data["pengurus_list"][i]["nama"] = st.text_input(f"Nama #{i+1}", value=org["nama"], key=f"nama_{i}")
        st.session_state.data["pengurus_list"][i]["nik"] = st.text_input(f"NIK #{i+1}", value=org["nik"], key=f"nik_{i}")
    
    col1, col2 = st
