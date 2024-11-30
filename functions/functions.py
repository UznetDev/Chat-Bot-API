import random
import string

def generate_token(length=200):
    """
    Tasodifiy token yaratish uchun funksiya.
    
    Parametrlar:
        length (int): Token uzunligi.

    Qaytaradi:
        str: Yaratilgan token.
    """
    if length <= 0:
        raise ValueError("Token uzunligi musbat bo'lishi kerak.")
    
    # Tasodifiy belgilar to'plami (harflar, raqamlar, va maxsus belgilar)
    characters = string.ascii_letters + string.digits + string.punctuation
    
    # Tokenni yaratish
    token = ''.join(random.choice(characters) for _ in range(length))
    return token

# Funksiyani ishlatish
try:
    token_length = 16  # Token uzunligini kiriting
    token = generate_token(token_length)
    print(f"Yaratilgan token: {token}")
except ValueError as e:
    print(f"Xatolik: {e}")
