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

# Fungsi load dan save draft
def load_draft():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            st.session_state.data = json.load(f)
        st.success("Draft berhasil dimuat!")

def save_draft():
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.data, f)
    st.success("Draft berhasil disimpan!")

# Jenis badan hukum
jenis = st.selectbox("Pilih Jenis Badan Hukum", ["CV", "PT", "Yayasan"], 
    index=["CV", "PT", "Yayasan"].index(st.session_state.data["jenis_badan"]))
st.session_state.data["jenis_badan"] = jenis

# Form umum
st.text_input("Nama CV / PT / Yayasan", key="nama_badan")
st.text_area("Alamat", key="alamat")
st.text_area("Bidang Usaha / Maksud Tujuan", key="bidang_usaha")
st.text_input("Nomor Akta", key="nomor_akta")
st.date_input("Tanggal Akta", key="tanggal_akta", value=datetime.strptime(st.session_state.data["tanggal_akta"], "%Y-%m-%d"))
st.text_input("Jam Akta", key="jam_akta")
st.text_input("Nama Notaris", key="nama_notaris")

# Kepengurusan dinamis
st.markdown("### 👤 Struktur Kepengurusan")
for i, org in enumerate(st.session_state.data["pengurus_list"]):
    st.session_state.data["pengurus_list"][i]["jabatan"] = st.text_input(f"Jabatan #{i+1}", value=org["jabatan"], key=f"jabatan_{i}")
    st.session_state.data["pengurus_list"][i]["nama"] = st.text_input(f"Nama #{i+1}", value=org["nama"], key=f"nama_{i}")
    st.session_state.data["pengurus_list"][i]["nik"] = st.text_input(f"NIK #{i+1}", value=org["nik"], key=f"nik_{i}")

if st.button("➕ Tambah Pengurus"):
    st.session_state.data["pengurus_list"].append({"jabatan": "", "nama": "", "nik": ""})

if st.button("🗑 Hapus Pengurus Terakhir") and st.session_state.data["pengurus_list"]:
    st.session_state.data["pengurus_list"].pop()

# Simpan & muat draft
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.button("💾 Simpan Draft", on_click=save_draft)
with col2:
    st.button("📂 Muat Draft", on_click=load_draft)

# Template mapping
template_map = {
    "CV": "template_cv.docx",
    "PT": "template_pt.docx",
    "Yayasan": "template_yayasan.docx"
}

# Generate DOCX
st.markdown("---")
if st.button("📄 Generate Dokumen Akta"):
    template_file = template_map.get(jenis)
    if not os.path.exists(template_file):
        st.error(f"Template untuk {jenis} tidak ditemukan: {template_file}")
    else:
        doc = DocxTemplate(template_file)
        context = st.session_state.data
        doc.render(context)

        filename = f"akta_{jenis.lower()}_{context['nama_badan'].replace(' ', '_')}.docx"
        doc.save(filename)

        with open(filename, "rb") as f:
            st.download_button("📥 Download Akta", f, file_name=filename)
