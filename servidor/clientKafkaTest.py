from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',   # puerto del broker
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Simular el contenido del request
mensaje = {
    "idSolicitante": 101,
    "idOrganizacion": 1,
    "donacion": [
        {"categoria": "ALIMENTOS", "descripcion": "Puré de tomates"},
        {"categoria": "ROPA", "descripcion": "Camisas"}
    ]
}

producer.send("solicitud-donaciones", mensaje)
producer.flush()
print("Mensaje enviado!")