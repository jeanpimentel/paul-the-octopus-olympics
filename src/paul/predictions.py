import abc
import logging
from random import randint
from typing import Dict, Optional

from src.paul.dtos import Prediction
from src.paul.enums import NOC, Competition, League, OlympicEvents, ParalympicEvents
from src.paul.exceptions import InvalidEventException

logger = logging.getLogger(__name__)


class AbstractPredictor(abc.ABC):
    @abc.abstractmethod
    def predict(self, league: League, event, predictions=None) -> Prediction:
        raise NotImplementedError

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class OlympicsPredictor(AbstractPredictor):
    def predict(
        self, league: League, event: OlympicEvents, predictions=None
    ) -> Prediction:
        return Prediction(
            gold=NOC.UNITED_STATES_OF_AMERICA,
            silver=NOC.PEOPLES_REPUBLIC_OF_CHINA,
            bronze=NOC(randint(1, 206)),
        )


class ParalympicsPredictor(AbstractPredictor):
    def predict(
        self, league: League, event: ParalympicEvents, predictions=None
    ) -> Prediction:
        return Prediction(
            gold=NOC(randint(1, 206)),
            silver=NOC(randint(1, 206)),
            bronze=NOC(randint(1, 206)),
        )


def predict(
    league: League,
    competition: Competition,
    id_event: int,
    predictions: Optional[Dict[str, Dict[NOC, float]]] = None,
    **kwargs,
) -> Prediction:
    if competition is Competition.OLYMPICS:
        try:
            event = OlympicEvents(id_event)
        except Exception as e:
            raise InvalidEventException(
                f"Invalid event id {id_event} for " f"competition {competition}"
            ) from e

        predictor = OlympicsPredictor()
    elif competition is Competition.PARALYMPICS:
        try:
            event = ParalympicEvents(id_event)
        except Exception as e:
            raise InvalidEventException(
                f"Invalid event id {id_event} for " f"competition {competition}"
            ) from e

        predictor = ParalympicsPredictor()
    else:
        raise ValueError("Invalid Competition")

    logger.debug(f"League: {league}")
    logger.debug(f"Competition: {competition}")
    logger.debug(f"Event: {event}")
    logger.debug(f"Predictor: {predictor}")
    logger.debug(f"Test Mode: {kwargs.get('test_mode')}")

    return predictor.predict(league=league, event=event, predictions=predictions)
