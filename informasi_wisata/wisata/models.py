from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User  # Pakai model bawaan Django (inheritance)

#  Abstraksi: Menyembunyikan detail implementasi database dan kita cukup bikin class-nya aja.
#  Enkapsulasi: Semua data destinasi dan ulasan disimpan dan diproses di dalam masing-masing class model.

class KategoriDestinasi(models.Model):  #  Inheritance: Mewarisi dari models.Model
    # Nama dan deskripsi kategori, misalnya "Pantai", "Gunung", dll
    nama = models.CharField(max_length=100, verbose_name=_("Nama Kategori"))  #  Enkapsulasi
    deskripsi = models.TextField(blank=True, null=True, 
                                 verbose_name=_("Deskripsi"))

    class Meta:
        verbose_name = _("Kategori Destinasi")
        verbose_name_plural = _("Kategori Destinasi")

    def __str__(self):  # 🌀 Polimorfisme: __str__ bisa berbeda tiap model, walau nama fungsi sama
        return self.nama


class DestinasiWisata(models.Model):
    nama = models.CharField(max_length=100)
    lokasi = models.CharField(max_length=255)
    kategori = models.ForeignKey(KategoriDestinasi, on_delete=models.CASCADE)
    deskripsi = models.TextField()
    harga_tiket = models.CharField(max_length=50, default="Gratis")
    jam_buka = models.TimeField(null=True, blank=True)
    jam_tutup = models.TimeField(null=True, blank=True)
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)
    tanggal_diperbarui = models.DateTimeField(auto_now=True)

    def __str__(self):  # Polimorfisme
        return self.nama


class DetailHargaTiket(models.Model):
    """Model untuk menyimpan detail harga tiket per destinasi"""
    JENIS_TIKET_CHOICES = [
        ('masuk_lokal', 'Tiket Masuk Turis Lokal'),
        ('masuk_asing', 'Tiket Masuk Turis Asing'),
        ('parkir_motor', 'Parkir Motor'),
        ('parkir_mobil', 'Parkir Mobil'),
        ('parkir_bus', 'Parkir Bus'),
        ('wahana', 'Wahana Tambahan'),
        ('guide', 'Guide/Pemandu'),
        ('other', 'Lainnya'),
    ]
    
    destinasi = models.ForeignKey(
        DestinasiWisata,
        on_delete=models.CASCADE,
        related_name='detail_harga',
        verbose_name=_("Destinasi")
    )
    jenis_tiket = models.CharField(
        max_length=20,
        choices=JENIS_TIKET_CHOICES,
        verbose_name=_("Jenis Tiket")
    )
    nama_tiket = models.CharField(
        max_length=100,
        verbose_name=_("Nama Tiket"),
        help_text=_("Contoh: Tiket Masuk Pantai Gigi Hiu")
    )
    harga = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Harga (Rp)")
    )
    satuan = models.CharField(
        max_length=50,
        default="orang",
        verbose_name=_("Satuan"),
        help_text=_("Contoh: orang, motor, mobil, group")
    )
    keterangan = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Keterangan Tambahan")
    )
    aktif = models.BooleanField(
        default=True,
        verbose_name=_("Aktif")
    )
    urutan = models.PositiveSmallIntegerField(
        default=1,
        verbose_name=_("Urutan Tampil")
    )

    class Meta:
        verbose_name = _("Detail Harga Tiket")
        verbose_name_plural = _("Detail Harga Tiket")
        ordering = ['urutan', 'jenis_tiket']
        unique_together = ['destinasi', 'jenis_tiket', 'nama_tiket']

    def __str__(self):
        return f"{self.destinasi.nama} - {self.nama_tiket}: Rp{self.harga:,.0f}/{self.satuan}"

    def harga_formatted(self):
        """Return formatted price in Indonesian Rupiah"""
        return f"Rp{self.harga:,.0f}"


class GambarDestinasi(models.Model):  # Inheritance
    # Menyimpan gambar untuk tiap destinasi wisata
    destinasi = models.ForeignKey(  # Relasi ke DestinasiWisata
        DestinasiWisata,
        on_delete=models.CASCADE,
        related_name='gambar'
    )
    gambar = models.ImageField(  # Field khusus untuk upload gambar
        upload_to='gambar_destinasi/',
        verbose_name=_("Gambar")
    )
    keterangan = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Keterangan")
    )

    class Meta:
        verbose_name = _("Gambar Destinasi")
        verbose_name_plural = _("Gambar Destinasi")

    def __str__(self):  # 🌀
        return f"{self.destinasi.nama} - {self.keterangan or _('Gambar')}"


class UlasanPengguna(models.Model):  # Inheritance
    # Model ulasan oleh user terhadap destinasi
    destinasi = models.ForeignKey(  # Relasi ke DestinasiWisata
        DestinasiWisata,
        on_delete=models.CASCADE,
        related_name='ulasan',
        verbose_name=_("Destinasi")
    )
    pengguna = models.ForeignKey(  # Relasi ke model User bawaan Django
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Pengguna")
    )
    rating = models.PositiveSmallIntegerField(verbose_name=_("Rating (1-5)"))  # Angka rating 1-5
    komentar = models.TextField(blank=True, verbose_name=_("Komentar"))  # Ulasan teks opsional
    tanggal_ulasan = models.DateTimeField(auto_now_add=True, verbose_name=_("Tanggal Ulasan"))

    class Meta:
        verbose_name = _("Ulasan Pengguna")
        verbose_name_plural = _("Ulasan Pengguna")
        ordering = ['-tanggal_ulasan']  # Default urutan berdasarkan tanggal terbaru

    def __str__(self):  # 🌀
        return f"{self.pengguna.username} - {self.destinasi.nama} ({self.rating})"