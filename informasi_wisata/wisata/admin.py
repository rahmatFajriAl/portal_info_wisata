from django.contrib import admin
from .models import KategoriDestinasi, DestinasiWisata, GambarDestinasi, UlasanPengguna
from django.utils.html import format_html  # digunakan untuk membuat HTML custom dalam admin panel

# Menampilkan model KategoriDestinasi di admin
@admin.register(KategoriDestinasi)
class KategoriDestinasiAdmin(admin.ModelAdmin):
    list_display = ('nama', 'deskripsi')  # kolom yang akan ditampilkan di list view
    search_fields = ('nama',)  # fitur pencarian berdasarkan nama

# Menampilkan form input gambar secara inline di form DestinasiWisata
class GambarDestinasiInline(admin.TabularInline):
    model = GambarDestinasi  # model yang di-inline-kan
    extra = 1  # jumlah form kosong yang ditampilkan untuk tambah data

# Menampilkan model DestinasiWisata di admin
@admin.register(DestinasiWisata)
class DestinasiWisataAdmin(admin.ModelAdmin):
    list_display = ('nama', 'lokasi', 'kategori', 'tanggal_dibuat', 'tanggal_diperbarui')  # kolom yang ditampilkan
    search_fields = ('nama', 'lokasi', 'kategori__nama')  # pencarian berdasarkan nama, lokasi, dan kategori
    list_filter = ('kategori', 'tanggal_dibuat')  # filter di sidebar
    inlines = [GambarDestinasiInline]  # menampilkan gambar terkait dalam form destinasi
    readonly_fields = ('tanggal_dibuat', 'tanggal_diperbarui')  # hanya baca (tidak bisa diubah)

    def lokasi_link(self, obj):
        # Membuat link Google Maps dari lokasi destinasi
        query = obj.lokasi.replace(' ', '+')
        url = f"https://www.google.com/maps/search/?api=1&query={query}"
        return format_html(f'<a href="{url}" target="_blank">{obj.lokasi}</a>')  # tampilkan sebagai HTML

    lokasi_link.short_description = 'Lokasi'  # label kolom custom

# Menampilkan model GambarDestinasi di admin
@admin.register(GambarDestinasi)
class GambarDestinasiAdmin(admin.ModelAdmin):
    list_display = ('destinasi', 'keterangan')  # kolom yang ditampilkan
    search_fields = ('destinasi__nama', 'keterangan')  # pencarian berdasarkan nama destinasi dan keterangan
    list_filter = ('destinasi',)  # filter berdasarkan destinasi

# Menampilkan model UlasanPengguna di admin
@admin.register(UlasanPengguna)
class UlasanAdmin(admin.ModelAdmin):
    list_display = ('destinasi', 'pengguna', 'rating', 'tanggal_ulasan')  # kolom yang ditampilkan
    search_fields = ('destinasi__nama', 'pengguna__username', 'komentar')  # fitur pencarian
    list_filter = ('rating', 'tanggal_ulasan')  # filter di sidebar
    readonly_fields = ('tanggal_ulasan',)  # kolom tidak bisa diubah (readonly)
