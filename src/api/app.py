import http
import logging.handlers
import os
from datetime import datetime

import coloredlogs
from flask import Flask, json, jsonify, redirect
from flask_cors import CORS
from flask_smorest import Api

from .blueprints import predictions
from .config import load_configs
from .exceptions.http import HTTPException

log_level = os.environ.get("LOG_LEVEL", "WARNING").upper()

logging.basicConfig(level=log_level)

coloredlogs.install(
    level=log_level,
    datefmt="%H:%M:%S",
    fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
)

app = load_configs(Flask(__name__))

# allowing Cross origin requests
CORS(app)

# Wrapping the app
api = Api(app)

# Blueprints
api.register_blueprint(predictions.blueprint)


# Errors
@app.errorhandler(HTTPException)
def handle_http_exception(error: HTTPException):
    app.logger.exception(f"HTTP Exception")

    return jsonify({"error": True, "message": error.message}), error.status_code


@app.errorhandler(Exception)
def handle_exception(e: Exception):
    """Handles uncaught exceptions that are not of type HTTPException"""
    app.logger.exception(f"Uncaught exception: {e}")

    return (
        jsonify(
            {
                "error": True,
                "message": "",
            }
        ),
        http.HTTPStatus.INTERNAL_SERVER_ERROR,
    )


@app.route("/")
def main_page():
    return redirect("/doc/swagger-ui")


@app.route("/ping", methods=["GET"])
def ping():
    from ..paul import __version__ as paul_version

    return json.jsonify({"now": datetime.now(), "version": paul_version})
