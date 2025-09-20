import bcrypt
import random
import string

def generar_clave(longitud=8):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))

def encriptar_clave(clave):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(clave.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verificar_clave(clave, clave_hash):
    return bcrypt.checkpw(clave.encode('utf-8'), clave_hash.encode('utf-8'))