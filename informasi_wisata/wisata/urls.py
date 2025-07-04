from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    HomeView,
    DaftarDestinasiView,
    DetailDestinasiView,
    RegisterView,
    LoginView,
    LogoutView,
)

urlpatterns = [
    # Halaman utama
    path('', HomeView.as_view(), name='home'),  # Abstraksi: render home tanpa tahu isi logikanya

    # Daftar semua destinasi
    path('destinasi/', DaftarDestinasiView.as_view(), name='destinasi_wisata'),  # Enkapsulasi: logika tersembunyi di dalam class view

    # Detail destinasi (hanya untuk user login)
    path('destinasi/<int:destinasi_id>/', DetailDestinasiView.as_view(), name='detail_destinasi'),

    # Autentikasi
    path('register/', RegisterView.as_view(), name='register'),  # Inheritance dari View
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

# Menambahkan static/media jika dalam mode DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
