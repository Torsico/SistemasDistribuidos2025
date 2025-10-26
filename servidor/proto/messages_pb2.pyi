from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Donacion(_message.Message):
    __slots__ = ("categoria", "descripcion", "cantidad")
    CATEGORIA_FIELD_NUMBER: _ClassVar[int]
    DESCRIPCION_FIELD_NUMBER: _ClassVar[int]
    CANTIDAD_FIELD_NUMBER: _ClassVar[int]
    categoria: str
    descripcion: str
    cantidad: int
    def __init__(self, categoria: _Optional[str] = ..., descripcion: _Optional[str] = ..., cantidad: _Optional[int] = ...) -> None: ...

class SolicitudDonacion(_message.Message):
    __slots__ = ("idOrganizacionSolicitante", "idSolicitud", "donacion")
    IDORGANIZACIONSOLICITANTE_FIELD_NUMBER: _ClassVar[int]
    IDSOLICITUD_FIELD_NUMBER: _ClassVar[int]
    DONACION_FIELD_NUMBER: _ClassVar[int]
    idOrganizacionSolicitante: int
    idSolicitud: int
    donacion: _containers.RepeatedCompositeFieldContainer[Donacion]
    def __init__(self, idOrganizacionSolicitante: _Optional[int] = ..., idSolicitud: _Optional[int] = ..., donacion: _Optional[_Iterable[_Union[Donacion, _Mapping]]] = ...) -> None: ...

class TransferenciaDonacion(_message.Message):
    __slots__ = ("idSolicitud", "idOrganizacionDonante", "idOrganizacionSolicitante", "donacion")
    IDSOLICITUD_FIELD_NUMBER: _ClassVar[int]
    IDORGANIZACIONDONANTE_FIELD_NUMBER: _ClassVar[int]
    IDORGANIZACIONSOLICITANTE_FIELD_NUMBER: _ClassVar[int]
    DONACION_FIELD_NUMBER: _ClassVar[int]
    idSolicitud: int
    idOrganizacionDonante: int
    idOrganizacionSolicitante: int
    donacion: _containers.RepeatedCompositeFieldContainer[Donacion]
    def __init__(self, idSolicitud: _Optional[int] = ..., idOrganizacionDonante: _Optional[int] = ..., idOrganizacionSolicitante: _Optional[int] = ..., donacion: _Optional[_Iterable[_Union[Donacion, _Mapping]]] = ...) -> None: ...

class OfertaDonacion(_message.Message):
    __slots__ = ("idOferta", "idOrganizacionDonante", "donacion")
    IDOFERTA_FIELD_NUMBER: _ClassVar[int]
    IDORGANIZACIONDONANTE_FIELD_NUMBER: _ClassVar[int]
    DONACION_FIELD_NUMBER: _ClassVar[int]
    idOferta: int
    idOrganizacionDonante: int
    donacion: _containers.RepeatedCompositeFieldContainer[Donacion]
    def __init__(self, idOferta: _Optional[int] = ..., idOrganizacionDonante: _Optional[int] = ..., donacion: _Optional[_Iterable[_Union[Donacion, _Mapping]]] = ...) -> None: ...

class BajaSolicitud(_message.Message):
    __slots__ = ("idOrganizacionSolicitante", "idSolicitud")
    IDORGANIZACIONSOLICITANTE_FIELD_NUMBER: _ClassVar[int]
    IDSOLICITUD_FIELD_NUMBER: _ClassVar[int]
    idOrganizacionSolicitante: int
    idSolicitud: int
    def __init__(self, idOrganizacionSolicitante: _Optional[int] = ..., idSolicitud: _Optional[int] = ...) -> None: ...

class RespuestaDonacion(_message.Message):
    __slots__ = ("mensaje", "exito")
    MENSAJE_FIELD_NUMBER: _ClassVar[int]
    EXITO_FIELD_NUMBER: _ClassVar[int]
    mensaje: str
    exito: bool
    def __init__(self, mensaje: _Optional[str] = ..., exito: bool = ...) -> None: ...

class EventoExterno(_message.Message):
    __slots__ = ("idOrganizacion", "idEvento", "nombreEvento", "descripcion", "fechaHora")
    IDORGANIZACION_FIELD_NUMBER: _ClassVar[int]
    IDEVENTO_FIELD_NUMBER: _ClassVar[int]
    NOMBREEVENTO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPCION_FIELD_NUMBER: _ClassVar[int]
    FECHAHORA_FIELD_NUMBER: _ClassVar[int]
    idOrganizacion: int
    idEvento: int
    nombreEvento: str
    descripcion: str
    fechaHora: str
    def __init__(self, idOrganizacion: _Optional[int] = ..., idEvento: _Optional[int] = ..., nombreEvento: _Optional[str] = ..., descripcion: _Optional[str] = ..., fechaHora: _Optional[str] = ...) -> None: ...

class BajaEvento(_message.Message):
    __slots__ = ("idOrganizacion", "idEvento")
    IDORGANIZACION_FIELD_NUMBER: _ClassVar[int]
    IDEVENTO_FIELD_NUMBER: _ClassVar[int]
    idOrganizacion: int
    idEvento: int
    def __init__(self, idOrganizacion: _Optional[int] = ..., idEvento: _Optional[int] = ...) -> None: ...

class Voluntario(_message.Message):
    __slots__ = ("idOrganizacion", "idVoluntario", "nombre", "apellido", "telefono", "email")
    IDORGANIZACION_FIELD_NUMBER: _ClassVar[int]
    IDVOLUNTARIO_FIELD_NUMBER: _ClassVar[int]
    NOMBRE_FIELD_NUMBER: _ClassVar[int]
    APELLIDO_FIELD_NUMBER: _ClassVar[int]
    TELEFONO_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    idOrganizacion: int
    idVoluntario: int
    nombre: str
    apellido: str
    telefono: str
    email: str
    def __init__(self, idOrganizacion: _Optional[int] = ..., idVoluntario: _Optional[int] = ..., nombre: _Optional[str] = ..., apellido: _Optional[str] = ..., telefono: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...

class AdhesionEvento(_message.Message):
    __slots__ = ("idEvento", "voluntario")
    IDEVENTO_FIELD_NUMBER: _ClassVar[int]
    VOLUNTARIO_FIELD_NUMBER: _ClassVar[int]
    idEvento: int
    voluntario: Voluntario
    def __init__(self, idEvento: _Optional[int] = ..., voluntario: _Optional[_Union[Voluntario, _Mapping]] = ...) -> None: ...

class RespuestaEvento(_message.Message):
    __slots__ = ("mensaje", "exito")
    MENSAJE_FIELD_NUMBER: _ClassVar[int]
    EXITO_FIELD_NUMBER: _ClassVar[int]
    mensaje: str
    exito: bool
    def __init__(self, mensaje: _Optional[str] = ..., exito: bool = ...) -> None: ...
