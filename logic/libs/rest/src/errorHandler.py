from flask import Flask
from logic.libs.exception.exception import AppException, UnknownException
from logic.libs.logger.logger import logger
from werkzeug.exceptions import HTTPException


def load_generic_error_handler(app: Flask):
    """
    Carga el handler de error basico para manejo de AppExceptions y excepciones comunes
    """
    @app.errorhandler(HTTPException)
    def handle_exception(httpe):
        return '', httpe.code

    @app.errorhandler(AppException)
    def handle_business_exception(ae: AppException):
        logger().warning(ae.to_json())
        return ae.to_json(), 409

    @app.errorhandler(Exception)
    def handle_exception(e: Exception):
        logger().exception(e)
        return UnknownException(e).to_json(), 500
