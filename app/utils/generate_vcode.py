import random
import string

def generate_vcode():
    first_part = ''.join(random.choices(string.ascii_uppercase, k=4))
    second_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    id_value = first_part + second_part
    return id_value