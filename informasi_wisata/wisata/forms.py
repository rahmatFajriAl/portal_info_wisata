from django import forms
from .models import UlasanPengguna

class UlasanForm(forms.ModelForm):
    class Meta:
        model = UlasanPengguna
        fields = ['rating', 'komentar']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'class': 'form-control',
                'placeholder': 'Masukkan rating 1-5'
            }),
            'komentar': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Tulis ulasan Anda...'
            }),
        }
        labels = {
            'rating': 'Rating (1-5)',
            'komentar': 'Komentar / Ulasan',
        }
