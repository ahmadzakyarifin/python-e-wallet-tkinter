import re

def is_valid_email(email):
    """Memeriksa apakah email memiliki format yang valid."""
    # Regex ketat untuk validasi email
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def is_valid_phone(phone):
    """Memeriksa apakah nomor telepon merupakan nomor ponsel Indonesia yang valid."""
    # Dimulai dengan 08, diikuti oleh 8-11 digit (total 10-13 digit)
    pattern = r"^08\d{8,11}$"
    return re.match(pattern, phone) is not None

def is_valid_password(password):
    """
    Memeriksa apakah password memenuhi persyaratan kompleksitas:
    - Minimal 8 karakter
    - Minimal satu huruf
    - Minimal satu angka
    """
    if len(password) < 8:
        return False
    if not re.search(r"[a-zA-Z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    return True

def is_valid_username(username):
    """Memeriksa apakah username valid (dilonggarkan)."""
    # Izinkan username apa saja selama tidak kosong
    return len(username) > 0

def is_valid_pln_number(no_meter):
    """Memeriksa apakah nomor PLN valid (11-12 digit)."""
    # Hapus spasi (jika ada yang terlewat, meskipun view seharusnya sudah menghapusnya)
    no_meter = no_meter.strip()
    return no_meter.isdigit() and 11 <= len(no_meter) <= 12
