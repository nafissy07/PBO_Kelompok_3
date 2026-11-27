"""Halaman Riwayat Transaksi: lihat dan cari transaksi sebelumnya."""
import streamlit as st

from utils import rupiah
from views.komponen import judul, kartu, kosong, tabel_html


def tampilkan(ctrl):
    judul("Riwayat Transaksi", "Cari dan lihat kembali pesanan sebelumnya.")
    with kartu("riwayat"):
        kata = st.text_input("Cari transaksi", key="cari_riwayat",
                             placeholder="Cari ID, pelanggan, atau nama produk...",
                             label_visibility="collapsed")
        data = ctrl.cari_riwayat(kata)
        if not data:
            kosong("Tidak ada transaksi yang cocok 🔍" if kata else "Belum ada transaksi ☕")
            return
        tabel_html(
            ["ID", "Waktu", "Pelanggan", "Item", "Total", "Bayar", "Kembali", "Status"],
            [[t.id_transaksi, t.waktu.strftime("%d %b %Y, %H.%M"), t.pelanggan, t.jumlah_item,
              rupiah(t.total), rupiah(t.uang_bayar), rupiah(t.kembalian), "Lunas"]
             for t in data],
            kolom_lencana=("Status",))

        pilihan = st.selectbox("Lihat struk", [t.id_transaksi for t in data])
        transaksi = next(t for t in data if t.id_transaksi == pilihan)
        st.code(transaksi.cetak_struk(), language=None)