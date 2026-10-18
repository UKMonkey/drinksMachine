import time


class DrinkDispenser:

    @classmethod
    def make_drink(cls, recipe, glass_size, progress_callback=None):
        print("========================================")
        print(f"DISPENSER: Starting to pour '{recipe.name}' into '{glass_size['name']}'")

        for ingredient in recipe.ingredients:
            print(f" -> Pumping {ingredient.amount_ml:.1f} ml of '{ingredient.name}'")

        print("DISPENSER: Dispensing in progress...")

        total_steps = 5  # 30 seconds simulation
        for step in range(total_steps + 1):
            percent = int((step / total_steps) * 100)
            if progress_callback:
                progress_callback(percent)

            if step < total_steps:
                time.sleep(1)

        print("DISPENSER: Pour complete successfully!")
        print("========================================")