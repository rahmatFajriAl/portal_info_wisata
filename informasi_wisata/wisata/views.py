from django.shortcuts import render, get_object_or_404, redirect
from django.views import View  # Untuk membuat CBV
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import DestinasiWisata, GambarDestinasi, UlasanPengguna, DetailHargaTiket
from .forms import UlasanForm

class HomeView(TemplateView):
    template_name = 'wisata/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['destinasi_terbaru'] = DestinasiWisata.objects.all().order_by('-id')
        return context

class DaftarDestinasiView(TemplateView):
    template_name = 'wisata/destinasi_wisata.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['destinasi_terbaru'] = DestinasiWisata.objects.all().order_by('-id')
        return context

class DetailDestinasiView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, destinasi_id):
        destinasi = get_object_or_404(DestinasiWisata, id=destinasi_id)
        gambar_list = destinasi.gambar.all()
        ulasan_list = UlasanPengguna.objects.filter(destinasi=destinasi).order_by('-tanggal_ulasan')
        harga_list = DetailHargaTiket.objects.filter(destinasi=destinasi, aktif=True)
        form = UlasanForm()

        return render(request, 'detail_destinasi.html', {
            'destinasi': destinasi,
            'gambar_list': gambar_list,
            'ulasan_list': ulasan_list,
            'harga_list': harga_list,
            'form': form,
        })

    def post(self, request, destinasi_id):
        destinasi = get_object_or_404(DestinasiWisata, id=destinasi_id)
        gambar_list = destinasi.gambar.all()
        ulasan_list = UlasanPengguna.objects.filter(destinasi=destinasi).order_by('-tanggal_ulasan')
        harga_list = DetailHargaTiket.objects.filter(destinasi=destinasi, aktif=True)
        form = UlasanForm(request.POST)

        if form.is_valid():
            ulasan = form.save(commit=False)
            ulasan.destinasi = destinasi
            ulasan.pengguna = request.user
            ulasan.save()
            messages.success(request, "Ulasan Anda berhasil dikirim.")
            return redirect('detail_destinasi', destinasi_id=destinasi.id)
        else:
            messages.error(request, "Ulasan gagal dikirim. Mohon periksa input Anda.")

        return render(request, 'detail_destinasi.html', {
            'destinasi': destinasi,
            'gambar_list': gambar_list,
            'ulasan_list': ulasan_list,
            'harga_list': harga_list,
            'form': form,
        })

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'auth/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Halo {user.username}, akun Anda berhasil dibuat!")
            return redirect('home')
        else:
            messages.error(request, "Gagal mendaftar. Mohon periksa formulir.")
        return render(request, 'auth/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'auth/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Selamat datang, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Login gagal. Mohon periksa username dan password.")
        return render(request, 'auth/login.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "Anda telah berhasil logout.")
        return redirect('login')
