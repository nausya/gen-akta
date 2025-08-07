import streamlit as st
from docxtpl import DocxTemplate
from datetime import datetime
import json
import os
from doc_reader import parse_docx_template

st.set_page_config(page_title="Akta Notaris Dinamis", layout="wide")
st.title("📄 Aplikasi Akta Pendirian Badan Hukum")

DATA_FILE = "draft_data.json"

# Inisialisasi default state
if "data" not in st.session_state:
    st.session_state.data = {
        "jenis_badan": "",
        "nama_badan": "",
        "alamat": "",
        "bidang_usaha": "",
        "tanggal_akta": str(datetime.today().date()),
        "jam_akta": "",
        "nama_notaris": "",
        "pengurus_list": [],
        "modal_list": [],
        "kbli_list": []
    }

# Fungsi Simpan/Muat Draft
def save_draft():
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.data, f)
    st.success("✅ Draft disimpan!")

def load_draft():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
