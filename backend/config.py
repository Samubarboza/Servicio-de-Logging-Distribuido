import os # modulo de python para leer variables de entorno
from dotenv import load_dotenv

# agarra el archivo .env y carga en el programa, sirve para que el programa lea url o configuraciones
load_dotenv()

url_base_datos = os.getenv("DB_URL", "sqlite:///logs.db") # 
lista_tokens_permitidos = [t.strip() for t in os.getenv("TOKENS", "").split(",") if t.strip()] # split convierte a lista, strip() borra los espacios al inicio y al final y devuelve un string limpio

limite_por_defecto = 50
limite_maximo = 500
