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
            st.session_state.data = json.load(f)
        st.success("📂 Draft berhasil dimuat!")

# === Sidebar ===
with st.sidebar:
    st.markdown("## 📤 Upload Template Awal")
    uploaded = st.file_uploader("Pilih file .docx (CV/Yayasan)", type=["docx"])
    if uploaded:
        parsed = parse_docx_template(uploaded)
        st.session_state.data.update(parsed)
        st.success("✅ Data awal berhasil dimuat dari template!")

    if st.button("💾 Simpan Draft"):
        save_draft()
    if st.button("📂 Muat Draft Lama"):
        load_draft()

# === TABs ===
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📘 Umum", "🏢 Alamat", "👥 Pengurus", "💰 Modal", "📚 KBLI", "📄 Export"
])

# === TAB 1: UMUM ===
with tab1:
    st.text_input("Jenis Badan Hukum", key="jenis_badan")
    st.text_input("Nama Badan Hukum", key="nama_badan")
    st.date_input("Tanggal Akta", key="tanggal_akta", value=datetime.strptime(st.session_state.data["tanggal_akta"], "%Y-%m-%d"))
    st.text_input("Jam Akta", key="jam_akta")
    st.text_input("Nama Notaris", key="nama_notaris")

# === TAB 2: ALAMAT ===
with tab2:
    st.text_area("Alamat Lengkap", key="alamat")
    st.text_area("Maksud & Tujuan Usaha", key="bidang_usaha")

# === TAB 3: PENGURUS ===
with tab3:
    st.markdown("### Struktur Pengurus")
    for i, p in enumerate(st.session_state.data["pengurus_list"]):
        st.session_state.data["pengurus_list"][i]["jabatan"] = st.text_input(f"Jabatan #{i+1}", p["jabatan"], key=f"pj{i}")
        st.session_state.data["pengurus_list"][i]["nama"] = st.text_input(f"Nama #{i+1}", p["nama"], key=f"pn{i}")
        st.session_state.data["pengurus_list"][i]["nik"] = st.text_input(f"NIK #{i+1}", p["nik"], key=f"pnik{i}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Tambah Pengurus"):
            st.session_state.data["pengurus_list"].append({"jabatan": "", "nama": "", "nik": ""})
    with col2:
        if st.button("🗑 Hapus Terakhir") and st.session_state.data["pengurus_list"]:
            st.session_state.data["pengurus_list"].pop()

# === TAB 4: MODAL ===
with tab4:
    st.markdown("### Modal / Kekayaan Awal")
    for i, m in enumerate(st.session_state.data["modal_list"]):
        st.session_state.data["modal_list"][i]["nama"] = st.text_input(f"Nama Penyetor #{i+1}", m["nama"], key=f"mn{i}")
        st.session_state.data["modal_list"][i]["peran"] = st.text_input(f"Peran #{i+1}", m["peran"], key=f"mp{i}")
        st.session_state.data["modal_list"][i]["jumlah"] = st.number_input(f"Jumlah #{i+1}", value=m["jumlah"], key=f"mj{i}")
        st.session_state.data["modal_list"][i]["jenis"] = st.text_input(f"Jenis Modal #{i+1}", m["jenis"], key=f"mjns{i}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Tambah Modal"):
            st.session_state.data["modal_list"].append({"nama": "", "peran": "", "jumlah": 0, "jenis": ""})
    with col2:
        if st.button("🗑 Hapus Modal Terakhir") and st.session_state.data["modal_list"]:
            st.session_state.data["modal_list"].pop()

# === TAB 5: KBLI ===
with tab5:
    st.markdown("### Klasifikasi KBLI")
    for i, k in enumerate(st.session_state.data["kbli_list"]):
        st.session_state.data["kbli_list"][i]["kode"] = st.text_input(f"Kode KBLI #{i+1}", k["kode"], key=f"kk{i}")
        st.session_state.data["kbli_list"][i]["judul"] = st.text_input(f"Uraian KBLI #{i+1}", k["judul"], key=f"kj{i}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Tambah KBLI"):
            st.session_state.data["kbli_list"].append({"kode": "", "judul": ""})
    with col2:
        if st.button("🗑 Hapus KBLI Terakhir") and st.session_state.data["kbli_list"]:
            st.session_state.data["kbli_list"].pop()

# === TAB 6: EXPORT ===
with tab6:
    st.markdown("### 📄 Buat Dokumen Akta")
    template_map = {
        "CV": "template_cv.docx",
        "Yayasan": "template_yayasan.docx",
        "PT": "template_pt.docx"
    }
    jenis = st.session_state.data["jenis_badan"]
    template_file = template_map.get(jenis)

    if st.button("📄 Generate DOCX"):
        if not os.path.exists(template_file):
            st.error(f"Template tidak ditemukan: {template_file}")
        else:
            doc = DocxTemplate(template_file)
            doc.render(st.session_state.data)
            filename = f"akta_{jenis.lower()}_{st.session_state.data['nama_badan'].replace(' ', '_')}.docx"
            doc.save(filename)
            with open(filename, "rb") as f:
                st.download_button("📥 Download Akta", f, file_name=filename)
