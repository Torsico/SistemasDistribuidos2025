import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
import usuarios_pb2 as _usuarios_pb2
import donaciones_pb2 as _donaciones_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Eventos(_message.Message):
    __slots__ = ("ideventos", "nombre", "descripcion", "fechaHora", "usuario", "donar")
    IDEVENTOS_FIELD_NUMBER: _ClassVar[int]
    NOMBRE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPCION_FIELD_NUMBER: _ClassVar[int]
    FECHAHORA_FIELD_NUMBER: _ClassVar[int]
    USUARIO_FIELD_NUMBER: _ClassVar[int]
    DONAR_FIELD_NUMBER: _ClassVar[int]
    ideventos: int
    nombre: str
    descripcion: str
    fechaHora: _timestamp_pb2.Timestamp
    usuario: _containers.RepeatedCompositeFieldContainer[_usuarios_pb2.Usuario]
    donar: _containers.RepeatedCompositeFieldContainer[DonarEvento]
    def __init__(self, ideventos: _Optional[int] = ..., nombre: _Optional[str] = ..., descripcion: _Optional[str] = ..., fechaHora: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., usuario: _Optional[_Iterable[_Union[_usuarios_pb2.Usuario, _Mapping]]] = ..., donar: _Optional[_Iterable[_Union[DonarEvento, _Mapping]]] = ...) -> None: ...

class AltaEventoRequest(_message.Message):
    __slots__ = ("evento",)
    EVENTO_FIELD_NUMBER: _ClassVar[int]
    evento: Eventos
    def __init__(self, evento: _Optional[_Union[Eventos, _Mapping]] = ...) -> None: ...

class AltaEventoResponse(_message.Message):
    __slots__ = ("suceso",)
    SUCESO_FIELD_NUMBER: _ClassVar[int]
    suceso: bool
    def __init__(self, suceso: bool = ...) -> None: ...

class ModEventoRequest(_message.Message):
    __slots__ = ("evento", "donaciones")
    EVENTO_FIELD_NUMBER: _ClassVar[int]
    DONACIONES_FIELD_NUMBER: _ClassVar[int]
    evento: Eventos
    donaciones: _containers.RepeatedCompositeFieldContainer[_donaciones_pb2.Donaciones]
    def __init__(self, evento: _Optional[_Union[Eventos, _Mapping]] = ..., donaciones: _Optional[_Iterable[_Union[_donaciones_pb2.Donaciones, _Mapping]]] = ...) -> None: ...

class ModEventoResponse(_message.Message):
    __slots__ = ("suceso",)
    SUCESO_FIELD_NUMBER: _ClassVar[int]
    suceso: bool
    def __init__(self, suceso: bool = ...) -> None: ...

class BajaEventoRequest(_message.Message):
    __slots__ = ("ideventos",)
    IDEVENTOS_FIELD_NUMBER: _ClassVar[int]
    ideventos: int
    def __init__(self, ideventos: _Optional[int] = ...) -> None: ...

class BajaEventoResponse(_message.Message):
    __slots__ = ("suceso",)
    SUCESO_FIELD_NUMBER: _ClassVar[int]
    suceso: bool
    def __init__(self, suceso: bool = ...) -> None: ...

class DonarEvento(_message.Message):
    __slots__ = ("iddonaciones", "ideventos", "cantidad_donada")
    IDDONACIONES_FIELD_NUMBER: _ClassVar[int]
    IDEVENTOS_FIELD_NUMBER: _ClassVar[int]
    CANTIDAD_DONADA_FIELD_NUMBER: _ClassVar[int]
    iddonaciones: int
    ideventos: int
    cantidad_donada: int
    def __init__(self, iddonaciones: _Optional[int] = ..., ideventos: _Optional[int] = ..., cantidad_donada: _Optional[int] = ...) -> None: ...

class DonarRequest(_message.Message):
    __slots__ = ("donar",)
    DONAR_FIELD_NUMBER: _ClassVar[int]
    donar: DonarEvento
    def __init__(self, donar: _Optional[_Union[DonarEvento, _Mapping]] = ...) -> None: ...

class DonarResponse(_message.Message):
    __slots__ = ("suceso",)
    SUCESO_FIELD_NUMBER: _ClassVar[int]
    suceso: bool
    def __init__(self, suceso: bool = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListEventosResponse(_message.Message):
    __slots__ = ("evento",)
    EVENTO_FIELD_NUMBER: _ClassVar[int]
    evento: _containers.RepeatedCompositeFieldContainer[Eventos]
    def __init__(self, evento: _Optional[_Iterable[_Union[Eventos, _Mapping]]] = ...) -> None: ...
