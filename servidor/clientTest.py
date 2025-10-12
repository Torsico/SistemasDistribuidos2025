# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter client."""
from __future__ import print_function

from google.protobuf.timestamp_pb2 import Timestamp
import datetime

import logging
import jwt
import grpc
from proto import usuarios_pb2, usuarios_pb2_grpc
from proto import donaciones_pb2, donaciones_pb2_grpc
from proto import eventos_pb2, eventos_pb2_grpc
from google.protobuf import empty_pb2
import datetime

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to greet world ...")
    with grpc.insecure_channel("localhost:50051") as channel:
        
        stub = usuarios_pb2_grpc.UsuarioServiceStub(channel)

        
        ## Test Usuario
        # Obtener 1 usuario

        request = usuarios_pb2.UsuarioRequest(idusuario=1)
        response = stub.GetUsuario(request)

        usuarioPrueba = response.usuario
        print(f"ID: {usuarioPrueba.idusuario}, Usuario: {usuarioPrueba.nombreUsuario}, Nombre: {usuarioPrueba.nombre} {usuarioPrueba.apellido}, Email: {usuarioPrueba.email}, Rol: {usuarioPrueba.rol}, Activo: {usuarioPrueba.activo}")
        

        # Alta Usuario

        usuarioAlta = usuarios_pb2.Usuario(
            nombreUsuario="juli123",
            nombre="Julián",
            apellido="González",
            email="julian@example.com",
            rol=1,
            clave="1234",
            telefono="123456789",
            activo=True
        )

        request = usuarios_pb2.AltaUsuarioRequest(usuario=usuarioAlta)

        try:
            response = stub.AltaUsuario(request)
            print("Alta Usuario - Respuesta del servidor:", response.suceso)
        except grpc.RpcError as e:
            print("Error en Alta Usuario:", e.code(), e.details())
        
        # Modificacion Usuario

        usuarioMod = usuarios_pb2.Usuario(
            idusuario=3,
            nombreUsuario="juli321",
            nombre="Andres",
            apellido="Guille",
            rol=2,
            telefono="123456789",
            activo=True
        )

        request = usuarios_pb2.ModUsuarioRequest(usuario=usuarioMod)
        try:
            response = stub.ModUsuario(request)
            print("Mod Usuario - Respuesta del servidor:", response.suceso)
        except grpc.RpcError as e:
            print("Error en Mod Usuario:", e.code(), e.details())

        # Baja Usuario

        request = usuarios_pb2.BajaUsuarioRequest(idusuario=3)
        try:
            response = stub.BajaUsuario(request)
            print("Baja Usuario - Respuesta del servidor:", response.suceso)
        except grpc.RpcError as e:
            print("Error en Baja Usuario:", e.code(), e.details())

        # Reimprimir la lista de usuarios
        
        response = stub.GetUsuarios(empty_pb2.Empty())
        for u in response.usuarios:
            print(f"ID: {u.idusuario}, Usuario: {u.nombreUsuario}, Nombre: {u.nombre} {u.apellido}, Email: {u.email}, Rol: {u.rol}, Activo: {u.activo}")

        ## Test Donaciones
        # Alta Donaciones

        ###Token Temporal
        SECRET_KEY = "secretosecretoso468"

        payload = {
            "idusuario": 3,
            "nombreUsuario": "jdoe",
            "rol": "Presidente",
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        metadata = [("authorization", token)]
        ###

        stub = donaciones_pb2_grpc.DonacionesServiceStub(channel)
        
        donacionesAlta = donaciones_pb2.Donaciones(
            categoria="Ropa",
            descripcion="Azul",
            cantidad=10,
            eliminado=False,
        )

        request = donaciones_pb2.AltaDonacionesRequest(donaciones=donacionesAlta)

        try:
            response = stub.AltaDonaciones(request, metadata=metadata)
            print("Alta Donaciones - Respuesta del Servidor: ", response.suceso)
        except grpc.RpcError as e:
            print("Error en Alta Donaciones:", e.code(), e.details())

        # Mod Donaciones

        donacionesMod = donaciones_pb2.Donaciones(
            iddonaciones=2,
            descripcion="Verde",
            cantidad=15
        )

        request = donaciones_pb2.ModDonacionesRequest(donaciones=donacionesMod)
        try:
            response = stub.ModDonaciones(request, metadata=metadata)
            print("Mod Donaciones - Respuesta del Servidor: ", response.suceso)
        except grpc.RpcError as e:
            print("Error en Mod Donaciones:", e.code(), e.details())

        #Baja Donaciones

        request = donaciones_pb2.BajaDonacionesRequest(iddonaciones=2)
        try:
            response = stub.BajaDonaciones(request, metadata=metadata)
            print("Baja Donaciones - Respuesta del Servidor ", response.suceso)
        except grpc.RpcError as e:
            print("Error en Baja Donaciones:", e.code(), e.details())

        # Reimprimir la lista de donaciones
        
        response = stub.GetDonaciones(empty_pb2.Empty())
        for d in response.donaciones:
            print(f"ID: {d.iddonaciones}, Categoria: {d.categoria}, Descripcion: {d.descripcion}, Cantidad: {d.cantidad}, Eliminado? {d.eliminado}, Fecha de Alta: {d.fecha_alta}, Fecha de Modificacion: {d.fecha_mod}, Usuario de Alta: {d.usuario_alta}, Usuario que Modifico: {d.usuario_mod}")

        ## Test Eventos

        stub = eventos_pb2_grpc.EventosServiceStub(channel)

        # Alta Eventos

        # Fecha manualmente
        fecha_str = "2025-12-22 14:30:00"
        # Convertir al formato que timestamp acepte
        fecha_dt = datetime.datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
        # Se convierte y envia como Timestamp
        fecha_ts = Timestamp()
        fecha_ts.FromDatetime(fecha_dt)

        eventoAlta = eventos_pb2.Eventos(
            nombre="Barrio Nuevo",
            descripcion="Es un barrio nuevo",
            fechaHora=fecha_ts,
            usuario=[usuarioPrueba]
        )
        request = eventos_pb2.AltaEventoRequest(evento=eventoAlta)
        try:
            response = stub.AltaEvento(request, metadata=metadata)
            print("Alta Evento - Respuesta del Servidor: ", response.suceso)
        except grpc.RpcError as e:
            print("Error en Alta Evento:", e.code(), e.details())

        # Mod Evento

        eventoMod = eventos_pb2.Eventos(
            ideventos=1,
            nombre="Barrio Renovado"
        )
        
        donacionEvento = eventos_pb2.DonarEvento(
            iddonaciones=3,
            ideventos=2,
            cantidad_donada=3
        )

        usuarioEvento1 = eventos_pb2.UsuarioEvento(
            idusuario=2,
            idevento=2
        )

        usuarioEvento2 = eventos_pb2.UsuarioEvento(
            idusuario=1,
            idevento=1
        )

        request = eventos_pb2.ModEventoRequest(evento=eventoMod)

        try:
            response = stub.ModEvento(request, metadata=metadata)
            print("Mod Evento - Respuesta del Servidor: ", response.suceso)
        except grpc.RpcError as e:
            print("Error en Mod Evento:", e.code(), e.details())


        request = eventos_pb2.DonarRequest(donar=donacionEvento)
        try:
            response = stub.DonarEvento(request, metadata=metadata)
            print("Mod Donacion Evento - Respuesta del Servidor: ", response.suceso)
        except grpc.RpcError as e:
            print("Error en Mod Donacion Evento:", e.code(), e.details())

        
        request = eventos_pb2.ModificarMiembroRequest(miembro=usuarioEvento1)
        try:
            response = stub.AsignarMiembro(request)
            print("Asignar Miembro Evento - Respuesta del Servidor: ", response.suceso)
        except grpc.RpcError as e:
            print("Error en Asignar Miembro Evento:", e.code(), e.details())

        request = eventos_pb2.ModificarMiembroRequest(miembro=usuarioEvento2)
        try:
            response = stub.QuitarMiembro(request)
            print("Quitar Miembro Evento - Respuesta del Servidor: ", response.suceso)
        except grpc.RpcError as e:
            print("Error en Quitar Miembro Evento:", e.code(), e.details())

        # Baja Evento

        request = eventos_pb2.BajaEventoRequest(ideventos=4)
        try:
            response = stub.BajaEvento(request)
            print("Baja Evento - Respuesta del servidor:", response.suceso)
        except grpc.RpcError as e:
            print("Error en Baja Evento:", e.code(), e.details())

        # Reimprimir la lista de eventos
        response = stub.GetEventos(empty_pb2.Empty())
        for e in response.evento:
            print(f"Evento: ID: {e.ideventos}, Nombre: {e.nombre}, Descripcion: {e.descripcion}, fecha evento: {e.fechaHora}")
            print("Usuarios: ")
            for u in e.usuario:
                print(f"ID: {u.idusuario}, Usuario: {u.nombreUsuario}, Nombre: {u.nombre} {u.apellido}, Email: {u.email}, Rol: {u.rol}, Activo: {u.activo}")
            for d in e.donar:
                print("Donaciones Registradas: ")
                print(f"ID: {d.iddonaciones}, Cantidad: {d.cantidad_donada}")


if __name__ == "__main__":
    logging.basicConfig()
    run()
