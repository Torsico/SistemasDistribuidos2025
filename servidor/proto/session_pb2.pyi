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
    __slots__ = ("suceso", "mensaje", "idusuario")
    SUCESO_FIELD_NUMBER: _ClassVar[int]
    MENSAJE_FIELD_NUMBER: _ClassVar[int]
    IDUSUARIO_FIELD_NUMBER: _ClassVar[int]
    suceso: bool
    mensaje: str
    idusuario: int
    def __init__(self, suceso: bool = ..., mensaje: _Optional[str] = ..., idusuario: _Optional[int] = ...) -> None: ...

class logoutRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class logoutResponse(_message.Message):
    __slots__ = ("suceso",)
    SUCESO_FIELD_NUMBER: _ClassVar[int]
    suceso: bool
    def __init__(self, suceso: bool = ...) -> None: ...
