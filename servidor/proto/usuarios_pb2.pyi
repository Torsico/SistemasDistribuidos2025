from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Usuario(_message.Message):
    __slots__ = ("idusuario", "nombreUsuario", "nombre", "apellido", "email", "rol", "clave", "telefono", "activo")
    IDUSUARIO_FIELD_NUMBER: _ClassVar[int]
    NOMBREUSUARIO_FIELD_NUMBER: _ClassVar[int]
    NOMBRE_FIELD_NUMBER: _ClassVar[int]
    APELLIDO_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ROL_FIELD_NUMBER: _ClassVar[int]
    CLAVE_FIELD_NUMBER: _ClassVar[int]
    TELEFONO_FIELD_NUMBER: _ClassVar[int]
    ACTIVO_FIELD_NUMBER: _ClassVar[int]
    idusuario: int
    nombreUsuario: str
    nombre: str
    apellido: str
    email: str
    rol: int
    clave: str
    telefono: str
    activo: bool
    def __init__(self, idusuario: _Optional[int] = ..., nombreUsuario: _Optional[str] = ..., nombre: _Optional[str] = ..., apellido: _Optional[str] = ..., email: _Optional[str] = ..., rol: _Optional[int] = ..., clave: _Optional[str] = ..., telefono: _Optional[str] = ..., activo: bool = ...) -> None: ...

class AltaUsuarioRequest(_message.Message):
    __slots__ = ("usuario",)
    USUARIO_FIELD_NUMBER: _ClassVar[int]
    usuario: Usuario
    def __init__(self, usuario: _Optional[_Union[Usuario, _Mapping]] = ...) -> None: ...

class AltaUsuarioResponse(_message.Message):
    __slots__ = ("suceso",)
    SUCESO_FIELD_NUMBER: _ClassVar[int]
    suceso: bool
    def __init__(self, suceso: bool = ...) -> None: ...

class ModUsuarioRequest(_message.Message):
    __slots__ = ("usuario",)
    USUARIO_FIELD_NUMBER: _ClassVar[int]
    usuario: Usuario
    def __init__(self, usuario: _Optional[_Union[Usuario, _Mapping]] = ...) -> None: ...

class ModUsuarioResponse(_message.Message):
    __slots__ = ("suceso",)
    SUCESO_FIELD_NUMBER: _ClassVar[int]
    suceso: bool
    def __init__(self, suceso: bool = ...) -> None: ...

class BajaUsuarioRequest(_message.Message):
    __slots__ = ("idusuario",)
    IDUSUARIO_FIELD_NUMBER: _ClassVar[int]
    idusuario: int
    def __init__(self, idusuario: _Optional[int] = ...) -> None: ...

class BajaUsuarioResponse(_message.Message):
    __slots__ = ("suceso",)
    SUCESO_FIELD_NUMBER: _ClassVar[int]
    suceso: bool
    def __init__(self, suceso: bool = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UsuarioListResponse(_message.Message):
    __slots__ = ("usuarios",)
    USUARIOS_FIELD_NUMBER: _ClassVar[int]
    usuarios: _containers.RepeatedCompositeFieldContainer[Usuario]
    def __init__(self, usuarios: _Optional[_Iterable[_Union[Usuario, _Mapping]]] = ...) -> None: ...

class UsuarioRequest(_message.Message):
    __slots__ = ("idusuario",)
    IDUSUARIO_FIELD_NUMBER: _ClassVar[int]
    idusuario: int
    def __init__(self, idusuario: _Optional[int] = ...) -> None: ...

class UsuarioResponse(_message.Message):
    __slots__ = ("usuario",)
    USUARIO_FIELD_NUMBER: _ClassVar[int]
    usuario: Usuario
    def __init__(self, usuario: _Optional[_Union[Usuario, _Mapping]] = ...) -> None: ...
