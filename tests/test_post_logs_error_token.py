import json # para convertir diccionario a json
from datetime import datetime # para generar la fecha/hora actual
from backend.app import crear_aplicacion # funcion para crear la app flask 

# test que prueba que POST /logs falla si el token es invalido
def test_post_logs_token_invalido():
    app = crear_aplicacion() # crea la aplicacion flask
    cliente = app.test_client() # cliente de pruebas que simula peticiones http
    
    # encabezados http con token incorrecto
    encabezados = {
        'Content-Type': 'application/json',
        'Authorization': 'Token token_invalido'
    }
    
    # cuerpo del log a enviar (formato correcto, pero token es invalido)
    cuerpo = {
        'timestamp': datetime.utcnow().strtime("%Y-%m-%dT%H:%M:%S"),
        'service': 'servicio_pruebas',
        'severity': 'INFO',
        'message': 'debe fallar'
    }
    
    # enviamos POST /logs con token incorrecto
    respuesta = cliente.post('/logs', data=json.dumps(cuerpo), headers=encabezados)
    
    # verificamos que responde al 401 (no autorizado)
    assert respuesta.status_code == 401
    # la respuesta debe contener un campo 'error'
    data = respuesta.get_json()
    assert 'error' in data
