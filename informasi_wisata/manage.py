#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os  # Modul untuk mengakses environment dan path
import sys  # Modul untuk akses ke argumen command-line


def main():
    """Run administrative tasks."""  # Fungsi utama untuk menjalankan perintah administratif
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'informasi_wisata.settings')  
    # Menentukan file settings default dari proyek Django

    try:
        from django.core.management import execute_from_command_line  
        # Mengimpor fungsi eksekusi perintah Django (abstraksi – kita tinggal pakai aja)
    except ImportError as exc:
        # Jika Django tidak ditemukan, munculkan pesan error yang jelas
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)
    # Menjalankan perintah dari terminal seperti runserver, migrate, dll (abstraksi)


if __name__ == '__main__':
    main()
    # Menjalankan fungsi main() saat file ini dijalankan langsung (bukan diimport)
