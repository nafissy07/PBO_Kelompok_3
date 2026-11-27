"""Halaman Dashboard."""
from datetime import datetime

import streamlit as st

from utils import rupiah
from views.komponen import (HALAMAN_PEMESANAN, kartu, kartu_judul, kartu_stat, judul,
                            kosong, tabel_html)


def _sapaan() -> str:
    jam = datetime.now().hour
    if jam < 11:
        return "pagi"
    if jam < 15:
        return "siang"
    if jam < 18:
        return "sore"
    return "malam"


def _ke_pemesanan():
    st.session_state.halaman = HALAMAN_PEMESANAN


def tampilkan(ctrl):
    ringkas = ctrl.ringkasan()
    kiri, kanan = st.columns([4, 1], vertical_alignment="center")
    with kiri:
        judul(f"Selamat {_sapaan()}, {ctrl.kasir.nama}!",
              "Ringkasan aktivitas Coffee Order System hari ini.")
    with kanan:
        st.button("+ Pesanan Baru", key="pesanan_baru", type="primary", on_click=_ke_pemesanan)

    terlaris = ringkas["menu_terlaris"]
    kolom = st.columns(4)
    kartu_stat(kolom[0], "pendapatan", "💰 Total pendapatan", rupiah(ringkas["total_pendapatan"]))
    kartu_stat(kolom[1], "transaksi", "🧾 Jumlah transaksi", str(ringkas["jumlah_transaksi"]))
    kartu_stat(kolom[2], "menu", "📋 Item menu", str(ringkas["jumlah_menu"]))
    kartu_stat(kolom[3], "terlaris", "⭐ Menu terlaris",
               f"{terlaris[0]} ({terlaris[1]})" if terlaris else "-")

    with kartu("terbaru"):
        kartu_judul("Transaksi terbaru")
        terbaru = ctrl.cari_riwayat("")[:5]
        if not terbaru:
            kosong("Belum ada transaksi ☕")
        else:
            tabel_html(["ID", "Waktu", "Pelanggan", "Total"],
                       [[t.id_transaksi, t.waktu.strftime("%d %b %Y, %H.%M"),
                         t.pelanggan, rupiah(t.total)] for t in terbaru])