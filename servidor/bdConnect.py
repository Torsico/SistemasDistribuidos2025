import mysql.connector

from security import verificar_clave
from datetime import datetime

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="dist2025"
    )
    return conn

# Login

def verificar_usuario(usuario, clave):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT idusuario, clave, nombreUsuario, rol FROM dist2025.usuario WHERE nombreUsuario = %s OR email = %s"
    cursor.execute(query, (usuario, usuario))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return False, "Usuario o email inexistente", None

    idusuario, clave_guardada, nombreUsuario, rol = row

    # Caso 1: la clave es hash
    if clave_guardada.startswith("$2a$") or clave_guardada.startswith("$2b$") or clave_guardada.startswith("$2y$"):
        if not verificar_clave(clave, clave_guardada):
            return False, "Clave incorrecta", None
    else:
    # Caso 2: clave normal (casos de prueba)
        if clave != clave_guardada:
            return False, "Clave incorrecta", None

    return True, "Login exitoso", idusuario, nombreUsuario, rol

# Consultas de Usuario

def get_usuarios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT idusuario, nombreUsuario, nombre, apellido, email, rol, clave, telefono, activo FROM dist2025.usuario")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_usuario(idusuario):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT idusuario, nombreUsuario, nombre, apellido, email, rol, clave, telefono, activo FROM dist2025.usuario WHERE idusuario = %s",(idusuario,))
    row = cursor.fetchone()
    conn.close()
    return row

def alta_usuario(nombreUsuario, nombre, apellido, email, rol, clave, telefono, activo):
    try:
        conn =  get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO usuario (nombreUsuario, nombre, apellido, email, rol, clave, telefono, activo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (nombreUsuario, nombre, apellido, email, rol, clave, telefono, activo)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("Error al cargar:", e)
        return False
    
def mod_usuario(idusuario, nombreUsuario, nombre, apellido, rol, telefono, activo):
    try:
        conn =  get_connection()
        cursor = conn.cursor()
        sql = "UPDATE usuario SET nombreUsuario = %s, nombre = %s, apellido = %s, rol = %s, telefono = %s, activo = %s WHERE idusuario = %s"
        values = (nombreUsuario, nombre, apellido, rol, telefono, activo, idusuario)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("Error al cargar:", e)
        return False
    
def baja_usuario(idusuario):
    try:
        conn =  get_connection()
        cursor = conn.cursor()
        sql = "UPDATE usuario SET activo = false WHERE idusuario = %s"
        values = (idusuario,)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("Error al cargar:", e)
        return False

# Consulta de Donaciones

def get_donaciones():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT iddonaciones, categoria, descripcion, cantidad, eliminado, fecha_alta, fecha_mod, usuario_alta, usuario_mod FROM dist2025.donaciones")
    rows = cursor.fetchall()
    conn.close()
    return rows

def alta_donaciones(categoria, descripcion, cantidad, eliminado, fecha_alta, usuario_alta):
    try:
        conn =  get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO donaciones (categoria, descripcion, cantidad, eliminado, fecha_alta, usuario_alta) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (categoria, descripcion, cantidad, eliminado, fecha_alta, usuario_alta)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("Error al cargar:", e)
        return False

def mod_donaciones(iddonaciones, descripcion, cantidad, usuario_mod):
    try:
        conn =  get_connection()
        cursor = conn.cursor()
        now = datetime.now()
        sql = "UPDATE donaciones SET descripcion = %s, cantidad = %s, fecha_mod = %s, usuario_mod = %s WHERE iddonaciones = %s"
        values = (descripcion, cantidad, now, usuario_mod, iddonaciones)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("Error al cargar:", e)
        return False
    
def baja_donaciones(iddonaciones, usuario_mod):
    try:
        conn =  get_connection()
        cursor = conn.cursor()
        now = datetime.now()
        sql = "UPDATE donaciones SET eliminado = true, fecha_mod = %s, usuario_mod = %s WHERE iddonaciones = %s"
        values = (now, usuario_mod, iddonaciones)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("Error al cargar:", e)
        return False
# ...

def get_roles():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT idrol, nombre FROM dist2025.rol")
    rows = cursor.fetchall()
    conn.close()
    return rows