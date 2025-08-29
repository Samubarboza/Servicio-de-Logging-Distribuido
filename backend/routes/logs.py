
from flask import Blueprint, request, jsonify
from sqlalchemy import select, and_
from backend.auth.tokens import es_encabezado_autorizacion_valido
from backend.utils.validators import validar_diccionario_log, convertir_texto_a_datetime_iso8601
from backend.db.session import CrearSesion
from backend.db.models import RegistroLog
from backend.config import limite_por_defecto, limite_maximo

bp_logs = Blueprint("bp_logs", __name__)

@bp_logs.route("/logs", methods=["POST"])
def crear_logs():
    # 1) Autenticación
    encabezado_autorizacion = request.headers.get("Authorization")
    if not es_encabezado_autorizacion_valido(encabezado_autorizacion):
        return jsonify({"error": "Quién sos, bro?"}), 401

    # 2) JSON (un log o lista de logs)
    cuerpo_json = request.get_json(silent=True)
    if cuerpo_json is None:
        return jsonify({"error": "JSON inválido"}), 400
    lista_entradas = cuerpo_json if isinstance(cuerpo_json, list) else [cuerpo_json]

    # 3) Validación de cada log
    try:
        lista_datos_validados = [validar_diccionario_log(item) for item in lista_entradas]
    except ValueError as error_validacion:
        return jsonify({"error": str(error_validacion)}), 400

    # 4) Guardado en base (bulk)
    with CrearSesion() as sesion:
        objetos_a_guardar = [RegistroLog(**datos) for datos in lista_datos_validados]
        sesion.add_all(objetos_a_guardar)
        sesion.commit()

    return jsonify({"registros_guardados": len(lista_datos_validados)}), 200


@bp_logs.route("/logs", methods=["GET"])
def listar_logs():
    # 1) Leer filtros (en español, explícitos)
    texto_fecha_hora_evento_desde = request.args.get("fecha_hora_evento_desde")
    texto_fecha_hora_evento_hasta = request.args.get("fecha_hora_evento_hasta")
    texto_recibido_en_desde = request.args.get("recibido_en_desde")
    texto_recibido_en_hasta = request.args.get("recibido_en_hasta")

    texto_limite_resultados = request.args.get("limite", str(limite_por_defecto))
    texto_desplazamiento = request.args.get("desplazamiento", "0")

    # 2) Convertir parámetros a tipos correctos
    try:
        limite_resultados = min(int(texto_limite_resultados), limite_maximo)
        desplazamiento_resultados = int(texto_desplazamiento)
    except ValueError:
        return jsonify({"error": "limite/desplazamiento deben ser números enteros"}), 400

    # 3) Construir filtros de fechas si vienen
    lista_condiciones = []
    try:
        if texto_fecha_hora_evento_desde:
            lista_condiciones.append(
                RegistroLog.fecha_hora_evento >= convertir_texto_a_datetime_iso8601(texto_fecha_hora_evento_desde)
            )
        if texto_fecha_hora_evento_hasta:
            lista_condiciones.append(
                RegistroLog.fecha_hora_evento <= convertir_texto_a_datetime_iso8601(texto_fecha_hora_evento_hasta)
            )
        if texto_recibido_en_desde:
            lista_condiciones.append(
                RegistroLog.recibido_en >= convertir_texto_a_datetime_iso8601(texto_recibido_en_desde)
            )
        if texto_recibido_en_hasta:
            lista_condiciones.append(
                RegistroLog.recibido_en <= convertir_texto_a_datetime_iso8601(texto_recibido_en_hasta)
            )
    except ValueError as error_fechas:
        return jsonify({"error": str(error_fechas)}), 400

    # 4) Ejecutar consulta
    with CrearSesion() as sesion:
        consulta = select(RegistroLog)
        if lista_condiciones:
            consulta = consulta.where(and_(*lista_condiciones))
        consulta = consulta.order_by(RegistroLog.recibido_en.desc()).offset(desplazamiento_resultados).limit(limite_resultados)
        filas = sesion.execute(consulta).scalars().all()

    # 5) Salida clara en español
    lista_salida = [{
        "id": fila.id,
        "fecha_hora_evento": fila.fecha_hora_evento.isoformat(),
        "nombre_servicio": fila.nombre_servicio,
        "nivel_severidad": fila.nivel_severidad,
        "mensaje_evento": fila.mensaje_evento,
        "recibido_en": fila.recibido_en.isoformat(),
    } for fila in filas]

    return jsonify({"cantidad_resultados": len(lista_salida), "items": lista_salida}), 200
