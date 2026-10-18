class DrinkDispenser:

    @classmethod
    def make_drink(cls, recipe, glass_size):
        """
        Stub method to handle hardware dispensing logic.
        Communicates with pumps based on recipe ingredients, quantities,
        and glass size multipliers.
        """
        multiplier = glass_size.get("multiplier", 1.0)
        print("========================================")
        print(f"DISPENSER: Starting to pour '{recipe.name}' into '{glass_size['name']}'")
        print(f"Volume Multiplier: {multiplier}x")

        for ingredient in recipe.ingredients:
            scaled_amount = ingredient.amount * multiplier
            print(f" -> Pumping {scaled_amount:.1f} ml of '{ingredient.name}'")

        print("DISPENSER: Pour complete successfully!")
        print("========================================")

        # TODO: Add real hardware GPIO / motor controller triggers here