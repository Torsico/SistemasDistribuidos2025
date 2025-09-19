from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RolDTO(_message.Message):
    __slots__ = ("idrol", "nombre")
    IDROL_FIELD_NUMBER: _ClassVar[int]
    NOMBRE_FIELD_NUMBER: _ClassVar[int]
    idrol: int
    nombre: str
    def __init__(self, idrol: _Optional[int] = ..., nombre: _Optional[str] = ...) -> None: ...

class RolListResponse(_message.Message):
    __slots__ = ("roles",)
    ROLES_FIELD_NUMBER: _ClassVar[int]
    roles: _containers.RepeatedCompositeFieldContainer[RolDTO]
    def __init__(self, roles: _Optional[_Iterable[_Union[RolDTO, _Mapping]]] = ...) -> None: ...
