import logging

from flask_smorest import Blueprint

from flask.views import MethodView
from src.api.decorators.check_secret import check_secret
from src.api.exceptions.http import HTTPBadRequestException
from src.api.schemas.predictions import (
    PredictionHeadersSchema,
    PredictionRequestSchema,
    PredictionResponseSchema,
)
from src.paul.exceptions import InvalidEventException
from src.paul.predictions import predict

logger = logging.getLogger(__name__)

blueprint = Blueprint(
    name="predictions",
    import_name=__name__,
    url_prefix="/predictions",
    description="Predictions operations",
)


@blueprint.route("")
class Predictions(MethodView):
    @check_secret
    @blueprint.arguments(PredictionHeadersSchema, location="headers")
    @blueprint.arguments(PredictionRequestSchema)
    @blueprint.response(200, PredictionResponseSchema)
    def post(self, _, payload):
        logger.debug(f"Payload: {payload}")

        try:
            return predict(**payload)
        except InvalidEventException as e:
            raise HTTPBadRequestException(str(e)) from e
