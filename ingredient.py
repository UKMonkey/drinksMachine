from dataclasses import dataclass


@dataclass
class Ingredient:
    name: str
    amount_ml: float
