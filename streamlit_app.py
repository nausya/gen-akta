import streamlit as st
from docxtpl import DocxTemplate
from datetime import datetime
import json
import os

st.set_page_config(page_title="Akta Notaris Dinamis", layout="wide")
st.title("📄 Aplikasi Akta Pendirian Badan Hukum")

DATA_FILE = "draft_data.json"

# Inisialisasi default state
if "data" not in st.session_state:
    st.session_state.data = {
        "jenis_badan": "",
        "nomor_akta": "",
        "tanggal_akta": str(datetime.today().date()),
        "jam_akta": "",
        "nama_badan": "",
        "alamat_badan": "",
        "para_pihak": [],
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

# Sidebar untuk simpan/muat draft
with st.sidebar:
    st.markdown("## 💾 Draft")
    if st.button("📂 Muat Draft Lama"):
        load_draft()
    if st.button("💾 Simpan Draft"):
        save_draft()

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📘 Umum", "🏢 Alamat", "👥 Para Pihak", "💰 Modal", "📚 KBLI", "📄 Export"
])

with tab1:
    st.subheader("Informasi Umum")
    st.session_state.data["jenis_badan"] = st.selectbox("Jenis Badan Hukum", ["", "CV", "Yayasan"], index=0)
    st.session_state.data["nomor_akta"] = st.text_input("Nomor Akta", value=st.session_state.data["nomor_akta"])
    st.session_state.data["tanggal_akta"] = str(st.date_input("Tanggal Akta", value=datetime.strptime(st.session_state.data["tanggal_akta"], "%Y-%m-%d")))
    st.session_state.data["jam_akta"] = st.text_input("Jam Akta (contoh: 19.04 WIB)", value=st.session_state.data["jam_akta"])

with tab2:
    st.subheader("Alamat Badan Hukum")
    st.session_state.data["nama_badan"] = st.text_input("Nama CV / Yayasan", value=st.session_state.data["nama_badan"])
    st.session_state.data["alamat_badan"] = st.text_area("Alamat Lengkap", value=st.session_state.data["alamat_badan"])

with tab3:
    st.subheader("Para Pihak / Pengurus")
    for i, pihak in enumerate(st.session_state.data["para_pihak"]):
        st.session_state.data["para_pihak"][i]["nama"] = st.text_input(f"Nama Pihak #{i+1}", value=pihak["nama"], key=f"pn{i}")
        st.session_state.data["para_pihak"][i]["ttl"] = st.text_input(f"Tempat & Tanggal Lahir #{i+1}", value=pihak["ttl"], key=f"pttl{i}")
        st.session_state.data["para_pihak"][i]["jabatan"] = st.text_input(f"Jabatan #{i+1}", value=pihak.get("jabatan", ""), key=f"pj{i}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Tambah Pihak"):
            st.session_state.data["para_pihak"].append({"nama": "", "ttl": "", "jabatan": ""})
    with col2:
        if st.button("🗑 Hapus Pihak Terakhir") and st.session_state.data["para_pihak"]:
            st.session_state.data["para_pihak"].pop()

with tab4:
    st.subheader("Modal Awal / Kekayaan")
    for i, m in enumerate(st.session_state.data["modal_list"]):
        st.session_state.data["modal_list"][i]["nama"] = st.text_input(f"Nama Penyetor #{i+1}", m["nama"], key=f"mn{i}")
        st.session_state.data["modal_list"][i]["jumlah"] = st.text_input(f"Jumlah #{i+1}", m["jumlah"], key=f"mj{i}")
        st.session_state.data["modal_list"][i]["jenis"] = st.text_input(f"Jenis Modal #{i+1}", m["jenis"], key=f"mjns{i}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Tambah Modal"):
            st.session_state.data["modal_list"].append({"nama": "", "jumlah": "", "jenis": ""})
    with col2:
        if st.button("🗑 Hapus Modal Terakhir") and st.session_state.data["modal_list"]:
            st.session_state.data["modal_list"].pop()

with tab5:
    st.subheader("Klasifikasi KBLI")
    for i, k in enumerate(st.session_state.data["kbli_list"]):
        st.session_state.data["kbli_list"][i]["kode"] = st.text_input(f"Kode KBLI #{i+1}", k["kode"], key=f"kk{i}")
        st.session_state.data["kbli_list"][i]["judul"] = st.text_area(f"Uraian KBLI #{i+1}", k["judul"], key=f"kj{i}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Tambah KBLI"):
            st.session_state.data["kbli_list"].append({"kode": "", "judul": ""})
    with col2:
        if st.button("🗑 Hapus KBLI Terakhir") and st.session_state.data["kbli_list"]:
            st.session_state.data["kbli_list"].pop()

with tab6:
    st.subheader("Export Dokumen")
    jenis = st.session_state.data["jenis_badan"]
    template_map = {
        "CV": "template_cv.docx",
        "Yayasan": "template_yayasan.docx"
    }
    template_file = template_map.get(jenis)

    if st.button("📄 Generate DOCX"):
        if not jenis:
            st.warning("⚠️ Silakan isi Jenis Badan Hukum di Tab Umum.")
        elif not st.session_state.data["para_pihak"]:
            st.warning("⚠️ Data Para Pihak kosong, silakan isi di Tab Pihak.")
        elif not st.session_state.data["modal_list"]:
            st.warning("⚠️ Data Modal kosong, silakan isi di Tab Modal.")
        elif not st.session_state.data["kbli_list"]:
            st.warning("⚠️ Data KBLI kosong, silakan isi di Tab KBLI.")
        else:
            doc = DocxTemplate(template_file)
            doc.render(st.session_state.data)
            filename = f"akta_{jenis.lower()}_{st.session_state.data['nama_badan'].replace(' ', '_')}.docx"
            doc.save(filename)
            with open(filename, "rb") as f:
                st.download_button("📥 Download Akta", f, file_name=filename)

