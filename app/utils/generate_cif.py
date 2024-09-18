import random
import string

def generate_random_cif():
    # Generate 2 random alphabetic characters
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    # Generate 3 random digits
    digits = ''.join(random.choices(string.digits, k=3))
    # Combine letters and digits to form the CIF
    return letters + digits