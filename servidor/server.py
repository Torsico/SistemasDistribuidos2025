
import sys
import os

# Se agrega la carpeta 'proto' al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "proto"))

from concurrent import futures
import logging
import grpc

from service.usuario_service import UsuarioServiceImpl
from service.donaciones_service import DonacionesServiceImpl
from service.eventos_service import EventosServiceImpl
from service.login_service import LoginServiceImpl

from proto import session_pb2_grpc
from proto import usuarios_pb2_grpc
from proto import donaciones_pb2_grpc
from proto import eventos_pb2_grpc

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    session_pb2_grpc.add_LoginServiceServicer_to_server(LoginServiceImpl(), server)
    usuarios_pb2_grpc.add_UsuarioServiceServicer_to_server(UsuarioServiceImpl(), server)
    donaciones_pb2_grpc.add_DonacionesServiceServicer_to_server(DonacionesServiceImpl(), server)
    eventos_pb2_grpc.add_EventosServiceServicer_to_server(EventosServiceImpl(), server)
    #rol_pb2_grpc.add_RolServiceServicer_to_server(RolServiceImpl(), server)
    
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
