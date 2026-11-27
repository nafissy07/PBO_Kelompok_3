"""Komponen tampilan yang dipakai berulang."""
import html
import inspect

import streamlit as st

# Lebar penuh untuk tombol. Streamlit versi baru memakai width="stretch",
# versi lama memakai use_container_width=True. Dipilih otomatis.
try:
    _punya_width = "width" in inspect.signature(st.button).parameters
except (TypeError, ValueError):
    _punya_width = False
LEBAR_PENUH = {"width": "stretch"} if _punya_width else {"use_container_width": True}

# Nama halaman (dipakai app.py untuk navigasi dan dashboard untuk tombol pintas)
HALAMAN_DASHBOARD = "🏠 Dashboard"
HALAMAN_PEMESANAN = "🧾 Pemesanan"
HALAMAN_MENU = "📋 Manajemen Menu"
HALAMAN_RIWAYAT = "🕘 Riwayat Transaksi"


def h(teks) -> str:
    """Amankan teks dari pengguna sebelum disisipkan ke HTML."""
    return html.escape(str(teks))


def judul(teks: str, keterangan: str = ""):
    isi = f'<div class="judul">{h(teks)}</div>'
    if keterangan:
        isi += f'<div class="sub-judul">{h(keterangan)}</div>'
    st.markdown(isi, unsafe_allow_html=True)


def kartu(nama: str):
    """Wadah bergaya kartu. Dipakai dengan: with kartu('nama'): ..."""
    return st.container(key=f"kartu_{nama}")


def kartu_stat(kolom, kunci: str, label: str, nilai: str):
    with kolom:
        with kartu(f"stat_{kunci}"):
            st.markdown(f'<div class="stat-label">{h(label)}</div>'
                        f'<div class="stat-nilai">{h(nilai)}</div>', unsafe_allow_html=True)


def kartu_judul(teks: str):
    st.markdown(f'<div class="kartu-judul">{h(teks)}</div>', unsafe_allow_html=True)


def kosong(teks: str):
    st.markdown(f'<div class="kosong">{h(teks)}</div>', unsafe_allow_html=True)


def tabel_html(kepala: list, baris: list, kolom_lencana: tuple = ()):
    """Tabel HTML sederhana. Semua isi sel di-escape; kolom_lencana tampil sebagai lencana hijau."""
    th = "".join(f"<th>{h(k)}</th>" for k in kepala)
    tr = ""
    for b in baris:
        td = ""
        for k, sel in zip(kepala, b):
            isi = h(sel)
            if k in kolom_lencana:
                isi = f'<span class="lencana lencana-hijau">{isi}</span>'
            td += f"<td>{isi}</td>"
        tr += f"<tr>{td}</tr>"
    st.markdown(f'<div class="tabel-bungkus"><table class="tabel"><thead><tr>{th}</tr></thead>'
                f"<tbody>{tr}</tbody></table></div>", unsafe_allow_html=True)


def flash(tipe: str, teks: str):
    """Simpan pesan agar tetap tampil setelah halaman dimuat ulang."""
    st.session_state["flash"] = (tipe, teks)


def tampilkan_flash():
    pesan = st.session_state.pop("flash", None)
    if pesan:
        tipe, teks = pesan
        (st.success if tipe == "success" else st.error)(teks)