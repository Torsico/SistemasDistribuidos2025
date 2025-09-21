import bcrypt
import random
import string
import jwt
import datetime

SECRET_KEY = "secretosecretoso468"

def generar_clave(longitud=8):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))

def encriptar_clave(clave):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(clave.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verificar_clave(clave, clave_hash):
    return bcrypt.checkpw(clave.encode('utf-8'), clave_hash.encode('utf-8'))

def generar_token(idusuario, nombreUsuario, rol):
    carga = {
        "idusuario": idusuario,
        "nombreUsuario": nombreUsuario,
        "rol": rol,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }
    return jwt.encode(carga, SECRET_KEY, algorithm="HS256")

def verificar_token(token):
    try:
        carga = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {
                "ok":True,
                "idusuario":carga["idusuario"], 
                "nombreUsuario":carga["nombreUsuario"], 
                "rol":carga["rol"]
                }
    except jwt.ExpiredSignatureError:
        return {"ok": False, "error":"Token expirado"}
    except jwt.InvalidTokenError:
        return {"ok": False, "error":"Token expirado"}