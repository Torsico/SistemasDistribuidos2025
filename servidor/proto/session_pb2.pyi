from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LoginRequest(_message.Message):
    __slots__ = ("usuario_email", "clave")
    USUARIO_EMAIL_FIELD_NUMBER: _ClassVar[int]
    CLAVE_FIELD_NUMBER: _ClassVar[int]
    usuario_email: str
    clave: str
    def __init__(self, usuario_email: _Optional[str] = ..., clave: _Optional[str] = ...) -> None: ...

class LoginResponse(_message.Message):
    __slots__ = ("suceso", "token")
    SUCESO_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    suceso: bool
    token: str
    def __init__(self, suceso: bool = ..., token: _Optional[str] = ...) -> None: ...

class InfoRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class InfoResponse(_message.Message):
    __slots__ = ("nombreUsuario", "rol")
    NOMBREUSUARIO_FIELD_NUMBER: _ClassVar[int]
    ROL_FIELD_NUMBER: _ClassVar[int]
    nombreUsuario: str
    rol: int
    def __init__(self, nombreUsuario: _Optional[str] = ..., rol: _Optional[int] = ...) -> None: ...
