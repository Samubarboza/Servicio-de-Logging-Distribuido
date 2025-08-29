from sqlalchemy import create_engine # crea la conexion a la base de datos
from sqlalchemy.orm import sessionmaker, declarative_base # herramienta orm (sessiones y modelos)
from backend.config import url_base_datos # url de la base de datos desde config.py (.env)

# motor_bd es el motor de conexion (usa la url de la BD)
motor_bd = create_engine(url_base_datos)

# CrearSesion sirve para abrir sessiones con la BD (leer/escribir datos)
CrearSesion = sessionmaker(
    bind=motor_bd, # a que motor conectamos
    autoflush=False, # no guarda cambios automaticamente
    autocommit=False # requiere commit manual
)

# BaseModelo es la clase base para definir modelos (tablas)
BaseModelo = declarative_base()

# este archivo configura la conexion con la base de datos