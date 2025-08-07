import streamlit as st
from docxtpl import DocxTemplate
from datetime import datetime

# Inisialisasi session_state
if "info" not in st.session_state:
    st.session_state.info = {
        "nomor_akta": "",
        "tanggal_akta": datetime.today(),
        "jam_akta": "",
        "nama_cv": "",
        "alamat_cv": "",
        "bidang_usaha": "",
        "modal_total_terbilang": "",
        "nama_notaris": ""
    }

if "pihak" not in st.session_state:
    st.session_state.pihak = []

if "saksi" not in st.session_state:
    st.session_state.saksi = []

# Tabs menu
tabs = st.tabs(["📄 Informasi Akta", "👥 Para Pihak", "🏢 Perseroan", "🖋 Saksi", "📑 Generate"])

# Tab Informasi Akta
with tabs[0]:
    st.subheader("Informasi Akta")
    st.session_state.info["nomor_akta"] = st.text_input("Nomor Akta", st.session_state.info["nomor_akta"])
    st.session_state.info["tanggal_akta"] = st.date_input("Tanggal Akta", st.session_state.info["tanggal_akta"])
    st.session_state.info["jam_akta"] = st.text_input("Jam Akta", st.session_state.info["jam_akta"])
    st.session_state.info["nama_cv"] = st.text_input("Nama CV", st.session_state.info["nama_cv"])
    st.session_state.info["alamat_cv"] = st.text_area("Alamat CV", st.session_state.info["alamat_cv"])

# Tab Para Pihak (Dinamis)
with tabs[1]:
    st.subheader("Daftar Para Pihak")
    for i, pihak in enumerate(st.session_state.pihak):
        st.text_input(f"Nama Pihak {i+1}", pihak.get("nama",""), key=f"pihak_nama_{i}")
        st.text_input(f"TTL Pihak {i+1}", pihak.get("ttl",""), key=f"pihak_ttl_{i}")
        st.text_input(f"Pekerjaan Pihak {i+1}", pihak.get("pekerjaan",""), key=f"pihak_pekerjaan_{i}")
        st.text_area(f"Alamat Pihak {i+1}", pihak.get("alamat",""), key=f"pihak_alamat_{i}")
        st.text_input(f"NIK Pihak {i+1}", pihak.get("nik",""), key=f"pihak_nik_{i}")
        st.number_input(f"Modal Pihak {i+1} (Rp)", min_value=0, value=int(pihak.get("modal",0)), key=f"pihak_modal_{i}")
        st.text_input(f"Modal Pihak {i+1} (terbilang)", pihak.get("modal_terbilang",""), key=f"pihak_modal_terbilang_{i}")
        if st.button(f"❌ Hapus Pihak {i+1}"):
            st.session_state.pihak.pop(i)
            st.experimental_rerun()
    if st.button("➕ Tambah Pihak"):
        st.session_state.pihak.append({
            "nama": "", "ttl": "", "pekerjaan": "", "alamat": "",
            "nik": "", "modal": 0, "modal_terbilang": ""
        })
        st.experimental_rerun()

# Tab Perseroan
with tabs[2]:
    st.subheader("Informasi Perseroan")
    st.session_state.info["bidang_usaha"] = st.text_area("Bidang Usaha & KBLI", st.session_state.info["bidang_usaha"])
    total_modal = sum(int(st.session_state.get(f"pihak_modal_{i}",0)) for i in range(len(st.session_state.pihak)))
    st.write(f"Modal Total (otomatis): Rp. {total_modal:,}")
    st.session_state.info["modal_total_terbilang"] = st.text_input("Modal Total (terbilang)", st.session_state.info["modal_total_terbilang"])

# Tab Saksi (Dinamis)
with tabs[3]:
    st.subheader("Daftar Saksi")
    for i, saksi in enumerate(st.session_state.saksi):
        st.text_input(f"Nama Saksi {i+1}", saksi.get("nama",""), key=f"saksi_nama_{i}")
        st.text_input(f"TTL Saksi {i+1}", saksi.get("ttl",""), key=f"saksi_ttl_{i}")
        st.text_area(f"Alamat Saksi {i+1}", saksi.get("alamat",""), key=f"saksi_alamat_{i}")
        st.text_input(f"NIK Saksi {i+1}", saksi.get("nik",""), key=f"saksi_nik_{i}")
        if st.button(f"❌ Hapus Saksi {i+1}"):
            st.session_state.saksi.pop(i)
            st.experimental_rerun()
    if st.button("➕ Tambah Saksi"):
        st.session_state.saksi.append({"nama": "", "ttl": "", "alamat": "", "nik": ""})
        st.experimental_rerun()

# Tab Generate Dokumen
with tabs[4]:
    st.subheader("Generate Dokumen Akta")
    if st.button("📄 Buat Akta"):
        pihak_data = []
        for i in range(len(st.session_state.pihak)):
            pihak_data.append({
                "nama": st.session_state.get(f"pihak_nama_{i}",""),
                "ttl": st.session_state.get(f"pihak_ttl_{i}",""),
                "pekerjaan": st.session_state.get(f"pihak_pekerjaan_{i}",""),
                "alamat": st.session_state.get(f"pihak_alamat_{i}",""),
                "nik": st.session_state.get(f"pihak_nik_{i}",""),
                "modal": f"Rp. {int(st.session_state.get(f'pihak_modal_{i}',0)):,}",
                "modal_terbilang": st.session_state.get(f"pihak_modal_terbilang_{i}","")
            })

        saksi_data = []
        for i in range(len(st.session_state.saksi)):
            saksi_data.append({
                "nama": st.session_state.get(f"saksi_nama_{i}",""),
                "ttl": st.session_state.get(f"saksi_ttl_{i}",""),
                "alamat": st.session_state.get(f"saksi_alamat_{i}",""),
                "nik": st.session_state.get(f"saksi_nik_{i}","")
            })

        total_modal = sum(int(st.session_state.get(f"pihak_modal_{i}",0)) for i in range(len(pihak_data)))

        doc = DocxTemplate("akta_pendirian_cv_template.docx")
        context = {
            **st.session_state.info,
            "tanggal_akta": st.session_state.info["tanggal_akta"].strftime("%d-%m-%Y"),
            "pihak_list": pihak_data,
            "saksi_list": saksi_data,
            "modal_total": f"Rp. {total_modal:,}"
        }
        doc.render(context)
        output_path = f"akta_pendirian_cv_{st.session_state.info['nomor_akta']}.docx"
        doc.save(output_path)
        with open(output_path, "rb") as f:
            st.download_button(
                "📥 Download Akta",
                f,
                file_name=output_path,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
