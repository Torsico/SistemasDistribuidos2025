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

def obtener_usuario(usuario):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT idusuario, nombreUsuario, nombre, apellido, email, rol, clave, telefono, activo FROM dist2025.usuario WHERE nombreUsuario = %s",(usuario,))
    row = cursor.fetchone()
    conn.close()
    return row

def verificar_usuario(usuario, clave):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT idusuario, clave, nombreUsuario, rol FROM dist2025.usuario WHERE nombreUsuario = %s OR email = %s"
    cursor.execute(query, (usuario, usuario))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return False, "Usuario o email inexistente", None, None, None

    idusuario, clave_guardada, nombreUsuario, rol = row

    clave = clave.strip()
    clave_guardada = clave_guardada.strip()

    # Caso 1: la clave es hash
    if clave_guardada.startswith("$2a$") or clave_guardada.startswith("$2b$") or clave_guardada.startswith("$2y$"):
        if not verificar_clave(clave, clave_guardada):
            return False, "Clave incorrecta", None, None, None
    else:
    # Caso 2: clave normal (casos de prueba)
        if clave != clave_guardada:
            return False, "Clave incorrecta", None, None, None

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
        now = datetime.now()
        sql = "INSERT INTO donaciones (categoria, descripcion, cantidad, eliminado, fecha_alta, fecha_mod, usuario_alta, usuario_mod) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (categoria, descripcion, cantidad, eliminado, now, now, usuario_alta, usuario_alta)
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
    
def actualizar_stock(ideventos, donaciones, usuario_mod):
    try:
        conn =  get_connection()
        cursor = conn.cursor()
        now = datetime.now()

        for d in donaciones:
            
            cursor.execute(
                """
                INSERT INTO donaciones_has_eventos (donaciones_iddonaciones, eventos_ideventos, cantidad_donada)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE cantidad_donada = VALUES(cantidad_donada) 
                """, (d.iddonaciones, ideventos, d.cantidad))
            
            sql = "UPDATE donaciones SET cantidad = cantidad - %s, usuario_mod = %s, fecha_mod = %s WHERE iddonaciones = %s"
            values = (d.cantidad, usuario_mod, now, d.iddonaciones)

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

# Consulta Eventos
def get_evento(idevento):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT ideventos, nombre, descripcion, fechaHora FROM dist2025.eventos WHERE ideventos = %s"
    values = (idevento,)
    cursor.execute(sql, values)
    row = cursor.fetchone()
    conn.close()
    return row


def get_eventos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ideventos, nombre, descripcion, fechaHora FROM dist2025.eventos")
    rows = cursor.fetchall()

    eventosCompleto = []

    for e in rows:
        ideventos = e[0]
        sql = """
            SELECT u.idusuario, u.nombreUsuario, u.nombre, u.apellido, u.email, u.rol, u.clave, u.telefono, u.activo
            FROM dist2025.usuario u
            JOIN dist2025.participacion eu ON u.idusuario = eu.usuario_idusuario
            WHERE eu.eventos_ideventos = %s
            """
        values = (ideventos,)
        cursor.execute(sql, values)
        usuarios_bd = cursor.fetchall()

        eventosCompleto.append({
            "ideventos": ideventos,
            "nombre": e[1],
            "descripcion": e[2],
            "fechaHora": e[3],
            "usuarios": usuarios_bd
        })
    
    conn.close()
    return eventosCompleto

def alta_eventos(nombre, descripcion, fecha, usuarios):
    try:
        conn =  get_connection()
        cursor = conn.cursor()
        
        sql = "INSERT INTO eventos (nombre, descripcion, fechaHora) VALUES (%s, %s, %s)"
        values = (nombre, descripcion, fecha)
        cursor.execute(sql, values)
        idevento = cursor.lastrowid

        for u in usuarios:
            cursor.execute("INSERT INTO participacion (usuario_idusuario, eventos_ideventos) VALUES (%s, %s)", (u, idevento))

        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("Error al cargar:", e)
        return False
    
def mod_eventos(ideventos, nombre, usuarios):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        now = datetime.now()

        sql = "UPDATE eventos SET nombre = %s, fechaHora = %s WHERE ideventos = %s"
        values = (nombre, now, ideventos)
        cursor.execute(sql, values)

        cursor.execute("DELETE FROM dist2025.participacion WHERE eventos_ideventos = %s", (ideventos,))
        for u in usuarios:
            cursor.execute("INSERT INTO participacion (usuario_idusuario, eventos_ideventos) VALUES (%s, %s)", (u, ideventos))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print("Error al cargar:", e)
        return False

def baja_eventos(ideventos):
    try:
        conn =  get_connection()
        cursor = conn.cursor()
        now = datetime.now()

        sql = "SELECT fechaHora FROM dist2025.eventos WHERE ideventos = %s"
        values = (ideventos,)
        cursor.execute(sql, values)
        fechaHora = cursor.fetchone()

        fecha_evento = fechaHora[0]
        if fecha_evento <= now:
            print("Solo se pueden eliminar eventos a futuro")
            return False

        cursor.execute("DELETE FROM dist2025.participacion WHERE eventos_ideventos = %s", (ideventos,))
        cursor.execute("DELETE FROM dist2025.donaciones_has_eventos WHERE eventos_ideventos = %s", (ideventos,))
        cursor.execute("DELETE FROM dist2025.eventos WHERE ideventos = %s", (ideventos,))
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