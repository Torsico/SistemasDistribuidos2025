from kafka import KafkaConsumer, errors

import json
import time


def Consumer(topic):
    while True:
        try: 
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers="localhost:9092",
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='latest'
            )
            print(f"Conectado a Kafka, escuchando topic '{topic}'...")
            return consumer
        except errors.NoBrokersAvailable:
            print("Kafka no disponible, reintentando en 2s...")
            time.sleep(2)
    
def ConsumirSolicitud():
    consumer = Consumer("solicitud-donaciones")
    for mensaje in consumer:
        solicitud = mensaje.value
        print("Mensaje completo recibido:", solicitud)
        print("Solicitud Recibida:")
        print(f'ID Solicitante: {solicitud["idSolicitante"]}')
        print(f'ID Organizacion: {solicitud["idOrganizacion"]}')
        print(f'Donaciones: {solicitud["donacion"]}')

def ConsumirTransferencia(transferencia, topic):
    print(f'Transferencia Recibida ({topic}):')
    print(f'ID Solicitante: {transferencia["idSolicitante"]}')
    print(f'ID Organizacion donante: {transferencia["idOrganizacion"]}')
    for t in transferencia["donacion"]:
        print(f'- {t["categoria"]}: {t["descripcion"]}')

if __name__ == "__main__":
    ConsumirSolicitud()
    