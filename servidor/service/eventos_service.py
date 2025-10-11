import grpc
import datetime

from bdConnect import get_donacion, actualizar_stock, agregar_miembro_evento, quitar_miembro_evento
from bdConnect import get_evento, get_eventos, alta_eventos, mod_eventos, baja_eventos
from security import verificar_token
from proto import eventos_pb2, eventos_pb2_grpc
from proto import usuarios_pb2

class EventosServiceImpl(eventos_pb2_grpc.EventosServiceServicer):
    def GetEventos(self, request, context):
        EventosBD = get_eventos()
        if not EventosBD:
            context.abort(grpc.StatusCode.NOT_FOUND,f"No se encontraron el eventos")
        
        listaEventos = eventos_pb2.ListEventosResponse()
        for e in EventosBD:
            lista_usuarios = []
            for u in e["usuarios"]:
                lista_usuarios.append(
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
            
            lista_donaciones = []
            for d in e["donaciones"]:
                lista_donaciones.append(
                    eventos_pb2.DonarEvento(
                        iddonaciones=d[0],
                        cantidad_donada=d[1]
                    )
                )

            listaEventos.evento.append(
                eventos_pb2.Eventos(
                    ideventos=e["ideventos"],
                    nombre=e["nombre"],
                    descripcion=e["descripcion"],
                    fechaHora=e["fechaHora"],
                    usuario=lista_usuarios,
                    donar=lista_donaciones
                )
            )
        return listaEventos
    
    def AltaEvento(self, request, context):
        evento = request.evento
        fecha_dt = evento.fechaHora.ToDatetime()    #La base de datos no soporta Timestamp, entonces
                                                    #Se vuelve a convertir
        now = datetime.datetime.now()
        if fecha_dt <= now:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT,"La fecha del evento debe ser a futuro")

        exito = alta_eventos(
            evento.nombre,
            evento.descripcion,
            fecha_dt,
            [u.idusuario for u in evento.usuario]
        )
        if not exito:
            context.set_trailing_metadata((
                ("codigo-error", "Error alta"),
                ("mensaje-error", "No se pudo crear el evento")
            ))
            context.abort(grpc.StatusCode.INTERNAL, f"No se pudo crear el evento")
        return eventos_pb2.AltaEventoResponse(suceso=exito)

    def ModEvento(self, request, context):
        evento = request.evento
        if not evento:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT,"No existen evento disponibles")

        exito = mod_eventos(
            evento.ideventos,
            evento.nombre,
        )
        if not exito:
            context.set_trailing_metadata((
                ("codigo-error", "Error alta"),
                ("mensaje-error", "No se pudo crear el evento")
            ))
            context.abort(grpc.StatusCode.INTERNAL, f"No se pudo modificar el evento")

        return eventos_pb2.ModEventoResponse(suceso=exito)
    
    def DonarEvento(self, request, context):
        metadata = dict(context.invocation_metadata())
        token = metadata.get("authorization")

        resultado = verificar_token(token)
        if not resultado["ok"]:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, resultado["error"])
        idusuario = resultado["idusuario"]
    
        donacion = request.donar
        if not donacion:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT,"No existen eventos con donaciones registradas disponibles")

        DonacionBD = get_donacion(donacion.iddonaciones)
        if not DonacionBD:
            context.abort(grpc.StatusCode.NOT_FOUND,f"No se encontró la donación con id {donacion.iddonaciones}")
        evento_bd = get_evento(donacion.ideventos)
        if not evento_bd:
            context.abort(grpc.StatusCode.NOT_FOUND,f"No se encontró el evento con id {donacion.ideventos}")
        

        if donacion.cantidad_donada < 0:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT,"La cantidad de donación no puede ser negativa")
        if DonacionBD[3] < donacion.cantidad_donada:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT,"La cantidad de donacion no puede superar el existente")

        exito = actualizar_stock(donacion, idusuario)
        if not exito:
            context.abort(grpc.StatusCode.INTERNAL, "Error al actualizar el stock")
        
        return eventos_pb2.DonarResponse(suceso=exito)
    
    def AsignarMiembro(self, request, context):
        usuarioEvento = request.miembro
        
        exito = agregar_miembro_evento(usuarioEvento.idusuario, usuarioEvento.idevento)
        if not exito:
            context.abort(grpc.StatusCode.INTERNAL, "No se pudo agregar el usuario al evento")

        return eventos_pb2.ModificarMiembroResponse(suceso=exito)
    
    def QuitarMiembro(self, request, context):
        usuarioEvento = request.miembro

        exito = quitar_miembro_evento(usuarioEvento.idusuario, usuarioEvento.idevento)
        if not exito:
            context.abort(grpc.StatusCode.INTERNAL, "No se pudo quitar el usuario al evento")

        return eventos_pb2.ModificarMiembroResponse(suceso=exito)
    
    def BajaEvento(self, request, context):
        exito = baja_eventos(request.ideventos)
        print("Estado de Baja de Evento: ", exito)

        if not exito:
            context.set_trailing_metadata((
            ("codigo-error", "ID no encontrado"),
            ("mensaje-error", f"No se encontro el evento con id: {request.ideventos}")
        ))
            context.abort(grpc.StatusCode.NOT_FOUND, f"No se encontro el evento con id: {request.ideventos}")

        return eventos_pb2.BajaEventoResponse(suceso=exito)