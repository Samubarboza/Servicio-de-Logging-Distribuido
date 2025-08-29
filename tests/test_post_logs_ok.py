import json # para convertir diccionario python en texto json
from datetime import datetime # para generar la fecha y hora actual
from backend.app import crear_aplicacion # funcion que crea la app de flask

# test que prueba que POST /logs guarda un log correctamente
def test_post_logs_exitoso():
    app = crear_aplicacion() # crea la aplicacion flask
    cliente = app.test_client() # cliente de pruebas que simula peticiones http
    
    # encabezados http (tipo contenido y token valido)
    
    encabezados = {
        'Content-Type':'application/json',
        'Authorization': 'Token abc123'
    }
    
    # cuerpo del log a enviar (diccionario con datos correctos)
    cuerpo = {
        'timestamp':datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'),
        'service': 'servicio_pruebas',
        'severity': 'INFO',
        'messaje': 'todo ok'
    }

    # enviamos POST /logs con el cuerpo en formato JSON y los encabezados
    respuesta = cliente.post('/logs', data=json.dumps(cuerpo), headers=encabezados)
    
    # verificamos que el servidor responde 200 (ok)
    assert respuesta.status_code == 200
    # convertimos la respuesta en dict y chequeamos que guardo 1 registro
    data = respuesta.get_json()
    assert data['registros_guardados'] == 1