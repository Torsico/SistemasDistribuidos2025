import grpc
from kafka import KafkaConsumer
import json
import os
import threading
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "proto"))
from proto import messages_pb2, messages_pb2_grpc

KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
GRPC_SERVER = os.environ.get("GRPC_SERVER", "localhost:9090")

channel = grpc.insecure_channel(GRPC_SERVER)
stub = messages_pb2_grpc.MessagesServiceStub(channel)


def ConsumirSolicitudDonaciones():
    topic = "solicitud-donaciones"
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="solicitud_donaciones_group"
    )
    print(f"[KafkaCons] Escuchando {topic}")

    for msg in consumer:
        m = msg.value
        print(f"[{topic}] Mensaje recibido: {m}")
        solicitud = messages_pb2.SolicitudDonacion(
            idOrganizacionSolicitante=m["idOrganizacionSolicitante"],
            idSolicitud=m["idSolicitud"],
        )
        for d in m.get("donacion", []):
            solicitud.donacion.add(categoria=d["categoria"], descripcion=d["descripcion"])
        stub.AltaSolicitudDonacion(solicitud)
        print("Solicitud de donación registrada vía gRPC")


def ConsumirTransferenciaDonaciones():
    consumer = KafkaConsumer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="transferencia_donaciones_group"
    )

    consumer.subscribe(pattern=r'^transferencia_donaciones_.*$')     ## Regex para aceptar todos los topic que empiecen con...
    
    print(f"[KafkaCons] Escuchando..")

    for msg in consumer:
        topic = msg.topic
        m = msg.value
        print(f"[{topic}] Mensaje recibido: {m}")
        transferencia = messages_pb2.TransferenciaDonacion(
            idSolicitud=m["idSolicitud"],
            idOrganizacionDonante=m["idOrganizacionDonante"],
            idOrganizacionSolicitante=m["idOrganizacionSolicitante"]
        )
        for d in m["donacion"]:
            transferencia.donacion.add(
                categoria=d["categoria"],
                descripcion=d["descripcion"],
                cantidad=d["cantidad"]
            )
        stub.RegistrarTransferencia(transferencia)
        print("Transferencia registrada vía gRPC")


def ConsumirOfertaDonaciones():
    topic = "oferta-donaciones"
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="oferta_donaciones_group"
    )
    print(f"[KafkaCons] Escuchando {topic}")

    for msg in consumer:
        m = msg.value
        print(f"[{topic}] Mensaje recibido: {m}")
        oferta = messages_pb2.OfertaDonacion(
            idOferta=m["idOferta"],
            idOrganizacionDonante=m["idOrganizacionDonante"]
        )
        for d in m["donacion"]:
            oferta.donacion.add(
                categoria=d["categoria"],
                descripcion=d["descripcion"],
                cantidad=d["cantidad"]
            )
        stub.AltaOferta(oferta)
        print("Oferta registrada vía gRPC")


def ConsumirBajaSolicitud():
    topic = "baja-solicitud-donaciones"
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="baja_solicitud_group"
    )
    print(f"[KafkaCons] Escuchando {topic}")

    for msg in consumer:
        m = msg.value
        print(f"[{topic}] Mensaje recibido: {m}")
        baja = messages_pb2.BajaSolicitud(
            idOrganizacionSolicitante=m["idOrganizacionSolicitante"],
            idSolicitud=m["idSolicitud"]
        )
        stub.BajaSolicitudDonacion(baja)
        print("Solicitud dada de baja vía gRPC")


def ConsumirPublicarEvento():
    topic = "publicar-evento"
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="publicar_evento_group"
    )
    print(f"[KafkaCons] Escuchando {topic}")

    for msg in consumer:
        m = msg.value
        print(f"[{topic}] Mensaje recibido: {m}")
        evento = messages_pb2.EventoExterno(
            idOrganizacion=m["idOrganizacion"],
            idEvento=m["idEvento"],
            nombreEvento=m["nombreEvento"],
            descripcion=m["descripcion"],
            fechaHora=m["fechaHora"]
        )
        stub.PublicarEventoExterno(evento)
        print("Evento publicado vía gRPC")


def ConsumirBajaEvento():
    topic = "baja-evento-solidario"
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="baja_evento_group"
    )
    print(f"[KafkaCons] Escuchando {topic}")

    for msg in consumer:
        m = msg.value
        print(f"[{topic}] Mensaje recibido: {m}")
        baja = messages_pb2.BajaEvento(
            idOrganizacion=m["idOrganizacion"],
            idEvento=m["idEvento"]
        )
        stub.BajaEventoExterno(baja)
        print("Evento externo dado de baja vía gRPC")


def ConsumirAdhesionEvento():
    consumer = KafkaConsumer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="adhesion_evento_group"
    )

    consumer.subscribe(pattern=r'^adhesion-evento_.*$')     ## Regex para aceptar todos los topic que empiecen con...
    
    print(f"[KafkaCons] Escuchando...")

    for msg in consumer:
        topic = msg.topic
        m = msg.value
        print(f"[{topic}] Mensaje recibido: {m}")
        adhesion = messages_pb2.AdhesionEvento(
            idEvento=m["idEvento"],
            voluntario=messages_pb2.Voluntario(
                idOrganizacion=m["voluntario"]["idOrganizacion"],
                idVoluntario=m["voluntario"]["idVoluntario"],
                nombre=m["voluntario"]["nombre"],
                apellido=m["voluntario"]["apellido"],
                telefono=m["voluntario"]["telefono"],
                email=m["voluntario"]["email"]
            )
        )
        stub.RegistrarAdhesionEvento(adhesion)
        print("Adhesión registrada vía gRPC")


if __name__ == "__main__":
    threads = [
        threading.Thread(target=ConsumirSolicitudDonaciones),
        threading.Thread(target=ConsumirTransferenciaDonaciones),
        threading.Thread(target=ConsumirOfertaDonaciones),
        threading.Thread(target=ConsumirBajaSolicitud),
        threading.Thread(target=ConsumirPublicarEvento),
        threading.Thread(target=ConsumirBajaEvento),
        threading.Thread(target=ConsumirAdhesionEvento),
    ]

    for t in threads:
        t.start()