import streamlit as st
from docxtpl import DocxTemplate
from datetime import datetime
import os

st.title("📜 Generator Akta Pendirian CV")

with st.form("form_cv"):
    nomor_akta = st.text_input("Nomor Akta")
    tanggal_akta = st.date_input("Tanggal Akta", datetime.today())
    jam_akta = st.text_input("Jam Akta (contoh: 19.04 WIB)")
    nama_cv = st.text_input("Nama CV")
    alamat_cv = st.text_area("Alamat CV")

    nama_pihak1 = st.text_input("Nama Pihak 1")
    ttl_pihak1 = st.text_input("Tempat & Tanggal Lahir Pihak 1")
    pekerjaan_pihak1 = st.text_input("Pekerjaan Pihak 1")
    alamat_pihak1 = st.text_area("Alamat Pihak 1")
    nik_pihak1 = st.text_input("NIK Pihak 1")
    modal_pihak1 = st.number_input("Modal Pihak 1 (Rp)", min_value=0)
    modal_pihak1_terbilang = st.text_input("Modal Pihak 1 (terbilang)")

    nama_pihak2 = st.text_input("Nama Pihak 2")
    ttl_pihak2 = st.text_input("Tempat & Tanggal Lahir Pihak 2")
    pekerjaan_pihak2 = st.text_input("Pekerjaan Pihak 2")
    alamat_pihak2 = st.text_area("Alamat Pihak 2")
    nik_pihak2 = st.text_input("NIK Pihak 2")
    modal_pihak2 = st.number_input("Modal Pihak 2 (Rp)", min_value=0)
    modal_pihak2_terbilang = st.text_input("Modal Pihak 2 (terbilang)")

    bidang_usaha = st.text_area("Bidang Usaha & KBLI")
    modal_total = modal_pihak1 + modal_pihak2
    modal_total_terbilang = st.text_input("Modal Total (terbilang)")

    nama_notaris = st.text_input("Nama Notaris")
    nama_saksi1 = st.text_input("Nama Saksi 1")
    ttl_saksi1 = st.text_input("Tempat & Tanggal Lahir Saksi 1")
    alamat_saksi1 = st.text_area("Alamat Saksi 1")
    nik_saksi1 = st.text_input("NIK Saksi 1")

    nama_saksi2 = st.text_input("Nama Saksi 2")
    ttl_saksi2 = st.text_input("Tempat & Tanggal Lahir Saksi 2")
    alamat_saksi2 = st.text_area("Alamat Saksi 2")
    nik_saksi2 = st.text_input("NIK Saksi 2")

    submit = st.form_submit_button("Buat Akta")

if submit:
    doc = DocxTemplate("akta_pendirian_cv_template.docx")
    context = {
        "nomor_akta": nomor_akta,
        "tanggal_akta": tanggal_akta.strftime("%d-%m-%Y"),
        "jam_akta": jam_akta,
        "nama_cv": nama_cv,
        "alamat_cv": alamat_cv,
        "nama_pihak1": nama_pihak1,
        "ttl_pihak1": ttl_pihak1,
        "pekerjaan_pihak1": pekerjaan_pihak1,
        "alamat_pihak1": alamat_pihak1,
        "nik_pihak1": nik_pihak1,
        "modal_pihak1": f"Rp. {modal_pihak1:,}",
        "modal_pihak1_terbilang": modal_pihak1_terbilang,
        "nama_pihak2": nama_pihak2,
        "ttl_pihak2": ttl_pihak2,
        "pekerjaan_pihak2": pekerjaan_pihak2,
        "alamat_pihak2": alamat_pihak2,
        "nik_pihak2": nik_pihak2,
        "modal_pihak2": f"Rp. {modal_pihak2:,}",
        "modal_pihak2_terbilang": modal_pihak2_terbilang,
        "bidang_usaha": bidang_usaha,
        "modal_total": f"Rp. {modal_total:,}",
        "modal_total_terbilang": modal_total_terbilang,
        "nama_notaris": nama_notaris,
        "nama_saksi1": nama_saksi1,
        "ttl_saksi1": ttl_saksi1,
        "alamat_saksi1": alamat_saksi1,
        "nik_saksi1": nik_saksi1,
        "nama_saksi2": nama_saksi2,
        "ttl_saksi2": ttl_saksi2,
        "alamat_saksi2": alamat_saksi2,
        "nik_saksi2": nik_saksi2
    }
    doc.render(context)

    output_path = f"akta_pendirian_cv_{nomor_akta}.docx"
    doc.save(output_path)

    with open(output_path, "rb") as f:
        st.download_button(
            label="📥 Download Akta",
            data=f,
            file_name=output_path,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
