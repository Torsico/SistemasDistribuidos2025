import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
import usuarios_pb2 as _usuarios_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EventosDTO(_message.Message):
    __slots__ = ("nombre", "descripcion", "fecha")
    NOMBRE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPCION_FIELD_NUMBER: _ClassVar[int]
    FECHA_FIELD_NUMBER: _ClassVar[int]
    nombre: str
    descripcion: str
    fecha: _timestamp_pb2.Timestamp
    def __init__(self, nombre: _Optional[str] = ..., descripcion: _Optional[str] = ..., fecha: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Eventos(_message.Message):
    __slots__ = ("ideventos", "nombre", "descripcion", "fecha", "usuario")
    IDEVENTOS_FIELD_NUMBER: _ClassVar[int]
    NOMBRE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPCION_FIELD_NUMBER: _ClassVar[int]
    FECHA_FIELD_NUMBER: _ClassVar[int]
    USUARIO_FIELD_NUMBER: _ClassVar[int]
    ideventos: int
    nombre: str
    descripcion: str
    fecha: _timestamp_pb2.Timestamp
    usuario: _containers.RepeatedCompositeFieldContainer[_usuarios_pb2.Usuario]
    def __init__(self, ideventos: _Optional[int] = ..., nombre: _Optional[str] = ..., descripcion: _Optional[str] = ..., fecha: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., usuario: _Optional[_Iterable[_Union[_usuarios_pb2.Usuario, _Mapping]]] = ...) -> None: ...

class AltaEventoRequest(_message.Message):
    __slots__ = ("evento",)
    EVENTO_FIELD_NUMBER: _ClassVar[int]
    evento: EventosDTO
    def __init__(self, evento: _Optional[_Union[EventosDTO, _Mapping]] = ...) -> None: ...

class AltaEventoResponse(_message.Message):
    __slots__ = ("evento",)
    EVENTO_FIELD_NUMBER: _ClassVar[int]
    evento: Eventos
    def __init__(self, evento: _Optional[_Union[Eventos, _Mapping]] = ...) -> None: ...

class ModEventoRequest(_message.Message):
    __slots__ = ("evento",)
    EVENTO_FIELD_NUMBER: _ClassVar[int]
    evento: Eventos
    def __init__(self, evento: _Optional[_Union[Eventos, _Mapping]] = ...) -> None: ...

class ModEventoResponse(_message.Message):
    __slots__ = ("evento",)
    EVENTO_FIELD_NUMBER: _ClassVar[int]
    evento: Eventos
    def __init__(self, evento: _Optional[_Union[Eventos, _Mapping]] = ...) -> None: ...

class BajaEventoRequest(_message.Message):
    __slots__ = ("ideventos",)
    IDEVENTOS_FIELD_NUMBER: _ClassVar[int]
    ideventos: int
    def __init__(self, ideventos: _Optional[int] = ...) -> None: ...

class BajaEventoResponse(_message.Message):
    __slots__ = ("evento",)
    EVENTO_FIELD_NUMBER: _ClassVar[int]
    evento: Eventos
    def __init__(self, evento: _Optional[_Union[Eventos, _Mapping]] = ...) -> None: ...

class AsignarMiembroRequest(_message.Message):
    __slots__ = ("idusuario", "ideventos")
    IDUSUARIO_FIELD_NUMBER: _ClassVar[int]
    IDEVENTOS_FIELD_NUMBER: _ClassVar[int]
    idusuario: int
    ideventos: int
    def __init__(self, idusuario: _Optional[int] = ..., ideventos: _Optional[int] = ...) -> None: ...

class QuitarMiembroRequest(_message.Message):
    __slots__ = ("idusuario", "ideventos")
    IDUSUARIO_FIELD_NUMBER: _ClassVar[int]
    IDEVENTOS_FIELD_NUMBER: _ClassVar[int]
    idusuario: int
    ideventos: int
    def __init__(self, idusuario: _Optional[int] = ..., ideventos: _Optional[int] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListEventosResponse(_message.Message):
    __slots__ = ("evento",)
    EVENTO_FIELD_NUMBER: _ClassVar[int]
    evento: _containers.RepeatedCompositeFieldContainer[EventosDTO]
    def __init__(self, evento: _Optional[_Iterable[_Union[EventosDTO, _Mapping]]] = ...) -> None: ...
