# validacion de datos de logs
from datetime import datetime

# conjunto de severidades permitidas (niveles de logs validos)
conjunto_severidades_permitidas = {'INFO', 'DEBUG', 'ERROR', 'WARN', 'WARNING'}

# convierte texto en formato ISO8601 a ojeto datetime
def convertir_texto_a_datetime_iso8601(texto_fecha_hora: str) -> datetime:
    # devuelve un datetime o lanza valueError
    texto = texto_fecha_hora.rstrip('Z') # saca 'Z' del final si existe
    # intenta dos formatos: con milisegundos y sin milisegundos
    for formato in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(texto, formato) # convierte string a datetime
        except ValueError:
            continue # Si falla, prueba con el otro formato
    # si ninguno funciona, lanza error
    raise ValueError('timestamp no tiene formato ISO 8601')

# Valida que un diccionario de log tenga todos los campos y valores correctos
def validar_diccionario_log(diccionario_entrada: dict) -> dict:
    # verifica que existan y sean validos - timestamp, service, severity, message. Devuelve un dict listo para crear RegistroLog
    campos_obligatorios = ('timestamp', 'service', 'severity', 'message')
    for nombre_campo in campos_obligatorios:
        if nombre_campo not in diccionario_entrada:
            raise ValueError(f'Falle el campo: {nombre_campo}') # error si falla algo
        
    # convierte el timestamp de string a datetime
    fecha_hora_evento = convertir_texto_a_datetime_iso8601(diccionario_entrada['timestamp'])
    
    # normaliza y valida la severidad
    nivel_severidad = str(diccionario_entrada['severity']).upper().strip() # upper:convierte todo en mayuscula - strip: borra espacios y otros caracteres de incio de final
    if nivel_severidad == 'WARNING':
        nivel_severidad = 'WARN' # cambia warning a war
    if nivel_severidad not in conjunto_severidades_permitidas:
        raise ValueError('severity invalido (use INFO/DEBUG/ERROR/WARN)') # raise usamos para lanzar error
    
    # valida que servicio y mensajes no esten vacios
    nombre_servicio = str(diccionario_entrada['service']).strip()
    mensaje_evento = str(diccionario_entrada['message']).strip()
    if not nombre_servicio or not mensaje_evento:
        raise ValueError('service o message esta vacio')
    
    # devuelve un diccionario limpio y listo para guardar en la BD
    return {
        'fecha_hora_evento': fecha_hora_evento,
        'nombre_servicio': nombre_servicio,
        'nivel_severidad': nivel_severidad,
        'mensaje_evento': mensaje_evento
    }