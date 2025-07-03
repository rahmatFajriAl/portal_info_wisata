from django.urls import path  # Untuk membuat daftar URL routing
from . import views  # Mengimpor semua fungsi yang ada di views.py lokal
from wisata.views import home  # Import spesifik fungsi home dari views.py
from django.conf import settings  # Untuk mengakses konfigurasi dari settings.py
from django.conf.urls.static import static  # Untuk menampilkan file media saat DEBUG=True

urlpatterns = [
    path('', views.home, name='home'),  
    #  Abstraksi: Akses halaman utama dengan memanggil fungsi home, tinggal pakai tanpa tahu proses render-nya

    path('destinasi/', views.daftar_destinasi, name='destinasi_wisata'),  
    #  Enkapsulasi: Menampilkan semua destinasi, logikanya disembunyikan di views.daftar_destinasi

    path('destinasi/<int:destinasi_id>/', views.detail_destinasi, name='detail_destinasi'),  
    #  Enkapsulasi: Menampilkan detail berdasarkan ID destinasi, ID-nya diproses aman di views

    #  AUTHENTIKASI
    path('register/', views.register_view, name='register'),  
    # Inheritance + Abstraksi: Menggunakan UserCreationForm bawaan Django untuk register user

    path('login/', views.login_view, name='login'),  
    #  Enkapsulasi: Proses login dan validasi username/password disimpan dalam views.login_view

    path('logout/', views.logout_view, name='logout'),  
    #  Abstraksi: Logout pakai fungsi Django, kita tinggal panggil aja
]
