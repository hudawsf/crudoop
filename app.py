
import streamlit as st
import pandas as pd
import re

from mahasiswa import Mahasiswa


# =====================================
# KONFIGURASI APLIKASI
# =====================================

st.set_page_config(
    page_title="CRUD Mahasiswa",
    page_icon="🎓",
    layout="wide"
)

db = Mahasiswa()


# =====================================
# FUNGSI VALIDASI
# =====================================

def email_valid(email):
    if not email:
        return True

    pola = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return re.match(pola, email) is not None


def nim_valid(nim):
    return bool(nim.strip())


def nama_valid(nama):
    return bool(nama.strip())


# =====================================
# SIDEBAR MENU
# =====================================

st.sidebar.title("🎓 Menu Aplikasi")

menu = st.sidebar.radio(
    "Menu Utama",
    [
        "Dashboard",
        "Data Mahasiswa",
        "Tambah Mahasiswa",
        "Edit Mahasiswa",
        "Hapus Mahasiswa"
    ]
)

st.sidebar.divider()
st.sidebar.caption("CRUD Mahasiswa")
st.sidebar.caption("Python OOP + Streamlit + MySQL")


# =====================================
# DASHBOARD
# =====================================

if menu == "Dashboard":

    st.title("Dashboard Mahasiswa")

    try:
        data = db.tampilkan()

        total = len(data)

        jumlah_jurusan = len(set(
            item["jurusan"]
            for item in data
            if item["jurusan"]
        ))

        col1, col2 = st.columns(2)

        col1.metric(
            "Total Mahasiswa",
            total
        )

        col2.metric(
            "Jumlah Jurusan",
            jumlah_jurusan
        )

        st.divider()

        st.subheader("Data Mahasiswa Terbaru")

        if data:

            df = pd.DataFrame(data)

            st.dataframe(
                df.head(5),
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info("Belum ada data mahasiswa.")

    except Exception as e:
        st.error(f"Gagal memuat dashboard: {e}")


# =====================================
# DATA MAHASISWA
# =====================================

elif menu == "Data Mahasiswa":

    st.title("Data Mahasiswa")

    keyword = st.text_input(
        "Cari Mahasiswa",
        placeholder="Masukkan nama, NIM, atau jurusan..."
    )

    try:
        data = db.cari_data(keyword)

        if data:

            df = pd.DataFrame(data)

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            st.success(
                f"Data ditemukan: {len(data)} mahasiswa"
            )

        else:
            st.warning("Data mahasiswa tidak ditemukan.")

    except Exception as e:
        st.error(f"Gagal mengambil data: {e}")


# =====================================
# TAMBAH MAHASISWA
# =====================================

elif menu == "Tambah Mahasiswa":

    st.title("Tambah Mahasiswa")

    with st.form("form_tambah"):

        nama = st.text_input("Nama Lengkap")

        nim = st.text_input("NIM")

        jurusan = st.text_input("Jurusan")

        email = st.text_input("Email")

        submit = st.form_submit_button(
            "Simpan Data",
            use_container_width=True
        )

        if submit:

            if not nama_valid(nama):
                st.warning("Nama wajib diisi.")

            elif not nim_valid(nim):
                st.warning("NIM wajib diisi.")

            elif not email_valid(email.strip()):
                st.warning("Format email tidak valid.")

            else:

                try:
                    db.tambah(
                        nama.strip(),
                        nim.strip(),
                        jurusan.strip(),
                        email.strip()
                    )

                    st.success(
                        "Data mahasiswa berhasil ditambahkan!"
                    )

                    st.rerun()

                except Exception as e:

                    if "Duplicate entry" in str(e):
                        st.error(
                            "NIM sudah terdaftar. "
                            "Silakan gunakan NIM lain."
                        )

                    else:
                        st.error(
                            f"Gagal menyimpan data: {e}"
                        )


# =====================================
# EDIT MAHASISWA
# =====================================

elif menu == "Edit Mahasiswa":

    st.title("Edit Data Mahasiswa")

    try:
        data = db.tampilkan()

        if not data:

            st.info("Belum ada data mahasiswa.")

        else:

            pilihan = st.selectbox(
                "Pilih Mahasiswa",
                data,
                format_func=lambda x: (
                    f"{x['nim']} - {x['nama']}"
                )
            )

            mahasiswa = db.cari(pilihan["id"])

            if mahasiswa:

                with st.form("form_edit"):

                    nama = st.text_input(
                        "Nama Lengkap",
                        value=mahasiswa["nama"] or ""
                    )

                    nim = st.text_input(
                        "NIM",
                        value=mahasiswa["nim"] or ""
                    )

                    jurusan = st.text_input(
                        "Jurusan",
                        value=mahasiswa["jurusan"] or ""
                    )

                    email = st.text_input(
                        "Email",
                        value=mahasiswa["email"] or ""
                    )

                    submit = st.form_submit_button(
                        "Update Data",
                        use_container_width=True
                    )

                    if submit:

                        if not nama_valid(nama):
                            st.warning("Nama wajib diisi.")

                        elif not nim_valid(nim):
                            st.warning("NIM wajib diisi.")

                        elif not email_valid(email.strip()):
                            st.warning("Format email tidak valid.")

                        else:

                            try:
                                db.update(
                                    mahasiswa["id"],
                                    nama.strip(),
                                    nim.strip(),
                                    jurusan.strip(),
                                    email.strip()
                                )

                                st.success(
                                    "Data berhasil diperbarui!"
                                )

                                st.rerun()

                            except Exception as e:

                                if "Duplicate entry" in str(e):
                                    st.error(
                                        "NIM sudah digunakan mahasiswa lain."
                                    )

                                else:
                                    st.error(
                                        f"Gagal memperbarui data: {e}"
                                    )

    except Exception as e:
        st.error(f"Gagal memuat data: {e}")


# =====================================
# HAPUS MAHASISWA
# =====================================

elif menu == "Hapus Mahasiswa":

    st.title("Hapus Data Mahasiswa")

    try:
        data = db.tampilkan()

        if not data:

            st.info("Belum ada data mahasiswa.")

        else:

            pilihan = st.selectbox(
                "Pilih Mahasiswa",
                data,
                format_func=lambda x: (
                    f"{x['nim']} - {x['nama']}"
                )
            )

            st.warning(
                f"Anda akan menghapus data: {pilihan['nama']}"
            )

            konfirmasi = st.checkbox(
                "Saya yakin ingin menghapus data ini."
            )

            if st.button(
                "Hapus Data",
                type="primary"
            ):

                if konfirmasi:

                    db.hapus(pilihan["id"])

                    st.success(
                        "Data mahasiswa berhasil dihapus!"
                    )

                    st.rerun()

                else:
                    st.warning(
                        "Centang konfirmasi terlebih dahulu."
                    )

    except Exception as e:
        st.error(f"Gagal menghapus data: {e}")
