from kafka import KafkaConsumer, errors
import json
import time

consumer = None

def InicializarConsumer():
    global consumer
    while consumer is None:
        try:
            consumer = KafkaConsumer(
                bootstrap_servers="localhost:9092",
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='earliest'
            )
            print("[KafkaCons] Conectado a Kafka, escuchando...")
        except errors.NoBrokersAvailable:
            print("[KafkaCons] Kafka no disponible, reintentando en 2s...")
            time.sleep(2)
    return consumer


def ConsumirSolicitud():
    if consumer is None:
        InicializarConsumer()
    consumer.subscribe(["solicitud-donaciones"])
    for mensaje in consumer:
        solicitud = mensaje.value
        print("Solicitud Recibida:")
        print(f'ID Solicitante: {solicitud["idSolicitante"]}')
        print(f'ID Organizacion: {solicitud["idOrganizacion"]}')
        print(f'Donaciones: {solicitud["donacion"]}')


def ConsumirTransferencia(transferencia, topic):
    print(f'Transferencia Recibida ({topic}):')
    print(f'ID Solicitud: {transferencia["idSolicitud"]}')
    print(f'ID Organizacion donante: {transferencia["idOrganizacionDonante"]}')
    for t in transferencia["donacion"]:
        print(f'- {t["categoria"]}: {t["descripcion"]}, cantidad:{t["cantidad"]}')

def ConsumirTransferencias():
    if consumer is None:
        InicializarConsumer()
    consumer.subscribe(pattern=r"^transferencia-donaciones_.*$")
    for mensaje in consumer:
        try:
            data = mensaje.value
            idOrgSol = data["idOrganizacionSolicitante"]
            topic = f"transferencia-donaciones_{idOrgSol}"
            ConsumirTransferencia(data, topic)
        except Exception as e:
            print(f"[KafkaCons] Error procesando mensaje: {e}")


if __name__ == "__main__":
    #ConsumirSolicitud()
    ConsumirTransferencias()