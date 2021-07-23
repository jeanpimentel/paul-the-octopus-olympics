from dataclasses import dataclass

from src.paul.enums import NOC


@dataclass(frozen=True)
class Prediction:
    gold: NOC
    silver: NOC
    bronze: NOC
