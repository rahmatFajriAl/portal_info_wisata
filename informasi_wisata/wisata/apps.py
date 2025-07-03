from django.apps import AppConfig
from django.contrib import admin

# Konfigurasi utama untuk aplikasi "wisata"
class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Gunakan tipe ID otomatis sebagai default
    name = 'wisata'  # Nama aplikasi, harus sesuai dengan nama folder app

    def ready(self):
        # Akan dipanggil saat aplikasi siap (saat Django mulai)
        
        # Konfigurasi tampilan admin
        admin.site.site_header = "Info Wisata Admin"  # Header utama di halaman admin
        admin.site.site_title = "Info Wisata Admin"  # Judul tab browser admin
        admin.site.index_title = "Selamat datang di Info Wisata Admin Panel"  # Judul halaman index
        
        # Tambahkan kustomisasi ke model admin
        self.customize_admin_models()

    def customize_admin_models(self):
        # Impor model yang ingin dikustomisasi
        from .models import KategoriDestinasi, DestinasiWisata, GambarDestinasi, UlasanPengguna

        # Mengubah nama yang tampil di panel admin dengan menambahkan emoji/deskripsi
        
        KategoriDestinasi._meta.verbose_name = "Kategori Destinasi"
        KategoriDestinasi._meta.verbose_name_plural = "🏷️ Kategori Destinasi"  # Tampil di sidebar admin

        DestinasiWisata._meta.verbose_name = "Destinasi Wisata"
        DestinasiWisata._meta.verbose_name_plural = "🏝️ Destinasi Wisata"

        GambarDestinasi._meta.verbose_name = "Gambar Destinasi"
        GambarDestinasi._meta.verbose_name_plural = "📸 Gambar Destinasi"

        UlasanPengguna._meta.verbose_name = "Ulasan Pengguna"
        UlasanPengguna._meta.verbose_name_plural = "⭐ Ulasan Pengguna"
