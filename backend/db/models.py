from sqlalchemy import Column, Integer, String, DateTime, Index # herramientas para definir columnas e indices
from datetime import datetime # para usar fecha/hora actual
from backend.db.session import BaseModelo # clase para modelos (tablas)

# Clase que representa la tabla 'registros_log' en la base de datos
class RegistroLog(BaseModelo):
    __tablename__ = 'registros_log' # nombre real de la tabla en la base de datos
    
    id = Column(Integer, primary_key=True) # id unico, clave primaria
    # Momento en que ocurrio el evento
    fecha_hora_evento = Column(DateTime, nullable=False)
    # nombre del servicio que genero
    nombre_servicio = Column(String(100), nullable=False)
    # nivel de importancia: INFO, DEBUG, ERROR, WARN
    nivel_severidad = Column(String(20), nullable=False)
    # texto descriptivo del evento
    mensaje_evento = Column(String(1000), nullable=False)
    # momento en el que el servidor recibio el log (se asigna automaticamente al guardar)
    recibido_en = Column(DateTime, nullable=False, default=datetime.utcnow)
