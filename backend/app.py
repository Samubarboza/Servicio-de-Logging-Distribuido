from flask import Flask
from backend.routes.logs import bp_logs
from backend.db.session import BaseModelo, motor_bd

def crear_aplicacion():
    app = Flask(__name__)

    # Crear tablas si no existen
    BaseModelo.metadata.create_all(bind=motor_bd)

    # Registrar endpoints
    app.register_blueprint(bp_logs)

    # Ruta simple de salud
    @app.get("/salud")
    def ruta_salud():
        return {"estado": "ok"}, 200

    return app

if __name__ == "__main__":
    app = crear_aplicacion()
    app.run(host="127.0.0.1", port=8000, debug=True)
