"""Halaman Manajemen Menu: tambah, ubah, hapus, dan lihat daftar menu.

Isian form dan kolom daftar memakai urutan yang sama:
Nama produk, Kategori, Jenis, Harga.
"""
import streamlit as st

from models.menu import Menu
from utils import rupiah
from views.komponen import LEBAR_PENUH, flash, judul, tampilkan_flash

KATEGORI_AWAL = Menu.daftar_kategori()[0]


# ---------- callback tombol (dijalankan sebelum halaman digambar ulang) ----------
def _reset_form():
    ss = st.session_state
    ss.edit_id = None
    ss.f_nama = ""
    ss.f_kategori = KATEGORI_AWAL
    ss.f_jenis = Menu.daftar_jenis(KATEGORI_AWAL)[0]
    ss.f_harga = 0
    ss.error_form = None


def _mulai_ubah(id_menu, ctrl):
    menu = ctrl.cari_menu(id_menu)
    if menu is None:
        return
    ss = st.session_state
    ss.edit_id = id_menu
    ss.f_nama = menu.nama
    ss.f_kategori = menu.kategori
    ss.f_jenis = menu.jenis
    ss.f_harga = menu.harga
    ss.error_form = None


def _simpan(ctrl):
    ss = st.session_state
    try:
        if ss.edit_id:
            ctrl.ubah_menu(ss.edit_id, ss.f_kategori, ss.f_nama, ss.f_jenis, ss.f_harga)
            flash("success", "Menu diperbarui ✓")
        else:
            ctrl.tambah_menu(ss.f_kategori, ss.f_nama, ss.f_jenis, ss.f_harga)
            flash("success", "Menu ditambahkan ✓")
    except ValueError as e:                     # nama kosong / harga tidak valid / jenis salah
        ss.error_form = str(e)
        return
    _reset_form()


def _minta_hapus(id_menu):
    st.session_state.hapus_id = id_menu


def _batal_hapus():
    st.session_state.hapus_id = None


def _konfirmasi_hapus(ctrl):
    ctrl.hapus_menu(st.session_state.hapus_id)
    st.session_state.hapus_id = None
    flash("success", "Menu dihapus")


# ---------- tampilan ----------
def _form(ctrl):
    ss = st.session_state
    with st.container(border=True):
        st.markdown("### Ubah Menu" if ss.edit_id else "### Tambah Menu")
        st.text_input("Nama produk", key="f_nama")
        st.selectbox("Kategori", Menu.daftar_kategori(), key="f_kategori")

        # Pilihan Jenis mengikuti Kategori yang sedang dipilih
        opsi_jenis = Menu.daftar_jenis(ss.f_kategori)
        if ss.f_jenis not in opsi_jenis:
            ss.f_jenis = opsi_jenis[0]
        st.selectbox("Jenis", opsi_jenis, key="f_jenis")

        st.number_input("Harga (Rp)", min_value=0, step=1000, key="f_harga")
        if ss.error_form:
            st.error(ss.error_form)
        st.button("Simpan" if ss.edit_id else "Tambah", type="primary",
                  on_click=_simpan, args=(ctrl,))
        if ss.edit_id:
            st.button("Batal", on_click=_reset_form)


def _daftar(ctrl):
    ss = st.session_state
    daftar = ctrl.daftar_menu()
    with st.container(border=True):
        st.markdown(f"### Daftar Menu ({len(daftar)})")
        if ss.hapus_id:
            menu = ctrl.cari_menu(ss.hapus_id)
            if menu:
                st.warning(f"Hapus menu “{menu.nama}”?")
                ya, tidak, _ = st.columns([1, 1, 3])
                ya.button("Ya, hapus", on_click=_konfirmasi_hapus, args=(ctrl,), type="primary")
                tidak.button("Batal", on_click=_batal_hapus, key="batal_hapus")
        if not daftar:
            st.info("Belum ada menu.")
            return

        lebar = [3, 2, 2, 2, 1, 1]
        kepala = st.columns(lebar)
        for kolom, teks in zip(kepala, ["Nama produk", "Kategori", "Jenis", "Harga", "", ""]):
            kolom.markdown(f"**{teks}**" if teks else "")
        for menu in daftar:
            nama, kategori, jenis, harga, ubah, hapus = st.columns(lebar)
            nama.write(f"{menu.ikon} {menu.nama}")
            kategori.write(menu.kategori)
            jenis.write(menu.jenis)
            harga.write(rupiah(menu.harga))
            ubah.button("Ubah", key=f"ubah_{menu.id}", on_click=_mulai_ubah, args=(menu.id, ctrl))
            hapus.button("Hapus", key=f"hapus_{menu.id}", on_click=_minta_hapus, args=(menu.id,))


def tampilkan(ctrl):
    ss = st.session_state
    if "f_nama" not in ss:          # pertama kali dibuka, atau state form sudah dibersihkan
        _reset_form()
    ss.setdefault("hapus_id", None)
    judul("Manajemen Menu", "Tambah, ubah, hapus, dan lihat daftar menu makanan dan minuman.")
    tampilkan_flash()
    kiri, kanan = st.columns([1, 2], gap="large")
    with kiri:
        _form(ctrl)
    with kanan:
        _daftar(ctrl)