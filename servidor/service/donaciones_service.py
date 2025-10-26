import grpc

from security import verificar_token
from bdConnect import get_donaciones, alta_donaciones, mod_donaciones, baja_donaciones
from proto import donaciones_pb2, donaciones_pb2_grpc

class DonacionesServiceImpl(donaciones_pb2_grpc.DonacionesServiceServicer):
    def GetDonaciones(self, request, context):
        donacionesBD = get_donaciones()
        if not donacionesBD:
            context.abort(grpc.StatusCode.NOT_FOUND,f"No se encontraron donaciones")

        listaDonaciones = donaciones_pb2.ListDonacionesResponse()
        for d in donacionesBD:
            listaDonaciones.donaciones.append(
                donaciones_pb2.Donaciones(
                    iddonaciones=d[0],
                    categoria=d[1],
                    descripcion=d[2],
                    cantidad=d[3],
                    eliminado=d[4],
                    fecha_alta=d[5],
                    fecha_mod=d[6],
                    usuario_alta=d[7],
                    usuario_mod=d[8]
                )
            )
        return listaDonaciones
    
    def AltaDonaciones(self, request, context):
        metadata = dict(context.invocation_metadata())
        token = metadata.get("authorization")

        resultado = verificar_token(token)
        if not resultado["ok"]:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, resultado["error"])
        idusuario = resultado["idusuario"]

        donaciones = request.donaciones
        exito = alta_donaciones(
            donaciones.categoria,
            donaciones.descripcion,
            donaciones.cantidad,
            donaciones.eliminado,
            None,
            idusuario
        )
        if not exito:
            context.set_trailing_metadata((
                ("codigo-error", "Error alta"),
                ("mensaje-error", "No se pudo crear la donacion")
            ))
            context.abort(grpc.StatusCode.INTERNAL, f"No se pudo crear la donacion")
        return donaciones_pb2.AltaDonacionesResponse(suceso=exito)
    
    def ModDonaciones(self, request, context):
        metadata = dict(context.invocation_metadata())
        token = metadata.get("authorization")
        
        resultado = verificar_token(token)
        if not resultado["ok"]:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, resultado["error"])
        idusuario = resultado["idusuario"]
    
        donaciones = request.donaciones
        exito = mod_donaciones(
            donaciones.iddonaciones,
            donaciones.descripcion,
            donaciones.cantidad,
            idusuario
        )
        if not exito:
            context.set_trailing_metadata((
                ("codigo-error", "Error modificaciones"),
                ("mensaje-error", f"No se encontro la donacion con id: {donaciones.iddonaciones}")
            ))
            context.abort(grpc.StatusCode.NOT_FOUND, f"No se encontro la donacion")
        return donaciones_pb2.ModDonacionesResponse(suceso=exito)

    def BajaDonaciones(self, request, context):
        metadata = dict(context.invocation_metadata())
        token = metadata.get("authorization")
        
        resultado = verificar_token(token)
        if not resultado["ok"]:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, resultado["error"])
        idusuario = resultado["idusuario"]

        donaciones = request.iddonaciones
        exito = baja_donaciones(donaciones,idusuario)
        print("Estado de Baja de Donacion: ", exito)

        if not exito:
            context.set_trailing_metadata((
                ("codigo-error", "Error baja"),
                ("mensaje-error", f"No se encontro la donacion con id: {donaciones.iddonaciones}")
            ))
            context.abort(grpc.StatusCode.NOT_FOUND, f"No se encontro la donacion")
        return donaciones_pb2.BajaDonacionesResponse(suceso=exito)
    
    