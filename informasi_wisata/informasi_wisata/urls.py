from django.contrib import admin  # Modul untuk halaman admin Django
from django.urls import path, include  # path: untuk mendefinisikan URL, include: menyertakan URL dari app lain

from django.conf import settings  # Mengakses konfigurasi settings.py
from django.conf.urls.static import static  # Untuk menampilkan file media statis (gambar)

urlpatterns = [
    path('', include('wisata.urls')),  # Mengarahkan URL utama ke file urls.py di aplikasi 'wisata'
    path('admin/', admin.site.urls),  # Mengarahkan /admin ke halaman admin Django
]

# Untuk menampilkan file gambar dari MEDIA_URL saat DEBUG=True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
    # Menyediakan akses ke file media (seperti gambar yang diunggah) saat mode development
