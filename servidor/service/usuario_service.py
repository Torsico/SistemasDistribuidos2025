import grpc

from bdConnect import get_usuario, get_usuarios, alta_usuario, mod_usuario, baja_usuario
from security import generar_clave, encriptar_clave
from proto import usuarios_pb2, usuarios_pb2_grpc

class UsuarioServiceImpl(usuarios_pb2_grpc.UsuarioServiceServicer):
    def GetUsuarios(self, request, context):
        usuariosBD = get_usuarios()
        if not usuariosBD:
            context.abort(grpc.StatusCode.NOT_FOUND,f"No se encontraron usuarios.")
        
        lista = usuarios_pb2.UsuarioListResponse()
        for u in usuariosBD:
            lista.usuarios.append(
                usuarios_pb2.Usuario(
                    idusuario=u[0],
                    nombreUsuario=u[1],
                    nombre=u[2],
                    apellido=u[3],
                    email=u[4],
                    rol=u[5],
                    clave=u[6],
                    telefono=u[7],
                    activo=bool(u[8])
                )
            )
        print("- Lista: ", lista)
        return lista
    
    def GetUsuario(self, request, context):
        u = get_usuario(request.idusuario)
        if not u:
            context.abort(grpc.StatusCode.NOT_FOUND,f"No se encontro el usuario con id {u.idusuario}")

        usuario = usuarios_pb2.Usuario(
                    idusuario=u[0],
                    nombreUsuario=u[1],
                    nombre=u[2],
                    apellido=u[3],
                    email=u[4],
                    rol=u[5],
                    clave=u[6],
                    telefono=u[7],
                    activo=bool(u[8])
                )
        print("- Usuario: ", usuario)
        return usuarios_pb2.UsuarioResponse(usuario=usuario)

    
    def AltaUsuario(self, request, context):
        usuario = request.usuario
        clave = generar_clave()
        claveEncriptada = encriptar_clave(clave)

        print("---------------------------")
        print(f"Clave del usuario: {clave}")
        print("---------------------------")

        print("- Alta Usuario: ", usuario)
        exito = alta_usuario(
            usuario.nombreUsuario,
            usuario.nombre,
            usuario.apellido,
            usuario.email,
            usuario.rol,
            claveEncriptada,
            usuario.telefono,
            usuario.activo
        )

        print("- Estado de alta: ", exito)

        if not exito:
            context.set_trailing_metadata((
            ("codigo-error", "EMAIL_DUPLICADO"),
            ("mensaje-error", f"El email '{usuario.email}' ya existe")
        ))
            context.abort(grpc.StatusCode.ALREADY_EXISTS, f"El email '{usuario.email}' ya esta registrado")
        return usuarios_pb2.AltaUsuarioResponse(suceso=exito, clave=clave)
    
    def ModUsuario(self, request, context):
        usuario = request.usuario
        print("- Usuario a Modificar: ", usuario)
        exito = mod_usuario(
            usuario.idusuario,
            usuario.nombreUsuario,
            usuario.nombre,
            usuario.apellido,
            usuario.rol,
            usuario.telefono,
            usuario.activo
        )
        print("- Estado de modificacion: ", exito)

        if not exito:
            context.set_trailing_metadata((
            ("codigo-error", "ID no encontrado"),
            ("mensaje-error", f"No se encontro el usuario con id: {usuario.idusuario}")
        ))
            context.abort(grpc.StatusCode.NOT_FOUND, f"Usuario con id {usuario.idusuario} no encontrado")

        return usuarios_pb2.ModUsuarioResponse(suceso=exito)
    
    def BajaUsuario(self, request, context):
        exito = baja_usuario(request.idusuario)
        print(f"- Usuario con id: {request.idusuario}")
        print("- Estado de Baja: ", exito)

        if not exito:
            context.set_trailing_metadata((
            ("codigo-error", "ID no encontrado"),
            ("mensaje-error", f"No se encontro el usuario con id: {request.idusuario}")
        ))
            context.abort(grpc.StatusCode.NOT_FOUND, f"Usuario con id {request.idusuario} no encontrado")

        return usuarios_pb2.BajaUsuarioResponse(suceso=exito)