import sys
import os

# Se agrega la carpeta 'proto' al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "proto"))

from concurrent import futures
import logging
import grpc
from google.protobuf.timestamp_pb2 import Timestamp
import datetime

from security import generar_clave, encriptar_clave, generar_token, verificar_token
from bdConnect import verificar_usuario
from bdConnect import get_usuario, get_usuarios, alta_usuario, mod_usuario, baja_usuario
from bdConnect import get_donaciones, alta_donaciones, mod_donaciones, baja_donaciones
from bdConnect import get_eventos, alta_eventos
from bdConnect import get_roles, obtener_usuario
from proto import session_pb2, session_pb2_grpc
from proto import usuarios_pb2, usuarios_pb2_grpc
from proto import donaciones_pb2, donaciones_pb2_grpc
from proto import eventos_pb2, eventos_pb2_grpc
from proto import rol_pb2, rol_pb2_grpc


class LoginServiceImpl(session_pb2_grpc.LoginServiceServicer):
    def Login(self, request, context):
        usuario_email = request.usuario_email
        clave = request.clave

        usuarioObtenido = obtener_usuario(usuario_email)

        exito, mensaje, idusuario, nombreUsuario, rol = verificar_usuario(usuario_email, clave)

        if not exito:
            context.set_details(mensaje)
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            return session_pb2.LoginResponse(suceso=False)
        
        token = generar_token(idusuario, nombreUsuario, rol)

        usuario = usuarios_pb2.Usuario(
                    idusuario=usuarioObtenido[0],
                    nombreUsuario=usuarioObtenido[1],
                    nombre=usuarioObtenido[2],
                    apellido=usuarioObtenido[3],
                    email=usuarioObtenido[4],
                    rol=usuarioObtenido[5],
                    clave=usuarioObtenido[6],
                    telefono=usuarioObtenido[7],
                    activo=bool(usuarioObtenido[8])
                )

        return session_pb2.LoginResponse(suceso=True, usuario=usuario)
    
    def ObtenerInfo(self, request, context):
        metadata = dict(context.invocation_metadata())
        token = metadata.get("authorization")

        if not token:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Token no enviado")

        idusuario, nombreUsuario, rol = verificar_token(token)

        return session_pb2.InfoResponse(idusuario=idusuario, nombreUsuario=nombreUsuario, rol=rol)

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
        print("- Lista: ", lista)
        return lista
    
    def GetUsuario(self, request, context):
        u = get_usuario(request.idusuario)
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
        #context.abort(grpc.StatusCode.ALREADY_EXISTS, f"El email '{usuario.email}' ya esta registrado")
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
        #context.abort(grpc.StatusCode.NOT_FOUND, f"Usuario con id {usuario.idusuario} no encontrado")

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
        #context.abort(grpc.StatusCode.NOT_FOUND, f"Usuario con id {request.idusuario} no encontrado")

        return usuarios_pb2.BajaUsuarioResponse(suceso=exito)
    
class DonacionesServiceImpl(donaciones_pb2_grpc.DonacionesServiceServicer):
    def GetDonaciones(self, request, context):
        donacionesBD = get_donaciones()
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
        #context.abort(grpc.StatusCode.INTERNAL, f"No se pudo crear la donacion")
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
        #context.abort(grpc.StatusCode.NOT_FOUND, f"No se encontro la donacion")
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

        if not exito:
            context.set_trailing_metadata((
                ("codigo-error", "Error baja"),
                ("mensaje-error", f"No se encontro la donacion con id: {donaciones.iddonaciones}")
            ))
        #context.abort(grpc.StatusCode.NOT_FOUND, f"No se encontro la donacion")
        return donaciones_pb2.BajaDonacionesResponse(suceso=exito)
    
class EventoServiceImpl(eventos_pb2_grpc.EventosServiceServicer):
    def GetEventos(self, request, context):
        EventosBD = get_eventos()
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
            fecha_ts = Timestamp()
            if isinstance(e["fechaHora"], datetime.datetime):
                fecha_ts.FromDatetime(e["fechaHora"])
            else:
                fecha_dt = datetime.datetime.strptime(e["fechaHora"], "%Y-%m-%d %H:%M:%S")
                fecha_ts.FromDatetime(fecha_dt)
            listaEventos.evento.append(
                eventos_pb2.Eventos(
                    ideventos=e["ideventos"],
                    nombre=e["nombre"],
                    descripcion=e["descripcion"],
                    fechaHora=fecha_ts,
                    usuario=lista_usuarios
                )
            )
        return listaEventos
    



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
    session_pb2_grpc.add_LoginServiceServicer_to_server(LoginServiceImpl(), server)
    usuarios_pb2_grpc.add_UsuarioServiceServicer_to_server(UsuarioServiceImpl(), server)
    donaciones_pb2_grpc.add_DonacionesServiceServicer_to_server(DonacionesServiceImpl(), server)
    eventos_pb2_grpc.add_EventosServiceServicer_to_server(EventoServiceImpl(), server)
    rol_pb2_grpc.add_RolServiceServicer_to_server(RolServiceImpl(), server)
    
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
