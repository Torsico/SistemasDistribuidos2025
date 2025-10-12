from kafka import KafkaProducer, errors
from google.protobuf.json_format import MessageToDict

import json
import time


def ProducirSolicitud(solicitud):
    topic = "solicitud-donaciones"

    solicitud_dict = MessageToDict(solicitud, preserving_proto_field_name=True)

    producer.send(topic, solicitud_dict)
    print(f"[KafkaProd] Solicitud publicada en {topic}: {solicitud}")
    producer.flush()
    producer.close()

def ProducirTransferencia(idSolicitud, idOrganizacion, donacion):
    transferencia = {
        "idSolicitud": idSolicitud,
        "idOrganizacion": idOrganizacion,
        "donacion": donacion        
    }
    topic = f"/transferencia-donaciones/{idOrganizacion}"
    producer.send(topic, transferencia)
    print(f"[KafkaProd] Transferencia publicada en {topic}: {transferencia}")
    producer.flush()
    producer.close()



while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers="kafka:9092",
            value_serializer=lambda m: json.dumps(m).encode('utf-8')
        )
    except errors.NoBrokersAvailable:
        print("Kafka no disponible, reintentando en 2s...")
        time.sleep(2)