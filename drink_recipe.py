from dataclasses import dataclass, field
from typing import List

from ingredient import Ingredient


@dataclass
class DrinkRecipe:
    name: str
    ingredients: List[Ingredient] = field(default_factory=list)

    def add_ingredient(self, name: str, amount_ml: float):
        self.ingredients.append(
            Ingredient(
                name=name,
                amount_ml=amount_ml,
            )
        )

    @property
    def total_volume_ml(self) -> float:
        return sum(i.amount_ml for i in self.ingredients)

    def __str__(self):
        lines = [
            f"Drink: {self.name}",
            f"Total volume: {self.total_volume_ml:.1f} ml",
        ]

        for ingredient in self.ingredients:
            lines.append(f"  - {ingredient.name}: {ingredient.amount_ml:.1f} ml")

        return "\n".join(lines)
