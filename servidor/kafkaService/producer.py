from flask import Flask, request, jsonify
from kafka import KafkaProducer, errors
import os
import json
import time


app = Flask(__name__)
producer = None

def InicializarProducer():
    global producer
    while producer is None:
        try:
            producer = KafkaProducer(
                bootstrap_servers=os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
                value_serializer=lambda m: json.dumps(m).encode('utf-8')
            )
            print("[KafkaProd] Producer conectado")
        except errors.NoBrokersAvailable:
            print("[KafkaProd] Kafka no disponible, reintentando en 2s...")
            time.sleep(2)
    return producer

producer = InicializarProducer()

## Solicitud Donaciones

@app.route('/solicitud-donaciones', methods=['POST'])
def ProducirSolicitud():
    global producer
    data = request.json

    idOrganizacionSolicitante = data.get("idOrganizacionSolicitante")
    idSolicitud = data.get("idSolicitud")
    donacion = data.get("donacion", [])

    lista_donacion = []
    for d in donacion:
        donacion_recibida = {
            "categoria": d.get("categoria"),
            "descripcion": d.get("descripcion"),
        }
        lista_donacion.append(donacion_recibida)

    solicitud = {
        "idOrganizacionSolicitante": idOrganizacionSolicitante,
        "idSolicitud": idSolicitud,
        "donacion": lista_donacion
    }

    topic = "solicitud-donaciones"
    
    producer.send(topic, solicitud)
    producer.flush()

    print(f"[KafkaProd] Solicitud publicada en {topic}: {solicitud}")
    return jsonify({"status": "Mensaje enviado a Kafka"}), 200


## Transferir Donaciones

@app.route('/transferencia-donaciones', methods=['POST'])
def ProducirTransferencia():
    global producer
    data = request.json

    idSolicitud = data.get("idSolicitud")
    idOrganizacionDonante = data.get("idOrganizacionDonante")
    idOrganizacionSolicitante = data.get("idOrganizacionSolicitante")
    donacion = data.get("donacion", [])

    lista_donacion = []
    for d in donacion:
        donacion_recibida = {
            "categoria": d.get("categoria"),
            "descripcion": d.get("descripcion"),
            "cantidad": d.get("cantidad")
        }
        lista_donacion.append(donacion_recibida)

    transferencia = {
        "idSolicitud": idSolicitud,
        "idOrganizacionDonante": idOrganizacionDonante,
        "idOrganizacionSolicitante": idOrganizacionSolicitante,
        "donacion": lista_donacion
    }

    topic = f"transferencia-donaciones_{idOrganizacionSolicitante}"

    producer.send(topic, transferencia)
    producer.flush()

    print(f"[KafkaProd] Transferencia publicada en {topic}: {transferencia}")
    return jsonify({"status": "Transferencia enviada a Kafka"}), 200


## Ofrecer Donaciones

@app.route('/oferta-donaciones', methods=['POST'])
def ProducirOferta(idOferta, idOrganizacionDonante, donacion):
    global producer
    data = request.json

    idOferta = data.get("idOferta")
    idOrganizacionDonante = data.get("idOrganizacionDonante")
    donacion = data.get("donacion", [])

    lista_donacion = []
    for d in donacion:
        donacion_recibida = {
            "categoria": d.get("categoria"),
            "descripcion": d.get("descripcion"),
            "cantidad": d.get("cantidad")
        }
        lista_donacion.append(donacion_recibida)

    oferta = {
        "idOferta": idOferta,
        "idOrganizacionDonante": idOrganizacionDonante,
        "donacion": lista_donacion
    }

    topic = "oferta-donaciones"
    
    producer.send(topic, oferta)
    producer.flush()
    print(f"[KafkaProd] Oferta publicada en {topic}: {oferta}")
    return jsonify({"status": "Oferta enviada a Kafka"}), 200
    

## Baja Solicitud Donaciones

@app.route('/baja-solicitud-donaciones', methods=['POST'])
def ProducirBajaDonacion():
    global producer
    data = request.json

    idOrganizacionSolicitante = data.get("idOrganizacionSolicitante")
    idSolicitud = data.get("idSolicitud")

    baja = {
        "idOrganizacionSolicitante": idOrganizacionSolicitante,
        "idSolicitud": idSolicitud
    }

    topic = 'baja-solicitud-donaciones'
    
    producer.send(topic, baja)
    producer.flush()
    print(f"[KafkaProd] Baja publicada en {topic}: {baja}")
    return jsonify({"status": "Baja enviada a Kafka"}), 200


## Publicar Evento

@app.route("/publicar-evento", methods=['POST'])
def ProducirPublicacion():
    global producer
    data = request.json
    
    idOrganizacion = data.get("idOrganizacion")
    idEvento = data.get("idEvento")
    nombreEvento = data.get("nombreEvento")
    descripcion = data.get("descripcion")
    fechaHora = data.get("fechaHora")

    publicar = {
        "idOrganizacion": idOrganizacion,
        "idEvento": idEvento,
        "nombreEvento": nombreEvento,
        "descripcion": descripcion,
        "fechaHora": fechaHora
    }

    topic = 'publicar-evento'

    producer.send(topic, publicar)
    producer.flush()
    return jsonify({"status": "Publicacion enviada a Kafka"}), 200


## Baja Evento

@app.route('/baja-evento-solidario', methods=['POST'])
def ProducirBajaEvento():
    global producer
    data = request.json

    idOrganizacion = data.get("idOrganizacion")
    idEvento = data.get("idEvento")

    baja = {
        "idOrganizacion": idOrganizacion,
        "idEvento": idEvento
    }

    topic = 'baja-evento-solidario'
    
    producer.send(topic, baja)
    producer.flush()
    print(f"[KafkaProd] Baja Evento publicada en {topic}: {baja}")
    return jsonify({"status": "Baja Evento enviada a Kafka"}), 200


## Adhesion Evento

@app.route('/adhesion-evento', methods=['POST'])
def ProducirAdhesion():
    global producer
    data = request.json

    idEvento = data.get("idEvento")
    idOrganizador = data.get("idOrganizador")
    voluntario = data.get("voluntario", {})

    voluntario_recibido = {
        "idOrganizacion": voluntario.get("idOrganizacion"),
        "idVoluntario": voluntario.get("idVoluntario"),
        "nombre": voluntario.get("nombre"),
        "apellido": voluntario.get("apellido"),
        "telefono": voluntario.get("telefono"),
        "email": voluntario.get("email")
    }
    
    adhesion = {
        "idEvento": idEvento,
        "voluntario": voluntario_recibido
    }

    topic = f"adhesion-evento_{idOrganizador}"
    producer.send(topic, adhesion)
    producer.flush()

    print(f"[KafkaProd] Adhesiom publicada en {topic}: {adhesion}")
    return jsonify({"status": "Adhesion enviada a Kafka"}), 200    


## Cerrar Producer

def CerrarProducer():
    global producer
    if producer is not None:
        producer.flush()
        producer.close()
        print("[KafkaProd] Producer cerrado")
        producer = None

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
