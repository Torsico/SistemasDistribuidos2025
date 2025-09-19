import sys
import os

# Agregar la carpeta 'proto' al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "proto"))

from concurrent import futures
import logging

import grpc

from bdConnect import get_usuarios
from bdConnect import get_roles
from proto import usuarios_pb2
from proto import usuarios_pb2_grpc
from proto import rol_pb2
from proto import rol_pb2_grpc


class UsuarioServiceImpl(usuarios_pb2_grpc.UsuarioServiceServicer):
    def GetUsuarios(self, request, context):
        usuariosBD = get_usuarios()
        lista = usuarios_pb2.UsuarioListResponse()
        for u in usuariosBD:
            lista.usuarios.append(
                usuarios_pb2.Usuario(
                    nombreUsuario=u[0],
                    nombre=u[1],
                    apellido=u[2],
                    email=u[3],
                )
            )
        return lista


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
