import grpc
import sys
import os

# Se agrega la carpeta 'proto' al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "proto"))

from proto import donaciones_pb2, donaciones_pb2_grpc

with grpc.insecure_channel(f"localhost:50051") as channel:
    stub = donaciones_pb2_grpc.DonacionesServiceStub(channel)

    request = donaciones_pb2.SolicitarDonacionRequest(
        idSolicitante=101,
        idOrganizacion=1,
        donacion=[
            donaciones_pb2.DonacionSolicitada(categoria="ALIMENTOS", descripcion="Puré de tomates"),
            donaciones_pb2.DonacionSolicitada(categoria="ROPA", descripcion="Camisas")
        ]
    )

    response = stub.SolicitarDonacion(request)
    print("Solicitud enviada, éxito:", response.suceso)