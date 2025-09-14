import mysql.connector

def get_connection():
    """
    Crea y devuelve una conexión a la base de datos MySQL.
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="dist2025"
    )
    return conn

def get_usuarios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT idusuario, nombreUsuario, nombre, apellido, email, rol, clave, telefono, activo FROM dist2025.usuario")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_roles():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT idrol, nombre FROM dist2025.rol")
    rows = cursor.fetchall()
    conn.close()
    return rows