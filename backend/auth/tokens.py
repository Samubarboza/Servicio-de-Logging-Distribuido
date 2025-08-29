# importamos lista de tokens validos que definimos en el entorno
from backend.config import lista_tokens_permitidos

# espera: Authorization: Token TU_TOKEN
# devuelve true si TU_TOKEN esta en la lista blanca
def es_encabezado_autorizacion_valido(encabezado_autorizacion: str | None) -> bool:
    # si el header no trae el header Authorization, rechazamos al toque
    if not encabezado_autorizacion:
        return False
    
    # dividimos el header, convertimos en listas
    partes = encabezado_autorizacion.split()
    
    if len(partes) != 2 or partes[0].lower() != 'token': # convertimos en minusculas y verificamos
        return False
    
    token_enviado = partes[1] # guardamos la segunda parte 
    return token_enviado in lista_tokens_permitidos # revisamos si ese valor esta dentro de la lista de tokens (definido en .env)
# si esta, devuelve true, si no, false.

    