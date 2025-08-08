import streamlit as st
from datetime import datetime
from docxtpl import DocxTemplate
import os
import json

st.set_page_config(page_title="Aplikasi Dukungan Kantor Notaris", layout="wide")

# --- Inisialisasi session state ---
if "data" not in st.session_state:
    st.session_state.data = {
        "jenis_badan": "",
        "nomor_akta": "",
        "tanggal_akta": str(datetime.today().date()),
        "jam_akta": "",
        "nama_badan": "",
        "alamat": "",
        "para_pihak": [],
        "modal": [],
        "kbli_list": [],
        "nama_notaris": "UTAMI RAHMAYANTI, S.H.,M.Kn",
        "logo": "assets/logo_dummy.png"  # fallback logo dummy
    }

DATA_FILE = "draft_data.json"

# --- Fungsi Simpan & Muat Draft ---
def save_draft():
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.data, f)
    st.success("✅ Draft berhasil disimpan")

def load_draft():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            st.session_state.data = json.load(f)
        st.success("📂 Draft berhasil dimuat")
    else:
        st.warning("⚠️ Belum ada draft yang tersimpan")

# === Sidebar ===
try:
    st.sidebar.image(st.session_state.data["logo"], width=200)
except:
    st.sidebar.image("logo.png", width=200)

st.sidebar.markdown("##")
menu = st.sidebar.radio("Menu", ["Pembuatan Akta", "Persuratan", "Profil Notaris", "Admin Web"])

# === Header ===
st.markdown(f"""
    <h4 style='text-align:center; color:#0546b3'>{st.session_state.data['nama_notaris'].upper()} - NOTARIS KABUPATEN CIREBON</h4>
    <h2 style='text-align:center;'>🧾 Aplikasi Dukungan Kantor Notaris</h2>
    """, unsafe_allow_html=True)

# === Menu: Pembuatan Akta ===
if menu == "Pembuatan Akta":
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📘 Umum", "🏢 Alamat", "👥 Para Pihak", "💰 Modal", "📚 KBLI", "📄 Export"
    ])

    with tab1:
        st.subheader("Informasi Umum")
        st.session_state.data["jenis_badan"] = st.selectbox("Jenis Badan Hukum", ["CV", "PT", "Yayasan"], index=0 if st.session_state.data["jenis_badan"] == "" else ["CV", "PT", "Yayasan"].index(st.session_state.data["jenis_badan"]))
        st.session_state.data["nomor_akta"] = st.text_input("Nomor Akta", value=st.session_state.data["nomor_akta"])
        st.session_state.data["tanggal_akta"] = str(st.date_input("Tanggal Akta", value=datetime.strptime(st.session_state.data["tanggal_akta"], "%Y-%m-%d")))
        st.session_state.data["jam_akta"] = st.text_input("Jam Akta (contoh: 19.04 WIB)", value=st.session_state.data["jam_akta"])

    with tab2:
        st.subheader("Alamat Badan Hukum")
        st.session_state.data["nama_badan"] = st.text_input("Nama CV/PT/Yayasan", value=st.session_state.data["nama_badan"])
        st.session_state.data["alamat"] = st.text_area("Alamat CV/PT/Yayasan", value=st.session_state.data["alamat"])

    with tab3:
        st.subheader("Data Para Pihak")
        for i, pihak in enumerate(st.session_state.data["para_pihak"]):
            st.session_state.data["para_pihak"][i]["nama"] = st.text_input(f"Nama Pihak {i+1}", pihak["nama"], key=f"nama{i}")
            st.session_state.data["para_pihak"][i]["ttl"] = st.text_input(f"Tempat & Tanggal Lahir Pihak {i+1}", pihak["ttl"], key=f"ttl{i}")
            st.session_state.data["para_pihak"][i]["pekerjaan"] = st.text_input(f"Pekerjaan Pihak {i+1}", pihak["pekerjaan"], key=f"kerja{i}")
        if st.button("➕ Tambah Pihak"):
            st.session_state.data["para_pihak"].append({"nama": "", "ttl": "", "pekerjaan": ""})

    with tab4:
        st.subheader("Data Modal")
        for i, modal in enumerate(st.session_state.data["modal"]):
            st.session_state.data["modal"][i]["nama"] = st.text_input(f"Nama Penyetor {i+1}", modal["nama"], key=f"mn{i}")
            st.session_state.data["modal"][i]["jumlah"] = st.number_input(f"Jumlah Modal {i+1}", value=modal["jumlah"], key=f"mj{i}")
        if st.button("➕ Tambah Modal"):
            st.session_state.data["modal"].append({"nama": "", "jumlah": 0})

    with tab5:
        st.subheader("Data KBLI")
        for i, kbli in enumerate(st.session_state.data["kbli_list"]):
            st.session_state.data["kbli_list"][i]["kode"] = st.text_input(f"Kode KBLI #{i+1}", kbli["kode"], key=f"kk{i}")
            st.session_state.data["kbli_list"][i]["judul"] = st.text_area(f"Uraian KBLI #{i+1}", kbli["judul"], key=f"kj{i}")
        if st.button("➕ Tambah KBLI"):
            st.session_state.data["kbli_list"].append({"kode": "", "judul": ""})

    with tab6:
        st.subheader("Export Dokumen")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Simpan Draft"):
                save_draft()
        with col2:
            if st.button("📂 Muat Draft Lama"):
                load_draft()

        st.markdown("---")
        if st.button("📄 Generate DOCX"):
            template_map = {
                "CV": "template_cv.docx",
                "PT": "template_pt.docx",
                "Yayasan": "template_yayasan.docx"
            }
            template_path = template_map.get(st.session_state.data["jenis_badan"], None)

            if not template_path or not os.path.exists(template_path):
                st.error("⚠️ Template tidak ditemukan")
            else:
                try:
                    doc = DocxTemplate(template_path)
                    doc.render(st.session_state.data)
                    output_name = f"akta_{st.session_state.data['jenis_badan'].lower()}_{st.session_state.data['nama_badan'].replace(' ', '_')}.docx"
                    doc.save(output_name)
                    with open(output_name, "rb") as f:
                        st.download_button("📥 Download Akta", f, file_name=output_name)
                except Exception as e:
                    st.error(f"❌ Gagal generate dokumen: {e}")

elif menu == "Profil Notaris":
    st.subheader("Profil Notaris")
    uploaded_logo = st.file_uploader("Upload Logo Notaris", type=["png", "jpg", "jpeg"])
    if uploaded_logo:
        with open("uploaded_logo.png", "wb") as f:
            f.write(uploaded_logo.read())
        st.session_state.data["logo"] = "uploaded_logo.png"

    st.session_state.data["nama_notaris"] = st.text_input("Nama Notaris", value=st.session_state.data["nama_notaris"])
    st.success("Perubahan disimpan otomatis.")

elif menu == "Admin Web":
    st.subheader("Pengaturan Admin Web")
    st.info("🛠️ Fitur ini dalam pengembangan lebih lanjut.")
