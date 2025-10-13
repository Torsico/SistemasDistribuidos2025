from kafka import KafkaProducer, errors
import json
import time

producer = None

def InicializarProducer():
    global producer
    while producer is None:
        try:
            producer = KafkaProducer(
                bootstrap_servers="localhost:9092",
                value_serializer=lambda m: json.dumps(m).encode('utf-8')
            )
            print("[KafkaProd] Producer conectado")
        except errors.NoBrokersAvailable:
            print("[KafkaProd] Kafka no disponible, reintentando en 2s...")
            time.sleep(2)
    return producer

def ProducirSolicitud(solicitud):
    global producer
    if producer is None:
        InicializarProducer()
    topic = "solicitud-donaciones"
    producer.send(topic, solicitud)
    producer.flush()
    print(f"[KafkaProd] Solicitud publicada en {topic}: {solicitud}")

def ProducirTransferencia(idSolicitud, idOrganizacionDonante, idOrganizacionSolicitante, donacion):
    global producer
    if producer is None:
        InicializarProducer()
    topic = f"transferencia-donaciones_{idOrganizacionSolicitante}"
    transferencia = {
        "idSolicitud": idSolicitud,
        "idOrganizacionDonante": idOrganizacionDonante,
        "idOrganizacionSolicitante": idOrganizacionSolicitante,
        "donacion": donacion
    }
    producer.send(topic, transferencia)
    producer.flush()
    print(f"[KafkaProd] Transferencia publicada en {topic}: {transferencia}")

def CerrarProducer():
    global producer
    if producer is not None:
        producer.flush()
        producer.close()
        print("[KafkaProd] Producer cerrado")
        producer = None

if __name__ == "__main__":
    InicializarProducer()
    while True:
        time.sleep(2)
