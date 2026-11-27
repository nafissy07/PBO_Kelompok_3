"""Titik masuk aplikasi. Jalankan dengan:  streamlit run app.py"""
from pathlib import Path

import streamlit as st

from controllers.kedai_controller import KedaiController
from views import dashboard, manajemen_menu, pemesanan, riwayat, style
from views.komponen import (HALAMAN_DASHBOARD, HALAMAN_MENU, HALAMAN_PEMESANAN,
                            HALAMAN_RIWAYAT, LEBAR_PENUH)

st.set_page_config(page_title="Coffee Order System", page_icon="☕", layout="wide")

DB_PATH = str(Path(__file__).parent / "data" / "kedai_kopi.db")

HALAMAN = {
    HALAMAN_DASHBOARD: dashboard.tampilkan,
    HALAMAN_PEMESANAN: pemesanan.tampilkan,
    HALAMAN_MENU: manajemen_menu.tampilkan,
    HALAMAN_RIWAYAT: riwayat.tampilkan,
}


def _buka(nama_halaman: str):
    """Dipanggil saat tombol menu diklik: simpan halaman yang dipilih."""
    st.session_state.halaman = nama_halaman


@st.cache_resource
def ambil_controller() -> KedaiController:
    """Controller dibuat sekali saja, lalu dipakai ulang di setiap interaksi."""
    return KedaiController(DB_PATH)


def main():
    ctrl = ambil_controller()
    # Nilai toggle sudah tersimpan di session_state sebelum skrip berjalan,
    # jadi mode gelap bisa diterapkan sebelum sidebar digambar.
    style.terapkan(st.session_state.get("mode_gelap", False))

    with st.sidebar:
        st.markdown('<div class="brand"><div class="logo">☕</div><div>'
                    '<div class="brand-nama">Coffee Order</div>'
                    '<div class="brand-sub">System · Kelompok 3</div></div></div>',
                    unsafe_allow_html=True)
        st.session_state.setdefault("halaman", next(iter(HALAMAN)))
        for nama_halaman in HALAMAN:
            aktif = nama_halaman == st.session_state.halaman
            st.button(nama_halaman, key=f"nav_{nama_halaman}", on_click=_buka,
                      args=(nama_halaman,), type="primary" if aktif else "secondary",
                      **LEBAR_PENUH)

        with st.container(key="side_kasir"):
            st.markdown(f'<div class="kasir-label">Kasir aktif · {ctrl.kasir.id_kasir}</div>',
                        unsafe_allow_html=True)
            nama = st.text_input("Nama kasir", value=ctrl.kasir.nama, key="input_kasir",
                                 label_visibility="collapsed")
            if nama != ctrl.kasir.nama:
                try:
                    ctrl.ganti_nama_kasir(nama)
                except ValueError:
                    st.warning("Nama kasir tidak boleh kosong")
            st.toggle("Mode gelap", key="mode_gelap")

    HALAMAN[st.session_state.halaman](ctrl)


main()