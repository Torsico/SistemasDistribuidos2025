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

import logging

import grpc
from proto import usuarios_pb2
from proto import usuarios_pb2_grpc
from proto import rol_pb2
from proto import rol_pb2_grpc
from google.protobuf import empty_pb2


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to greet world ...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = usuarios_pb2_grpc.UsuarioServiceStub(channel)
        response = stub.GetUsuarios(empty_pb2.Empty())
        for u in response.usuarios:
            print(f"ID: {u.idusuario}, Usuario: {u.nombreUsuario}, Nombre: {u.nombre} {u.apellido}, Email: {u.email}, Rol: {u.rol}, Activo: {u.activo}")
        stub = rol_pb2_grpc.RolServiceStub(channel)
        response = stub.GetRoles(empty_pb2.Empty())
        for r in response.roles:
            print(f"ID Rol: {r.idrol}, Rol: {r.nombre}")


if __name__ == "__main__":
    logging.basicConfig()
    run()
