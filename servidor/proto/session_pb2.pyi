import usuarios_pb2 as _usuarios_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LoginRequest(_message.Message):
    __slots__ = ("usuario_email", "clave")
    USUARIO_EMAIL_FIELD_NUMBER: _ClassVar[int]
    CLAVE_FIELD_NUMBER: _ClassVar[int]
    usuario_email: str
    clave: str
    def __init__(self, usuario_email: _Optional[str] = ..., clave: _Optional[str] = ...) -> None: ...

class LoginResponse(_message.Message):
    __slots__ = ("suceso", "usuario", "token")
    SUCESO_FIELD_NUMBER: _ClassVar[int]
    USUARIO_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    suceso: bool
    usuario: _usuarios_pb2.Usuario
    token: str
    def __init__(self, suceso: bool = ..., usuario: _Optional[_Union[_usuarios_pb2.Usuario, _Mapping]] = ..., token: _Optional[str] = ...) -> None: ...

class InfoRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class InfoResponse(_message.Message):
    __slots__ = ("idusuario", "nombreUsuario", "rol")
    IDUSUARIO_FIELD_NUMBER: _ClassVar[int]
    NOMBREUSUARIO_FIELD_NUMBER: _ClassVar[int]
    ROL_FIELD_NUMBER: _ClassVar[int]
    idusuario: int
    nombreUsuario: str
    rol: int
    def __init__(self, idusuario: _Optional[int] = ..., nombreUsuario: _Optional[str] = ..., rol: _Optional[int] = ...) -> None: ...
