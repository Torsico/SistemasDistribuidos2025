import sys
import os

# Se agrega la carpeta 'proto' al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "proto"))

from concurrent import futures
import logging
import grpc

from security import generar_clave, encriptar_clave, verificar_clave
from bdConnect import get_usuarios, alta_usuario, mod_usuario, baja_usuario
from bdConnect import get_roles
from proto import usuarios_pb2, usuarios_pb2_grpc
from proto import rol_pb2, rol_pb2_grpc


class UsuarioServiceImpl(usuarios_pb2_grpc.UsuarioServiceServicer):
    def GetUsuarios(self, request, context):
        usuariosBD = get_usuarios()
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
        return lista
    
    def AltaUsuario(self, request, context):
        usuario = request.usuario
        clave = generar_clave()
        claveEncriptada = encriptar_clave(clave)

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

        if not exito:
            context.set_trailing_metadata((
            ("codigo-error", "EMAIL_DUPLICADO"),
            ("mensaje-error", f"El email '{usuario.email}' ya existe")
        ))
        context.abort(grpc.StatusCode.ALREADY_EXISTS, f"El email '{usuario.email}' ya esta registrado")
        return usuarios_pb2.AltaUsuarioResponse(suceso=exito)
    
    def ModUsuario(self, request, context):
        usuario = request.usuario

        exito = mod_usuario(
            usuario.idusuario,
            usuario.nombreUsuario,
            usuario.nombre,
            usuario.apellido,
            usuario.rol,
            usuario.telefono,
            usuario.activo
        )

        if not exito:
            context.set_trailing_metadata((
            ("codigo-error", "ID no encontrado"),
            ("mensaje-error", f"No se encontro el usuario con id: {usuario.idusuario}")
        ))
        context.abort(grpc.StatusCode.NOT_FOUND, f"Usuario con id {usuario.idusuario} no encontrado")

        return usuarios_pb2.ModUsuarioResponse(suceso=exito)
    
    def BajaUsuario(self, request, context):
        exito = baja_usuario(request.idusuario)

        if not exito:
            context.set_trailing_metadata((
            ("codigo-error", "ID no encontrado"),
            ("mensaje-error", f"No se encontro el usuario con id: {request.idusuario}")
        ))
        context.abort(grpc.StatusCode.NOT_FOUND, f"Usuario con id {request.idusuario} no encontrado")

        return usuarios_pb2.BajaUsuarioResponse(suceso=exito)


class RolServiceImpl(rol_pb2_grpc.RolServiceServicer):
    def GetRoles(self, request, context):
        rolesBD = get_roles()
        listaRol = rol_pb2.RolListResponse()
        for r in rolesBD:
            listaRol.roles.append(
                rol_pb2.RolDTO(
                    idrol=r[0],
                    nombre=r[1]
                )
            )
        return listaRol
    


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    usuarios_pb2_grpc.add_UsuarioServiceServicer_to_server(UsuarioServiceImpl(), server)
    rol_pb2_grpc.add_RolServiceServicer_to_server(RolServiceImpl(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
