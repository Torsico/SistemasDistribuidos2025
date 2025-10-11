import grpc

from security import generar_token, verificar_token
from bdConnect import verificar_usuario, obtener_usuario
from proto import session_pb2, session_pb2_grpc
from proto import usuarios_pb2

class LoginServiceImpl(session_pb2_grpc.LoginServiceServicer):
    def Login(self, request, context):
        usuario_email = request.usuario_email
        clave = request.clave

        exito, mensaje, idusuario, nombreUsuario, rol = verificar_usuario(usuario_email, clave)

        usuarioObtenido = obtener_usuario(nombreUsuario)

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

        return session_pb2.LoginResponse(suceso=True, usuario=usuario, token=token)
    
    def ObtenerInfo(self, request, context):
        metadata = dict(context.invocation_metadata())
        token = metadata.get("authorization")

        if not token:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Token no enviado")

        idusuario, nombreUsuario, rol = verificar_token(token)

        return session_pb2.InfoResponse(idusuario=idusuario, nombreUsuario=nombreUsuario, rol=rol)