from docx import Document
import re

def parse_docx_template(file):
    doc = Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])

    data = {
        "jenis_badan": "CV" if "sekutu" in text.lower() else "Yayasan",
        "nama_badan": "",
        "alamat": "",
        "bidang_usaha": "",
        "pengurus_list": [],
        "modal_list": [],
        "kbli_list": []
    }

    # === NAMA BADAN HUKUM ===
    match_nama = re.search(r"bernama\s+([A-Z .]+)", text, re.IGNORECASE)
    if match_nama:
        data["nama_badan"] = match_nama.group(1).strip()

    # === BIDANG USAHA / KBLI ===
    match_kbli = re.findall(r"KBLI.*?(\d{5})\s*-\s*(.*)", text)
    if match_kbli:
        for kode, judul in match_kbli:
            data["kbli_list"].append({
                "kode": kode.strip(),
                "judul": judul.strip()
            })
        data["bidang_usaha"] = "\n".join([f"{k} - {j}" for k, j in match_kbli])

    # === PENGURUS (Nama, Jabatan, NIK) ===
    pengurus = []
    pattern_pengurus = re.findall(r"(?i)(Ketua|Sekretaris|Bendahara|Direktur|Komisaris|Pembina|Pengawas).*?:\s*(.*?)\s*\(NIK[:：]?\s*(\d{8,})\)", text)
    for jabatan, nama, nik in pattern_pengurus:
        pengurus.append({
            "jabatan": jabatan.strip(),
            "nama": nama.strip(),
            "nik": nik.strip()
        })
    data["pengurus_list"] = pengurus

    # === MODAL ===
    pattern_modal = re.findall(r"modal.*?oleh\s*(.*?)\s*sebesar\s*Rp?\.?\s*([\d\.]+)", text, re.IGNORECASE)
    for nama, jumlah in pattern_modal:
        data["modal_list"].append({
            "nama": nama.strip(),
            "peran": "Pemilik Modal",
            "jumlah": int(jumlah.replace(".", "")),
            "jenis": "Tunai"
        })

    return data
