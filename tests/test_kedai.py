"""Pengujian logika aplikasi. Jalankan dari folder proyek:
    python -m unittest discover -s tests -v
"""
import unittest

from controllers.kedai_controller import KedaiController
from database.dao import MenuDAO, TransaksiDAO
from database.database_manager import DatabaseManager
from models import (Kasir, Makanan, Menu, Minuman, Orang, Pelanggan,
                    PembayaranKurangError, Pelayanan, Pesanan)


class TestMenu(unittest.TestCase):
    def test_menu_abstract_tidak_bisa_dibuat(self):
        with self.assertRaises(TypeError):
            Menu("X", 1000)

    def test_polymorphism_info_menu(self):
        minuman, makanan = Minuman("Latte", 25000, "Kopi"), Makanan("Roti Bakar", 17000, "Makanan Ringan")
        self.assertTrue(minuman.info_menu().startswith("[Minuman]"))
        self.assertTrue(makanan.info_menu().startswith("[Makanan]"))

    def test_factory_dan_inheritance(self):
        m = Menu.buat("Minuman", "Matcha", 26000, "Non-Kopi")
        self.assertIsInstance(m, Minuman)
        self.assertIsInstance(m, Menu)
        with self.assertRaises(ValueError):
            Menu.buat("Kopi", "X", 1000, "Kopi")          # kategori lama sudah tidak ada

    def test_jenis_mengikuti_kategori(self):
        self.assertEqual(Menu.daftar_kategori(), ["Minuman", "Makanan"])
        self.assertEqual(Menu.daftar_jenis("Minuman"), ["Kopi", "Non-Kopi", "Susu"])
        self.assertEqual(Menu.daftar_jenis("Makanan"), ["Makanan Ringan", "Makanan Berat", "Cemilan"])
        with self.assertRaises(ValueError):
            Minuman("Es Teh", 8000, "Cemilan")              # Cemilan bukan jenis minuman
        with self.assertRaises(ValueError):
            Makanan("Roti", 8000, "Susu")                   # Susu bukan jenis makanan
        self.assertEqual(Makanan("Kentang", 15000, "cemilan").jenis, "Cemilan")
        self.assertEqual(Minuman("Es Teh", 8000, "non-kopi").jenis, "Non-Kopi")

    def test_ikon_sesuai_jenis(self):
        self.assertEqual(Minuman("A", 1000, "Kopi").ikon, "☕")
        self.assertEqual(Minuman("B", 1000, "Susu").ikon, "🥛")
        self.assertEqual(Makanan("C", 1000, "Cemilan").ikon, "🍟")

    def test_validasi_encapsulation(self):
        m = Minuman("Espresso", 18000, "Kopi")
        m.ubah_harga(20000)
        self.assertEqual(m.harga, 20000)
        for salah in (0, -5, "abc"):
            with self.assertRaises(ValueError):
                m.ubah_harga(salah)
        with self.assertRaises(ValueError):
            Minuman("  ", 1000, "Kopi")


class TestPesananDanTransaksi(unittest.TestCase):
    def setUp(self):
        self.kopi = Minuman("Kopi Susu", 22000, "Kopi", 1)
        self.roti = Makanan("Croissant", 20000, "Makanan Ringan", 2)

    def test_hitung_total_dan_item(self):
        p = Pesanan()
        p.tambah_item(self.kopi, 2)
        p.tambah_item(self.roti)
        p.tambah_item(self.kopi)                       # menu sama: jumlah bertambah
        self.assertEqual(len(p.daftar_item), 2)
        self.assertEqual(p.hitung_total(), 3 * 22000 + 20000)

    def test_ubah_dan_hapus_item(self):
        p = Pesanan()
        p.tambah_item(self.kopi, 2)
        p.ubah_jumlah(self.kopi, 5)
        self.assertEqual(p.hitung_total(), 5 * 22000)
        p.ubah_jumlah(self.kopi, 0)                    # 0 = hapus
        self.assertTrue(p.kosong)

    def test_pembayaran_dan_kembalian(self):
        kasir = Kasir("Azhalia")
        p = Pesanan("Dina")
        p.tambah_item(self.kopi, 2)
        t = kasir.proses_pesanan(p, 50000)
        self.assertEqual(t.total, 44000)
        self.assertEqual(t.kembalian, 6000)
        self.assertEqual(p.status, Pesanan.STATUS_DIBAYAR)

    def test_uang_kurang_ditolak(self):
        kasir = Kasir("Azhalia")
        p = Pesanan()
        p.tambah_item(self.kopi)
        with self.assertRaises(PembayaranKurangError):
            kasir.proses_pesanan(p, 10000)
        self.assertEqual(p.status, Pesanan.STATUS_BARU)

    def test_pesanan_kosong_ditolak(self):
        with self.assertRaises(ValueError):
            Kasir("Azhalia").proses_pesanan(Pesanan(), 10000)

    def test_struk_memuat_data(self):
        p = Pesanan("Dina")
        p.tambah_item(self.kopi)
        t = Kasir("Azhalia").proses_pesanan(p, 25000, "0812")
        struk = t.cetak_struk()
        for teks in ("Azhalia", "Dina", "0812", "Kopi Susu", "Rp 22.000", "Rp 3.000"):
            self.assertIn(teks, struk)


class TestOrang(unittest.TestCase):
    def test_inheritance_dan_interface(self):
        kasir, pelanggan = Kasir("Azhalia"), Pelanggan("Dina", "0812")
        self.assertIsInstance(kasir, Orang)
        self.assertIsInstance(kasir, Pelayanan)
        self.assertIsInstance(pelanggan, Orang)
        self.assertNotEqual(kasir.info(), pelanggan.info())       # polymorphism

    def test_ubah_nama_kasir(self):
        kasir = Kasir("Azhalia")
        kasir.ubah_nama("Nafis")
        self.assertEqual(kasir.nama, "Nafis")
        with self.assertRaises(ValueError):
            kasir.ubah_nama("")

    def test_interface_tidak_bisa_dibuat(self):
        with self.assertRaises(TypeError):
            Pelayanan()


class TestDatabase(unittest.TestCase):
    def setUp(self):
        DatabaseManager.reset()
        self.db = DatabaseManager.get_instance(":memory:")

    def tearDown(self):
        DatabaseManager.reset()

    def test_singleton(self):
        self.assertIs(DatabaseManager.get_instance(), DatabaseManager.get_instance())
        self.assertIs(DatabaseManager(), self.db)

    def test_menu_dao_crud(self):
        dao = MenuDAO(self.db)
        m = dao.simpan(Minuman("Latte", 25000, "Susu"))
        self.assertIsNotNone(m.id)
        m.ubah_harga(27000)
        dao.simpan(m)
        dibaca = dao.cari_id(m.id)
        self.assertIsInstance(dibaca, Minuman)
        self.assertEqual(dibaca.harga, 27000)
        dao.hapus(m.id)
        self.assertIsNone(dao.cari_id(m.id))

    def test_migrasi_data_versi_lama(self):
        dao = MenuDAO(self.db)
        for kat, nama, jenis in (("Kopi", "Latte", "Susu"), ("Non-Kopi", "Teh", "Teh"),
                                 ("Makanan", "Roti Bakar", "Roti"), ("Makanan", "Bakso", "Lainnya"), ("Makanan", "Nasi Goreng", "Makanan Berat")):
            self.db.execute("INSERT INTO menu (nama, kategori, jenis, harga) VALUES (?,?,?,?)",
                            (nama, kat, jenis, 10000))
        dao.migrasi_data_lama()
        dao.migrasi_data_lama()                                   # aman dijalankan ulang
        hasil = {m.nama: (m.kategori, m.jenis) for m in dao.semua()}
        self.assertEqual(hasil["Latte"], ("Minuman", "Kopi"))
        self.assertEqual(hasil["Teh"], ("Minuman", "Non-Kopi"))
        self.assertEqual(hasil["Roti Bakar"], ("Makanan", "Makanan Ringan"))      # jenis lama diganti ke pilihan pertama
        self.assertEqual(hasil["Bakso"], ("Makanan", "Makanan Ringan"))
        self.assertEqual(hasil["Nasi Goreng"], ("Makanan", "Makanan Berat"))   # jenis yang valid tidak diubah

    def test_transaksi_dao_simpan_dan_cari(self):
        dao = TransaksiDAO(self.db)
        kasir = Kasir("Azhalia")
        for nama, kopi in (("Dina", "Latte"), ("Rafi", "Americano")):
            p = Pesanan(nama)
            p.tambah_item(Minuman(kopi, 20000, "Kopi", 1), 2)
            dao.simpan(kasir.proses_pesanan(p, 50000))
        semua = dao.semua()
        self.assertEqual([t.id_transaksi for t in semua], ["TRX-0002", "TRX-0001"])
        self.assertEqual([t.pelanggan for t in dao.cari("dina")], ["Dina"])
        self.assertEqual(len(dao.cari("Americano")), 1)            # cari lewat nama produk
        self.assertEqual(len(dao.cari("TRX-0001")), 1)
        self.assertEqual(dao.cari("tidak-ada"), [])
        self.assertEqual(dao.ringkasan(), (2, 80000))
        self.assertEqual(dao.menu_terlaris()[1], 2)


class TestController(unittest.TestCase):
    def setUp(self):
        DatabaseManager.reset()
        self.ctrl = KedaiController(":memory:")

    def tearDown(self):
        DatabaseManager.reset()

    def test_menu_awal_dan_filter(self):
        self.assertEqual(len(self.ctrl.daftar_menu()), 10)
        self.assertEqual(len(self.ctrl.daftar_menu("Makanan")), 2)
        self.assertEqual(len(self.ctrl.daftar_menu("Minuman")), 8)
        self.assertEqual(len(self.ctrl.daftar_menu(kata="kopi")), 1)

    def test_tambah_ubah_hapus_menu(self):
        m = self.ctrl.tambah_menu("Minuman", "Vietnam Drip", "Kopi", 24000)
        self.assertEqual(len(self.ctrl.daftar_menu()), 11)
        self.ctrl.ubah_menu(m.id, "Makanan", "Roti Keju", "Makanan Ringan", 25000)
        self.assertEqual(self.ctrl.cari_menu(m.id).kategori, "Makanan")
        with self.assertRaises(ValueError):
            self.ctrl.tambah_menu("Makanan", "Salah", "Susu", 5000)   # jenis tidak cocok kategori
        m2 = self.ctrl.tambah_menu("Makanan", "Kentang Goreng", "Cemilan", 15000)
        self.assertEqual(self.ctrl.cari_menu(m2.id).jenis, "Cemilan")
        self.ctrl.hapus_menu(m2.id)
        self.ctrl.hapus_menu(m.id)
        self.assertEqual(len(self.ctrl.daftar_menu()), 10)

    def test_alur_lengkap_pemesanan(self):
        self.assertEqual(self.ctrl.ringkasan()["jumlah_transaksi"], 0)
        p = self.ctrl.pesanan_baru()
        p.tambah_item(self.ctrl.daftar_menu()[3], 2)
        t = self.ctrl.bayar(p, 50000, "Dina", "0812")
        self.assertEqual(t.id_transaksi, "TRX-0001")
        self.assertEqual(t.kembalian, 6000)
        r = self.ctrl.ringkasan()
        self.assertEqual((r["jumlah_transaksi"], r["total_pendapatan"]), (1, 44000))
        self.assertEqual(r["menu_terlaris"], ("Kopi Susu Gula Aren", 2))

    def test_riwayat_tidak_berubah_walau_harga_menu_berubah(self):
        menu = self.ctrl.daftar_menu()[0]
        p = self.ctrl.pesanan_baru()
        p.tambah_item(menu)
        self.ctrl.bayar(p, 20000)
        self.ctrl.ubah_menu(menu.id, menu.kategori, menu.nama, menu.jenis, 99000)
        self.assertEqual(self.ctrl.cari_riwayat("")[0].total, 18000)

    def test_ganti_nama_kasir_tercatat_di_transaksi(self):
        self.ctrl.ganti_nama_kasir("Nafis")
        p = self.ctrl.pesanan_baru()
        p.tambah_item(self.ctrl.daftar_menu()[0])
        self.assertEqual(self.ctrl.bayar(p, 20000).kasir, "Nafis")


if __name__ == "__main__":
    unittest.main()