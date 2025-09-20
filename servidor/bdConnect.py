import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="dist2025"
    )
    return conn

# Consultas de Usuario

def get_usuarios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT idusuario, nombreUsuario, nombre, apellido, email, rol, clave, telefono, activo FROM dist2025.usuario")
    rows = cursor.fetchall()
    conn.close()
    return rows

def alta_usuario(nombreUsuario, nombre, apellido, email, rol, clave, telefono, activo):
    try:
        conn =  get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO usuarios (nombreUsuario, nombre, apellido, email, rol, clave, telefono, activo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (nombreUsuario, nombre, apellido, email, rol, clave, telefono, activo)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("Error al cargar")
        return False
    
def mod_usuario(idusuario, nombreUsuario, nombre, apellido, email, rol, clave, telefono, activo):
    try:
        conn =  get_connection()
        cursor = conn.cursor()
        sql = "UPDATE usuarios SET nombreUsuario = %s, nombre = %s, apellido = %s, email = %s, rol = = %s, telefono = %s, activo = %s WHERE idusuario = %s"
        values = (nombreUsuario, nombre, apellido, email, rol, clave, telefono, activo)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("Error al cargar")
        return False
    
def baja_usuario(idusuario):
    try:
        conn =  get_connection()
        cursor = conn.cursor()
        sql = "UPDATE usuarios SET activo = false WHERE idusuario = %s"
        values = (idusuario)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("Error al cargar")
        return False

# ...

def get_roles():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT idrol, nombre FROM dist2025.rol")
    rows = cursor.fetchall()
    conn.close()
    return rows