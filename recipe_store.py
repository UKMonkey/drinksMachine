from pathlib import Path
from recipe_loader import RecipeLoader


class RecipeStore:
    _instance = None
    _recipes = []

    @classmethod
    def get_recipe_file_path(cls) -> Path:
        # Check home directory first (where updates are copied), fallback to local data if needed
        home_path = Path.home() / "drinksMachine" / "data" / "drinksRecipes.json"
        if home_path.exists():
            return home_path

        # Fallback to local project data directory
        base_dir = Path(__file__).resolve().parent
        return base_dir / "data" / "drinksRecipes.json"

    @classmethod
    def load(cls):
        loader = RecipeLoader()
        recipe_file = cls.get_recipe_file_path()
        if recipe_file.exists():
            cls._recipes = loader.load(recipe_file)
        else:
            print(f"Recipe file not found at {recipe_file}")
            cls._recipes = []
        return cls._recipes

    @classmethod
    def get_recipes(cls):
        if not cls._recipes:
            cls.load()
        return cls._recipes