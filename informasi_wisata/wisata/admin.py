from django.contrib import admin
from .models import KategoriDestinasi, DestinasiWisata, GambarDestinasi, UlasanPengguna, DetailHargaTiket
from django.utils.html import format_html

# Menampilkan model KategoriDestinasi di admin
@admin.register(KategoriDestinasi)
class KategoriDestinasiAdmin(admin.ModelAdmin):
    list_display = ('nama', 'deskripsi')
    search_fields = ('nama',)


# Inline untuk DetailHargaTiket
class DetailHargaTiketInline(admin.TabularInline):
    model = DetailHargaTiket
    extra = 1
    fields = ('jenis_tiket', 'nama_tiket', 'harga', 'satuan', 'keterangan', 'aktif', 'urutan')
    ordering = ['urutan', 'jenis_tiket']


# Menampilkan form input gambar secara inline di form DestinasiWisata
class GambarDestinasiInline(admin.TabularInline):
    model = GambarDestinasi
    extra = 1


# Menampilkan model DestinasiWisata di admin
@admin.register(DestinasiWisata)
class DestinasiWisataAdmin(admin.ModelAdmin):
    list_display = (
        'nama', 
        'lokasi', 
        'kategori', 
        'harga_tiket', 
        'jumlah_detail_harga',
        'jam_buka', 
        'jam_tutup', 
        'tanggal_dibuat', 
        'tanggal_diperbarui'
    )
    search_fields = ('nama', 'lokasi', 'kategori__nama')
    list_filter = ('kategori', 'tanggal_dibuat')
    inlines = [DetailHargaTiketInline, GambarDestinasiInline]
    readonly_fields = ('tanggal_dibuat', 'tanggal_diperbarui')

    def jumlah_detail_harga(self, obj):
        """Menampilkan jumlah detail harga tiket"""
        count = obj.detail_harga.filter(aktif=True).count()
        if count > 0:
            return format_html(
                '<span style="color: green; font-weight: bold;">{} detail</span>',
                count
            )
        return format_html('<span style="color: red;">Belum ada detail</span>')
    jumlah_detail_harga.short_description = 'Detail Harga'

    def lokasi_link(self, obj):
        query = obj.lokasi.replace(' ', '+')
        url = f"https://www.google.com/maps/search/?api=1&query={query}"
        return format_html(f'<a href="{url}" target="_blank">{obj.lokasi}</a>')
    lokasi_link.short_description = 'Lokasi'


# Admin untuk DetailHargaTiket sebagai model terpisah
@admin.register(DetailHargaTiket)
class DetailHargaTiketAdmin(admin.ModelAdmin):
    list_display = (
        'destinasi', 
        'jenis_tiket', 
        'nama_tiket', 
        'harga_formatted', 
        'satuan', 
        'aktif', 
        'urutan'
    )
    list_filter = ('jenis_tiket', 'aktif', 'destinasi__kategori')
    search_fields = ('destinasi__nama', 'nama_tiket', 'keterangan')
    list_editable = ('aktif', 'urutan')
    ordering = ['destinasi', 'urutan', 'jenis_tiket']
    
    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('destinasi', 'jenis_tiket', 'nama_tiket')
        }),
        ('Harga & Satuan', {
            'fields': ('harga', 'satuan')
        }),
        ('Pengaturan Tampilan', {
            'fields': ('urutan', 'aktif')
        }),
        ('Keterangan', {
            'fields': ('keterangan',),
            'classes': ('collapse',)
        })
    )

    def harga_formatted(self, obj):
        """Format harga dalam Rupiah"""
        return obj.harga_formatted()
    harga_formatted.short_description = 'Harga'
    harga_formatted.admin_order_field = 'harga'


# Menampilkan model GambarDestinasi di admin
@admin.register(GambarDestinasi)
class GambarDestinasiAdmin(admin.ModelAdmin):
    list_display = ('destinasi', 'keterangan')
    search_fields = ('destinasi__nama', 'keterangan')
    list_filter = ('destinasi',)


# Menampilkan model UlasanPengguna di admin
@admin.register(UlasanPengguna)
class UlasanAdmin(admin.ModelAdmin):
    list_display = ('destinasi', 'pengguna', 'rating', 'tanggal_ulasan')
    search_fields = ('destinasi__nama', 'pengguna__username', 'komentar')
    list_filter = ('rating', 'tanggal_ulasan')
    readonly_fields = ('tanggal_ulasan',)