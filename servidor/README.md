Grupo L: Trabajo grupal para la materia de sistemas distribuidos que implementa una arquitectura distribuida utilizando gRPC. El servidor gRPC está desarrollado en Python con PyJWT para manejo de tokens, mientras que el cliente gRPC está implementado en Ruby con Rails. La base de datos utilizada es MySQL.

1 - Requisitos

- MySQL Workbench
- Python 3.12.5
- gRPC 1.75.0

2 - Configuracion de la Base de Datos:
- Crear una nueva base de datos llamada dist2025
- *Temporalmente*. Las credenciales de la bd seran: User: root, Pass: root

3 - Configuracion gRPC
- Para funcionar gRPC es necesario instalar, ademas del mismo, sus herramientas:
	- python -m pip install grpcio grpcio-tools

3 - Configuracion del Servidor Python
- Para integrar python al proyecto es necesario tener python 3.12.5 (python -m pip install --upgrade pip)
- Y su conector de MySQL (pip install mysql-connector-python)
- Una vez instalado, ejecutar "python server.py" desde la carpeta server
