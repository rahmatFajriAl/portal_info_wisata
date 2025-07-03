from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User  # Pakai model bawaan Django (inheritance)

#  Abstraksi: Menyembunyikan detail implementasi database dan kita cukup bikin class-nya aja.
#  Enkapsulasi: Semua data destinasi dan ulasan disimpan dan diproses di dalam masing-masing class model.

class KategoriDestinasi(models.Model):  #  Inheritance: Mewarisi dari models.Model
    # Nama dan deskripsi kategori, misalnya "Pantai", "Gunung", dll
    nama = models.CharField(max_length=100, verbose_name=_("Nama Kategori"))  #  Enkapsulasi
    deskripsi = models.TextField(blank=True, null=True, verbose_name=_("Deskripsi"))

    class Meta:
        verbose_name = _("Kategori Destinasi")
        verbose_name_plural = _("Kategori Destinasi")

    def __str__(self):  # 🌀 Polimorfisme: __str__ bisa berbeda tiap model, walau nama fungsi sama
        return self.nama


class DestinasiWisata(models.Model):  # Inheritance
    # Model utama destinasi wisata
    nama = models.CharField(max_length=200, verbose_name=_("Nama Destinasi"))  # 
    deskripsi = models.TextField(verbose_name=_("Deskripsi"))
    lokasi = models.CharField(max_length=255, verbose_name=_("Lokasi"))
    kategori = models.ForeignKey(  # Relasi ke KategoriDestinasi (Many to One)
        KategoriDestinasi,
        on_delete=models.CASCADE,
        related_name='destinasi',
        verbose_name=_("Kategori")
    )
    tanggal_dibuat = models.DateTimeField(auto_now_add=True, verbose_name=_("Tanggal Dibuat"))  # Timestamp otomatis
    tanggal_diperbarui = models.DateTimeField(auto_now=True, verbose_name=_("Tanggal Diperbarui"))

    class Meta:
        verbose_name = _("Destinasi Wisata")
        verbose_name_plural = _("Destinasi Wisata")

    def __str__(self):  # 🌀
        return self.nama


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
