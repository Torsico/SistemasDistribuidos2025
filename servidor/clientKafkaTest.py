from kafkaService.producer import ProducirSolicitud, ProducirTransferencia, CerrarProducer

# Producir Solicitud
mensaje_solicitud = {
    "idSolicitante": 101,
    "idOrganizacion": 1,
    "donacion": [
        {"categoria": "ALIMENTOS", "descripcion": "Puré de tomates"},
        {"categoria": "ROPA", "descripcion": "Camisas"}
    ]
}
#ProducirSolicitud(mensaje_solicitud)


# Producir Transferencia
mensaje_transferencia = [{"categoria": "ALIMENTOS", "descripcion": "Puré de tomates", "cantidad":2000},]

ProducirTransferencia(
    idSolicitud= 102,
    idOrganizacionDonante= 2,
    idOrganizacionSolicitante= 4,
    donacion= mensaje_transferencia
)

CerrarProducer()