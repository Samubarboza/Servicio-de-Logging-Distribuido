import requests # liqueria para hacer las peticiones https (POST, GET, etc)
from datetime import datetime # libreria para obtener la fecha y hora actual

url_servidor = 'https://127.0.0.1:8000/logs' # url del endpoint /logs en el servidor flask
token_valido = 'abc123' # token que debe coincidir con lo guardado en el venv

# encabezados http que acompañan el POST
encabezados_http = {
    'Contect-Type': 'application/json', # indicamos que mandamos JSON
    'Authorization': f'Token {token_valido}' # autenticacion con token valido
}

# funccion que crea un diccionario con los datos del log
def crear_log_simple():
    return {
        'timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'), # fecha y hora actual en formato ISO
        'service': 'servicio_autenticacion', # Nombre del servicio que genera el log
        'severity': 'ERROR', # nivel de severidad del log
        'message': 'login fallido (usuario o clave incorrecta)' # mensaje descriptivo
    }
    
# bloque principal que se ejecuta si corremos el archivo
if __name__ == '__main__':
    cuerpo = crear_log_simple() # generamos el log (diccionario con datos)
    # hacemos POST al servidor enviando JSON y encabezados
    respuesta = requests.post(url_servidor, json=cuerpo, headers=encabezados_http, timeout=10)
    # imprimimos codigo de respuesta (200, 500, etc)
    print('status', respuesta.status_code)
    # imprimimos el contenido de la respuesta del servidor
    print('respuesta:', respuesta.text)