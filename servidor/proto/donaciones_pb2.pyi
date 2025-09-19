import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DonacionesDTO(_message.Message):
    __slots__ = ("categoria", "descripcion", "cantidad")
    CATEGORIA_FIELD_NUMBER: _ClassVar[int]
    DESCRIPCION_FIELD_NUMBER: _ClassVar[int]
    CANTIDAD_FIELD_NUMBER: _ClassVar[int]
    categoria: str
    descripcion: str
    cantidad: int
    def __init__(self, categoria: _Optional[str] = ..., descripcion: _Optional[str] = ..., cantidad: _Optional[int] = ...) -> None: ...

class Donaciones(_message.Message):
    __slots__ = ("iddonaciones", "categoria", "descripcion", "cantidad", "eliminado", "hora_alta", "hora_mod", "usuario_alta", "usuario_mod")
    IDDONACIONES_FIELD_NUMBER: _ClassVar[int]
    CATEGORIA_FIELD_NUMBER: _ClassVar[int]
    DESCRIPCION_FIELD_NUMBER: _ClassVar[int]
    CANTIDAD_FIELD_NUMBER: _ClassVar[int]
    ELIMINADO_FIELD_NUMBER: _ClassVar[int]
    HORA_ALTA_FIELD_NUMBER: _ClassVar[int]
    HORA_MOD_FIELD_NUMBER: _ClassVar[int]
    USUARIO_ALTA_FIELD_NUMBER: _ClassVar[int]
    USUARIO_MOD_FIELD_NUMBER: _ClassVar[int]
    iddonaciones: int
    categoria: str
    descripcion: str
    cantidad: int
    eliminado: bool
    hora_alta: _timestamp_pb2.Timestamp
    hora_mod: _timestamp_pb2.Timestamp
    usuario_alta: int
    usuario_mod: int
    def __init__(self, iddonaciones: _Optional[int] = ..., categoria: _Optional[str] = ..., descripcion: _Optional[str] = ..., cantidad: _Optional[int] = ..., eliminado: bool = ..., hora_alta: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., hora_mod: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., usuario_alta: _Optional[int] = ..., usuario_mod: _Optional[int] = ...) -> None: ...

class AltaDonacionesRequest(_message.Message):
    __slots__ = ("donaciones",)
    DONACIONES_FIELD_NUMBER: _ClassVar[int]
    donaciones: DonacionesDTO
    def __init__(self, donaciones: _Optional[_Union[DonacionesDTO, _Mapping]] = ...) -> None: ...

class AltaDonacionesResponse(_message.Message):
    __slots__ = ("donaciones",)
    DONACIONES_FIELD_NUMBER: _ClassVar[int]
    donaciones: Donaciones
    def __init__(self, donaciones: _Optional[_Union[Donaciones, _Mapping]] = ...) -> None: ...

class ModDonacionesRequest(_message.Message):
    __slots__ = ("donaciones",)
    DONACIONES_FIELD_NUMBER: _ClassVar[int]
    donaciones: Donaciones
    def __init__(self, donaciones: _Optional[_Union[Donaciones, _Mapping]] = ...) -> None: ...

class ModDonacionesResponse(_message.Message):
    __slots__ = ("donaciones",)
    DONACIONES_FIELD_NUMBER: _ClassVar[int]
    donaciones: Donaciones
    def __init__(self, donaciones: _Optional[_Union[Donaciones, _Mapping]] = ...) -> None: ...

class BajaDonacionesRequest(_message.Message):
    __slots__ = ("iddonaciones",)
    IDDONACIONES_FIELD_NUMBER: _ClassVar[int]
    iddonaciones: int
    def __init__(self, iddonaciones: _Optional[int] = ...) -> None: ...

class BajaDonacionesResponse(_message.Message):
    __slots__ = ("donaciones",)
    DONACIONES_FIELD_NUMBER: _ClassVar[int]
    donaciones: Donaciones
    def __init__(self, donaciones: _Optional[_Union[Donaciones, _Mapping]] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListDonacionesResponse(_message.Message):
    __slots__ = ("donaciones",)
    DONACIONES_FIELD_NUMBER: _ClassVar[int]
    donaciones: _containers.RepeatedCompositeFieldContainer[DonacionesDTO]
    def __init__(self, donaciones: _Optional[_Iterable[_Union[DonacionesDTO, _Mapping]]] = ...) -> None: ...
