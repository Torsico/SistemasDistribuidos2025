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

import sys
import os

# Se agrega la carpeta 'proto' al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "proto"))

from google.protobuf.timestamp_pb2 import Timestamp
import datetime

import logging
import jwt
import grpc
from proto import usuarios_pb2, usuarios_pb2_grpc
from proto import rol_pb2, rol_pb2_grpc
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
        response = stub.AltaUsuario(request)
        print("Respuesta del servidor:", response.suceso)
        
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
        response = stub.ModUsuario(request)
        print("Respuesta del servidor:", response.suceso)

        # Baja Usuario

        request = usuarios_pb2.BajaUsuarioRequest(idusuario=3)
        response = stub.BajaUsuario(request)
        print("Respuesta del servidor:", response.suceso)

        # Reimprimir la lista de usuarios
        
        response = stub.GetUsuarios(empty_pb2.Empty())
        for u in response.usuarios:
            print(f"ID: {u.idusuario}, Usuario: {u.nombreUsuario}, Nombre: {u.nombre} {u.apellido}, Email: {u.email}, Rol: {u.rol}, Activo: {u.activo}")

        ## Test Donaciones
        # Alta Donaciones

        ###Token Temporal
        SECRET_KEY = "secretosecretoso468"

        payload = {
            "idusuario": 1,
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
        response = stub.AltaDonaciones(request, metadata=metadata)
        print("Respuesta del Servidor: ", response.suceso)

        # Mod Donaciones

        donacionesMod = donaciones_pb2.Donaciones(
            iddonaciones=2,
            descripcion="Verde",
            cantidad=15
        )

        request = donaciones_pb2.ModDonacionesRequest(donaciones=donacionesMod)
        response = stub.ModDonaciones(request, metadata=metadata)
        print("Respuesta del Servidor: ", response.suceso)

        #Baja Donaciones

        request = donaciones_pb2.BajaDonacionesRequest(iddonaciones=2)
        response = stub.BajaDonaciones(request, metadata=metadata)
        print("Respuesta del Servidor ", response.suceso)

        # Reimprimir la lista de donaciones
        
        response = stub.GetDonaciones(empty_pb2.Empty())
        for d in response.donaciones:
            print(f"ID: {d.iddonaciones}, Categoria: {d.categoria}, Descripcion: {d.descripcion}, Cantidad: {d.cantidad}, Eliminado? {d.eliminado}, Fecha de Alta: {d.fecha_alta}, Fecha de Modificacion: {d.fecha_mod}, Usuario de Alta: {d.usuario_alta}, Usuario que Modifico: {d.usuario_mod}")

        ## Test Eventos

        stub = eventos_pb2_grpc.EventosServiceStub(channel)
        response = stub.GetEventos(empty_pb2.Empty())
        for e in response.evento:
            print(f"Evento: ID: {e.ideventos}, Nombre: {e.nombre}, Descripcion: {e.descripcion}, fecha evento: {e.fechaHora}")
            print("Usuarios: ")
            for u in e.usuario:
                print(f"ID: {u.idusuario}, Usuario: {u.nombreUsuario}, Nombre: {u.nombre} {u.apellido}, Email: {u.email}, Rol: {u.rol}, Activo: {u.activo}")


        # Fecha manualmente
        fecha_str = "2025-09-22 14:30:00"
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
        response = stub.AltaEvento(request)
        print("Respuesta del Servidor: ", response.suceso)

        

        ## Test Roles
        
        stub = rol_pb2_grpc.RolServiceStub(channel)
        response = stub.GetRoles(empty_pb2.Empty())
        for r in response.roles:
            print(f"ID Rol: {r.idrol}, Rol: {r.nombre}")


if __name__ == "__main__":
    logging.basicConfig()
    run()
