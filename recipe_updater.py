import shutil
from pathlib import Path


class RecipeUpdater:

    RECIPE_FILENAME = "drinksRecipes.txt"

    def update(self):
        destination_dir = Path.home() / "drinksMachine" / "data"
        destination_dir.mkdir(parents=True, exist_ok=True)

        search_locations = [Path("/media/pi"), Path("/media"), Path("/run/media/pi")]

        source_file = None

        for location in search_locations:
            if not location.exists():
                continue

            for file in location.rglob(self.RECIPE_FILENAME):
                source_file = file
                break

            if source_file:
                break

        if source_file is None:
            raise FileNotFoundError(
                f"Could not find {self.RECIPE_FILENAME} on any USB device"
            )

        destination_file = destination_dir / self.RECIPE_FILENAME

        shutil.copy2(source_file, destination_file)
        print(f"Copied $source_file to $destination_file")

        return source_file, destination_file
