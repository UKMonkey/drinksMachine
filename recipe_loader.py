import csv

from drink_recipe import DrinkRecipe
from unit_converter import UnitConverter


class RecipeLoader:

    def load(self, filename):

        recipes = []

        with open(filename, newline="", encoding="utf-8-sig") as f:

            reader = csv.reader(f)

            for row_number, row in enumerate(reader, start=1):

                if not row:
                    continue

                drink_name = row[0].strip()

                if not drink_name:
                    raise ValueError(
                        f"Row {row_number}: missing drink name"
                    )

                if (len(row) - 1) % 3 != 0:
                    raise ValueError(
                        f"Row {row_number}: invalid column count ({len(row)})"
                    )

                recipe = DrinkRecipe(drink_name)

                for i in range(1, len(row), 3):

                    ingredient_name = row[i].strip()

                    if not ingredient_name:
                        raise ValueError(
                            f"Row {row_number}: missing ingredient name"
                        )

                    try:
                        amount = float(row[i + 1])
                    except ValueError:
                        raise ValueError(
                            f"Row {row_number}: invalid amount '{row[i + 1]}'"
                        )

                    unit = row[i + 2].strip()

                    amount_ml = UnitConverter.to_ml(
                        amount,
                        unit,
                    )

                    recipe.add_ingredient(
                        ingredient_name,
                        amount_ml,
                    )

                recipes.append(recipe)

        print(f"Successfully loaded {len(recipes)} recipes")

        return recipes