import streamlit as st
from docxtpl import DocxTemplate
from datetime import datetime
import json
import os

st.set_page_config(page_title="Akta Notaris Dinamis", layout="centered")
st.title("📄 Aplikasi Akta Pendirian Badan Hukum")

DATA_FILE = "draft_data.json"

# Inisialisasi session_state
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

# Load draft
def load_draft():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            st.session_state.data = json.load(f)
        st.success("Draft berhasil dimuat!")

# Save draft
def save_draft():
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.data, f)
    st.success("Draft berhasil disim
