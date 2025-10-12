from kafka import KafkaConsumer, errors

import json
import time

def Consumer(topic):
    consumer = None
    while consumer is None:
        try: 
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers="localhost:9092",
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='earliest',
                group_id='test-group'
            )
            print(f"Conectado a Kafka, escuchando topic '{topic}'...")
            
        except errors.NoBrokersAvailable:
            print("Kafka no disponible, reintentando en 2s...")
            time.sleep(2)
    return consumer
    
def ConsumirSolicitud():
    consumidor = Consumer("solicitud-donaciones")
    for mensaje in consumidor:
        solicitud = mensaje.value
        print("Mensaje completo recibido:", solicitud)
        print("Solicitud Recibida:")
        print(f'ID Solicitante: {solicitud["idSolicitante"]}')
        print(f'ID Organizacion: {solicitud["idOrganizacion"]}')
        print(f'Donaciones: {solicitud["donacion"]}')

def ConsumirTransferencia(transferencia, topic):
    print(f'Transferencia Recibida ({topic}):')
    print(f'ID Solicitud: {transferencia["idSolicitud"]}')
    print(f'ID Organizacion donante: {transferencia["idOrganizacion"]}')
    for t in transferencia["donacion"]:
        print(f'- {t["categoria"]}: {t["descripcion"]}, cantidad:{t["cantidad"]}')

for mensaje in Consumer("solicitud-donaciones"):
    print(mensaje.value)


if __name__ == "__main__":
    ConsumirSolicitud()
    