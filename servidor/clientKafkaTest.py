from kafkaService.producer import ProducirSolicitud, ProducirTransferencia, CerrarProducer
import requests

# Solicitud Donaciones
solicitud = {
    "idOrganizacionSolicitante": 4,
    "idSolicitud": 102,
    "donacion": [
        {"categoria": "ALIMENTOS", "descripcion": "Leche en polvo"}
    ]
}

response = requests.post("http://localhost:5000/solicitud-donaciones", json=solicitud)
######################################################################################################


# Transferencia Donaciones
mensaje_transferencia = [{"categoria": "ALIMENTOS", "descripcion": "Puré de tomates", "cantidad":2000},]

transferencia = {
    "idSolicitud": 102,
    "idOrganizacionDonante": 2,
    "idOrganizacionSolicitante": 4,
    "donacion": mensaje_transferencia
}

#response = requests.post("http://localhost:5000/transferencia-donaciones", json=transferencia)
######################################################################################################


# Oferta Donaciones
oferta = {
    "idOferta": 301,
    "idOrganizacionDonante": 2,
    "donacion": [
        {"categoria": "ROPA", "descripcion": "Camisas", "cantidad": 50}
    ]
}

#response = requests.post("http://localhost:5000/oferta-donaciones", json=oferta)
######################################################################################################


# Baja Solicitud
baja_solicitud = {
    "idOrganizacionSolicitante": 4,
    "idSolicitud": 102
}

#response = requests.post("http://localhost:5000/baja-solicitud-donaciones", json=baja_solicitud)
######################################################################################################


# Publicar Evento
evento = {
    "idOrganizacion": 1,
    "idEvento": 501,
    "nombreEvento": "Campaña Solidaria",
    "descripcion": "Recolección de alimentos",
    "fechaHora": "2025-11-01T10:00:00"
}

#response = requests.post("http://localhost:5000/publicar-evento", json=evento)
######################################################################################################


# Baja Evento
baja_evento = {
    "idOrganizacion": 1,
    "idEvento": 501
}

#response = requests.post("http://localhost:5000/baja-evento-solidario", json=baja_evento)
######################################################################################################


# Adhesion Evento
adhesion = {
    "idEvento": 501,
    "idOrganizador": 1,
    "voluntario": {
        "idOrganizacion": 4,
        "idVoluntario": 901,
        "nombre": "Juan",
        "apellido": "Pérez",
        "telefono": "123456789",
        "email": "juan@example.com"
    }
}

#response = requests.post("http://localhost:5000/adhesion-evento", json=adhesion)
######################################################################################################


print(response.json())