import json
from drink_recipe import DrinkRecipe
from unit_converter import UnitConverter


class RecipeLoader:

    def load(self, filename):
        recipes = []

        with open(filename, "r", encoding="utf-8-sig") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as ex:
                raise ValueError(f"Invalid JSON format in recipe file: {ex}")

        # Support both a list of recipes or a dictionary containing a recipes key
        recipe_list = data if isinstance(data, list) else data.get("recipes", [])

        for index, item in enumerate(recipe_list, start=1):
            drink_name = item.get("name", "").strip()

            if not drink_name:
                raise ValueError(f"Recipe item {index}: missing drink name")

            recipe = DrinkRecipe(drink_name)
            ingredients_data = item.get("ingredients", [])

            for ing_index, ing in enumerate(ingredients_data, start=1):
                ingredient_name = ing.get("name", "").strip()

                if not ingredient_name:
                    raise ValueError(f"Recipe '{drink_name}' (Item {index}), Ingredient {ing_index}: missing ingredient name")

                try:
                    amount = float(ing.get("amount"))
                except (TypeError, ValueError):
                    raise ValueError(f"Recipe '{drink_name}', Ingredient '{ingredient_name}': invalid or missing amount")

                unit = ing.get("unit", "").strip()

                # Convert amount to milliliters using your existing UnitConverter
                amount_ml = UnitConverter.to_ml(amount, unit)

                recipe.add_ingredient(ingredient_name, amount_ml)

            recipes.append(recipe)

        print(f"Successfully loaded {len(recipes)} recipes from JSON")
        return recipes