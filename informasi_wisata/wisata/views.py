from django.shortcuts import render, get_object_or_404, redirect  # Abstraksi: fungsi bantu untuk tampilkan halaman, redirect, atau ambil objek
from django.contrib.auth import login, logout, authenticate  # Abstraksi: fungsi otentikasi bawaan Django
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # Inheritance: form turunan dari class Django untuk register dan login
from django.contrib.auth.decorators import login_required  # Enkapsulasi: hanya user login yang boleh akses
from django.contrib import messages  #Enkapsulasi: untuk munculkan pesan ke pengguna
from .models import DestinasiWisata, GambarDestinasi, UlasanPengguna  # Mengakses data yang terenkapsulasi di model
from .forms import UlasanForm  # Inheritance: form custom untuk ulasan

# Halaman Beranda
def home(request):
    destinasi_terbaru = DestinasiWisata.objects.all().order_by('-id')  # Ambil data terbaru dari model
    return render(request, 'wisata/home.html', {'destinasi_terbaru': destinasi_terbaru})  # Abstraksi: render halaman

# Halaman Daftar Semua Destinasi
def daftar_destinasi(request):
    destinasi_terbaru = DestinasiWisata.objects.all().order_by('-id')  # Data terenkapsulasi di dalam model
    return render(request, 'wisata/destinasi_wisata.html', {'destinasi_terbaru': destinasi_terbaru})

# Halaman Detail Destinasi + Form Ulasan
@login_required(login_url='/login/')  # Enkapsulasi: hanya bisa diakses jika sudah login
def detail_destinasi(request, destinasi_id):
    destinasi = get_object_or_404(DestinasiWisata, id=destinasi_id)  # Abstraksi: ambil data atau tampilkan 404
    gambar_list = destinasi.gambar.all()  # Ambil semua gambar dari relasi
    ulasan_list = UlasanPengguna.objects.filter(destinasi=destinasi).order_by('-tanggal_ulasan')  # Data terenkripsi di dalam model

    if request.method == 'POST':
        form = UlasanForm(request.POST)  # Form turunan UlasanForm
        if form.is_valid():  # Polimorfisme: is_valid() berlaku di semua form
            ulasan = form.save(commit=False)  # Abstraksi: simpan form tanpa langsung ke DB
            ulasan.destinasi = destinasi  # Isi data relasi secara eksplisit
            ulasan.pengguna = request.user
            ulasan.save()  # Abstraksi: simpan ke DB
            messages.success(request, "Ulasan Anda berhasil dikirim.")
            return redirect('detail_destinasi', destinasi_id=destinasi.id)
        else:
            messages.error(request, "Ulasan gagal dikirim. Mohon periksa input Anda.")
    else:
        form = UlasanForm()

    return render(request, 'detail_destinasi.html', {
        'destinasi': destinasi,
        'gambar_list': gambar_list,
        'ulasan_list': ulasan_list,
        'form': form,
    })

# === AUTH ===

# Register (Daftar User Baru)
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # Inheritance: form bawaan Django
        if form.is_valid():  # Polimorfisme: method umum di semua form Django
            user = form.save()  # Abstraksi: simpan user baru
            login(request, user)  #  Login otomatis
            messages.success(request, f"Halo {user.username}, akun Anda berhasil dibuat!")
            return redirect('home')
        else:
            messages.error(request, "Gagal mendaftar. Mohon periksa formulir.")
    else:
        form = UserCreationForm()

    return render(request, 'auth/register.html', {'form': form})

# Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)  #  Inheritance: form bawaan Django
        if form.is_valid():
            user = form.get_user()  #  Ambil user dari data login
            login(request, user)  #  Login user
            messages.success(request, f"Selamat datang, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Login gagal. Mohon periksa username dan password.")
    else:
        form = AuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})

# Logout
def logout_view(request):
    logout(request)  # Abstraksi: keluar dari akun
    messages.info(request, "Anda telah berhasil logout.")
    return redirect('login')
