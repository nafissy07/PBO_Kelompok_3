"""Gaya (CSS) supaya tampilan mengikuti rancangan GUI, termasuk mode terang/gelap.

Warna disimpan sebagai variabel CSS (--bg, --kartu, dst). Mode gelap cukup mengganti
nilai variabelnya, jadi seluruh aturan CSS di bawah dipakai bersama oleh kedua mode.
"""
import streamlit as st

TERANG = {
    "bg": "#DCCBB9", "sisi": "#F5EFE3", "kartu": "#F5EFE3", "tile": "#EADFCF",
    "input": "#E3D3C1", "teks": "#7B4B3A", "lembut": "#A08373", "garis": "#E2D5C3",
    "garis-tebal": "#D4BFA8", "aksen": "#BF8461", "aksen-tua": "#7B4B3A",
    "bayangan": "rgba(90,55,35,.10)",
}
GELAP = {
    "bg": "#241A16", "sisi": "#30231D", "kartu": "#3A2B24", "tile": "#4A382F",
    "input": "#2B201B", "teks": "#F1E3D3", "lembut": "#C4A992", "garis": "#4D3B31",
    "garis-tebal": "#6A5244", "aksen": "#D39A74", "aksen-tua": "#8A5A45",
    "bayangan": "rgba(0,0,0,.35)",
}

FONT = "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700;800&display=swap');"

CSS = """
html, body, .stApp, button, input, textarea { font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif; }
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background: var(--bg); color: var(--teks); }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"], [data-testid="stHeaderActionElements"] { display: none !important; }
.block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1320px; }
.stApp p, .stApp label, .stApp li, .stApp h1, .stApp h2, .stApp h3, [data-testid="stWidgetLabel"] p { color: var(--teks); }
[data-testid="stWidgetLabel"] p { font-size: .8rem; font-weight: 600; color: var(--lembut); }

/* ---------- sidebar ---------- */
[data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child { background: var(--sisi); }
[data-testid="stSidebar"] { border-right: none; box-shadow: 2px 0 14px var(--bayangan); }
.brand { display: flex; align-items: center; gap: .7rem; margin: .2rem 0 1.3rem; }
.brand .logo { width: 42px; height: 42px; border-radius: 12px; background: var(--aksen); display: flex; align-items: center; justify-content: center; font-size: 1.4rem; flex: none; }
.brand-nama { font-weight: 800; font-size: 1.1rem; color: var(--teks); line-height: 1.1; }
.brand-sub { font-size: .7rem; color: var(--lembut); }
[data-testid="stSidebar"] .stButton button { justify-content: flex-start; width: 100%; padding: .55rem .9rem; min-height: 2.6rem; background: transparent; }
[data-testid="stSidebar"] .stButton button p { text-align: left; font-size: .95rem; }
[data-testid="stSidebar"] .stButton button:hover { background: var(--tile); }
[data-testid="stSidebar"] .stButton button[kind="primary"], [data-testid="stSidebar"] .stButton button[data-testid="stBaseButton-primary"] { background: var(--aksen-tua); }
.st-key-side_kasir { background: var(--tile); border-radius: 14px; padding: .8rem .9rem; margin-top: 1.6rem; }
.kasir-label { font-size: .75rem; font-weight: 700; color: var(--teks); margin-bottom: .4rem; }

/* ---------- judul halaman ---------- */
.judul { font-size: 2rem; font-weight: 800; color: var(--teks); line-height: 1.15; margin-bottom: .2rem; }
.sub-judul { font-size: .88rem; color: var(--lembut); margin-bottom: 1.2rem; }

/* ---------- kartu ---------- */
[class*="st-key-kartu_"] { background: var(--kartu); border-radius: 18px; padding: 1.1rem 1.3rem; box-shadow: 0 2px 12px var(--bayangan); }
.kartu-judul { font-size: 1.3rem; font-weight: 800; color: var(--teks); margin-bottom: .6rem; }
.stat-label { font-size: 1rem; font-weight: 700; color: var(--lembut); }
.stat-nilai { font-size: 1.6rem; font-weight: 800; color: var(--teks); margin-top: .9rem; line-height: 1.2; word-break: break-word; }
[class*="st-key-kartu_stat_"] { padding: 1.3rem 1.4rem 1.6rem; min-height: 7.8rem; }
[class*="st-key-kartu_terbaru"] { margin-top: .8rem; }
.kosong { text-align: center; padding: 1.4rem 0 1rem; color: var(--lembut); font-weight: 600; }

/* ---------- tombol ---------- */
.stButton button { border-radius: 12px; font-weight: 700; border: none; background: var(--tile); min-height: 2.4rem; transition: filter .15s, transform .15s; }
.stApp .stButton button, .stApp .stButton button p { color: var(--teks); }
.stButton button:hover { filter: brightness(.96); transform: translateY(-1px); }
.stButton button:disabled { opacity: .5; transform: none; }
.stApp .stButton button[kind="primary"], .stApp .stButton button[data-testid="stBaseButton-primary"] { background: var(--aksen); }
.stApp .stButton button[kind="primary"] p, .stApp .stButton button[data-testid="stBaseButton-primary"] p { color: #fff; }
.st-key-pesanan_baru { display: flex; justify-content: flex-end; }
.st-key-pesanan_baru button, .st-key-proses_bayar button { border-radius: 999px; }
.st-key-pesanan_baru button { padding: .4rem 1.3rem; }
.st-key-proses_bayar button { min-height: 2.9rem; }

/* ---------- kolom isian ---------- */
[data-baseweb="input"], [data-baseweb="base-input"], [data-baseweb="textarea"], [data-baseweb="select"] > div { background: var(--input) !important; border: none !important; border-radius: 12px !important; }
[data-baseweb="input"] input, [data-baseweb="select"] div, [data-baseweb="select"] span { color: var(--teks) !important; }
[data-baseweb="input"]:focus-within { box-shadow: 0 0 0 2px var(--aksen) !important; }
input::placeholder { color: var(--lembut) !important; opacity: 1; }
[data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] { display: none; }
[data-baseweb="popover"] [role="listbox"], [data-baseweb="menu"] { background: var(--kartu) !important; }
[data-baseweb="popover"] [role="option"] { color: var(--teks) !important; }
[data-baseweb="popover"] [role="option"]:hover, [data-baseweb="popover"] [role="option"][aria-selected="true"] { background: var(--tile) !important; }
[data-testid="stCode"] pre, [data-testid="stCode"] code { background: var(--tile) !important; color: var(--teks) !important; }
[data-testid="stCode"] { border-radius: 12px; }

/* ---------- filter kategori (radio dibuat jadi pil) ---------- */
.stRadio [role="radiogroup"] { gap: .5rem; flex-wrap: wrap; }
.stRadio label[data-baseweb="radio"] { border: 1.5px solid var(--garis-tebal); border-radius: 999px; padding: .2rem .95rem; margin: 0; cursor: pointer; }
.stRadio label[data-baseweb="radio"] > div:first-child { display: none; }
.stRadio label[data-baseweb="radio"] p { font-weight: 700; font-size: .85rem; }
.stRadio label[data-baseweb="radio"]:has(input:checked) { background: var(--aksen); border-color: var(--aksen); }
.stRadio label[data-baseweb="radio"]:has(input:checked) p { color: #fff !important; }

/* ---------- kartu produk (seluruh kartu bisa diklik) ---------- */
[class*="st-key-produk_"] { position: relative; background: var(--tile); border-radius: 16px; padding: .95rem 1rem; min-height: 9.6rem; transition: transform .15s, box-shadow .15s; }
[class*="st-key-produk_"]:hover { transform: translateY(-2px); box-shadow: 0 6px 16px var(--bayangan); }
[class*="st-key-produk_"] .stButton { position: absolute; inset: 0; width: 100%; height: 100%; z-index: 2; }
[class*="st-key-produk_"] .stButton button { width: 100%; height: 100%; opacity: 0; cursor: pointer; }
.produk-ikon { font-size: 1.9rem; line-height: 1; margin-bottom: .5rem; }
.produk-nama { font-weight: 800; font-size: .95rem; line-height: 1.2; min-height: 2.4em; color: var(--teks); }
.produk-sub { font-size: .72rem; color: var(--lembut); margin-top: .15rem; }
.produk-harga { font-weight: 800; font-size: .88rem; color: var(--teks); margin-top: .55rem; }

/* ---------- keranjang ---------- */
[class*="st-key-baris_"] { border-bottom: 1px solid var(--garis); padding: .45rem 0; }
.krj-nama { font-weight: 700; font-size: .9rem; color: var(--teks); }
.krj-sub { font-size: .75rem; color: var(--lembut); }
.krj-jml { text-align: center; font-weight: 700; font-size: 1rem; color: var(--teks); }
[class*="st-key-krj_"] { display: flex; justify-content: center; align-items: center; }
[class*="st-key-krj_"] .stButton { display: flex; justify-content: center; align-items: center; width: auto; }
[class*="st-key-krj_"] button { display: flex; align-items: center; justify-content: center; min-height: 0; height: 1.9rem; width: 1.9rem; padding: 0; border-radius: 50%; background: transparent; border: 1.5px solid var(--aksen); }
[class*="st-key-krj_"] button p { margin: 0; color: var(--aksen) !important; font-size: 1.1rem; font-weight: 700; line-height: 1; }
/* Simbol − dan + digambar dengan CSS (bukan huruf) supaya pas di tengah lingkaran */
[class*="st-key-krj_min_"] button p, [class*="st-key-krj_plus_"] button p { display: none; }
[class*="st-key-krj_min_"] button::before, [class*="st-key-krj_plus_"] button::before { content: ""; display: block; width: .85rem; height: .85rem; background: var(--aksen); -webkit-mask-repeat: no-repeat; mask-repeat: no-repeat; -webkit-mask-position: center; mask-position: center; -webkit-mask-size: contain; mask-size: contain; }
[class*="st-key-krj_min_"] button::before { -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect x='3' y='10.5' width='18' height='3' rx='1.5'/%3E%3C/svg%3E"); mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect x='3' y='10.5' width='18' height='3' rx='1.5'/%3E%3C/svg%3E"); }
[class*="st-key-krj_plus_"] button::before { -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect x='3' y='10.5' width='18' height='3' rx='1.5'/%3E%3Crect x='10.5' y='3' width='3' height='18' rx='1.5'/%3E%3C/svg%3E"); mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect x='3' y='10.5' width='18' height='3' rx='1.5'/%3E%3Crect x='10.5' y='3' width='3' height='18' rx='1.5'/%3E%3C/svg%3E"); }
[class*="st-key-krj_hapus_"] { justify-content: flex-end; }
[class*="st-key-krj_hapus_"] button { width: auto; height: 1.9rem; padding: 0 .8rem; border-radius: 999px; background: #B5483A; border: none; white-space: nowrap; }
[class*="st-key-krj_hapus_"] button p { color: #fff !important; font-size: .75rem; }
.baris-total { display: flex; justify-content: space-between; align-items: baseline; font-weight: 800; color: var(--teks); }
.baris-total.besar { font-size: 1.2rem; margin: .7rem 0 .5rem; }
.baris-total.kecil { font-size: .85rem; margin: .4rem 0 .8rem; }
[class*="st-key-cepat_"] button { background: transparent; border: 1.5px solid var(--garis-tebal); border-radius: 999px; font-size: .8rem; min-height: 2.1rem; }

/* ---------- tabel ---------- */
.tabel-bungkus { overflow-x: auto; }
.stApp .tabel { width: 100%; border-collapse: collapse; font-size: .95rem; margin: 0; }
.stApp .tabel th { text-align: left; font-weight: 600; color: var(--lembut); background: transparent; padding: .5rem .6rem; white-space: nowrap; border: none; border-bottom: 1px solid var(--garis); }
.stApp .tabel td { font-weight: 600; color: var(--teks); background: transparent; padding: .7rem .6rem; white-space: nowrap; border: none; border-bottom: 1px solid var(--garis); }
.stApp .tabel tbody tr:last-child td { border-bottom: none; }
.lencana { display: inline-block; padding: .12rem .65rem; border-radius: 999px; font-size: .72rem; font-weight: 700; background: var(--tile); color: var(--teks); }
.lencana-hijau { background: #5E7F57; color: #fff; }

/* ---------- daftar menu ---------- */
.th { font-size: .78rem; font-weight: 600; color: var(--lembut); }
.sel { font-size: .85rem; font-weight: 600; color: var(--teks); }
[class*="st-key-mn_"] button { min-height: 1.8rem; padding: 0 .85rem; border-radius: 999px; white-space: nowrap; }
[class*="st-key-mn_"] button p { font-size: .78rem; }
[class*="st-key-mn_hapus_"] button { background: #B5483A; }
.stApp [class*="st-key-mn_hapus_"] button p { color: #fff; }
"""


def terapkan(gelap: bool = False):
    warna = GELAP if gelap else TERANG
    variabel = ";".join(f"--{k}:{v}" for k, v in warna.items())
    # Baris kosong dibuang supaya Markdown tidak memotong blok <style>.
    css = "\n".join(baris for baris in CSS.splitlines() if baris.strip())
    st.markdown(f"<style>{FONT}:root{{{variabel}}}{css}</style>", unsafe_allow_html=True)