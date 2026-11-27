"""Halaman Manajemen Menu: tambah, ubah, hapus, dan lihat daftar menu.

Isian form dan kolom daftar memakai urutan yang sama:
Nama produk, Kategori, Jenis, Harga.
"""
import streamlit as st

from models.menu import Menu
from utils import rupiah
from views.komponen import (LEBAR_PENUH, flash, h, judul, kartu, kartu_judul, kosong,
                            tampilkan_flash)

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
    with kartu("form"):
        kartu_judul("Ubah Menu" if ss.edit_id else "Tambah Menu")
        st.text_input("Nama produk", key="f_nama", placeholder="Nama produk")
        st.selectbox("Kategori", Menu.daftar_kategori(), key="f_kategori")

        # Pilihan Jenis mengikuti Kategori yang sedang dipilih
        opsi_jenis = Menu.daftar_jenis(ss.f_kategori)
        if ss.f_jenis not in opsi_jenis:
            ss.f_jenis = opsi_jenis[0]
        st.selectbox("Jenis", opsi_jenis, key="f_jenis")

        st.number_input("Harga (Rp)", min_value=0, step=1000, key="f_harga")
        if ss.error_form:
            st.error(ss.error_form)
        st.button("Simpan" if ss.edit_id else "Tambah", key="simpan_menu", type="primary",
                  on_click=_simpan, args=(ctrl,), **LEBAR_PENUH)
        if ss.edit_id:
            st.button("Batal", key="batal_ubah", on_click=_reset_form, **LEBAR_PENUH)


LEBAR_KOLOM = [2.6, 1.5, 1.7, 1.9, 1, 1.1]      # Nama produk, Kategori, Jenis, Harga, Ubah, Hapus


def _daftar(ctrl):
    ss = st.session_state
    daftar = ctrl.daftar_menu()
    with kartu("daftar"):
        kartu_judul(f"Daftar Menu ({len(daftar)})")
        if ss.hapus_id:
            menu = ctrl.cari_menu(ss.hapus_id)
            if menu:
                st.warning(f"Hapus menu “{menu.nama}”?")
                ya, tidak, _ = st.columns([1, 1, 2])
                ya.button("Ya, hapus", key="ya_hapus", on_click=_konfirmasi_hapus, args=(ctrl,),
                          type="primary", **LEBAR_PENUH)
                tidak.button("Batal", key="batal_hapus", on_click=_batal_hapus, **LEBAR_PENUH)
        if not daftar:
            kosong("Belum ada menu.")
            return

        with st.container(key="baris_kepala"):
            for kolom, teks in zip(st.columns(LEBAR_KOLOM, gap="small"),
                                   ["Nama produk", "Kategori", "Jenis", "Harga", "", ""]):
                kolom.markdown(f'<div class="th">{teks}</div>', unsafe_allow_html=True)
        for menu in daftar:
            with st.container(key=f"baris_menu_{menu.id}"):
                nama, kategori, jenis, harga, ubah, hapus = st.columns(
                    LEBAR_KOLOM, gap="small", vertical_alignment="center")
                nama.markdown(f'<div class="sel">{h(menu.ikon)} {h(menu.nama)}</div>',
                              unsafe_allow_html=True)
                kategori.markdown(f'<span class="lencana">{h(menu.kategori)}</span>',
                                  unsafe_allow_html=True)
                jenis.markdown(f'<div class="sel">{h(menu.jenis)}</div>', unsafe_allow_html=True)
                harga.markdown(f'<div class="sel">{h(rupiah(menu.harga))}</div>',
                               unsafe_allow_html=True)
                ubah.button("Ubah", key=f"mn_ubah_{menu.id}", on_click=_mulai_ubah,
                            args=(menu.id, ctrl))
                hapus.button("Hapus", key=f"mn_hapus_{menu.id}", on_click=_minta_hapus,
                             args=(menu.id,))


def tampilkan(ctrl):
    ss = st.session_state
    if "f_nama" not in ss:          # pertama kali dibuka, atau state form sudah dibersihkan
        _reset_form()
    ss.setdefault("hapus_id", None)
    judul("Manajemen Menu", "Tambah, ubah, hapus, dan lihat daftar menu kopi, non-kopi, dan makanan.")
    tampilkan_flash()
    kiri, kanan = st.columns([1, 2.1], gap="large")
    with kiri:
        _form(ctrl)
    with kanan:
        _daftar(ctrl)