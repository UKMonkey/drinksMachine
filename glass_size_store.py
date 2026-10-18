import json
from pathlib import Path


class GlassSizeStore:
    _glass_sizes = []

    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "data"
    CONFIG_FILE = DATA_DIR / "glassSizeData.json"

    @classmethod
    def load(cls):
        """Load glass sizes from the JSON configuration file."""
        cls._glass_sizes = []

        # Check home directory path pattern if needed, or default to data/glassSizeData.json
        file_path = cls.CONFIG_FILE
        home_path = Path.home() / "drinksMachine" / "data" / "glassSizeData.json"
        if home_path.exists():
            file_path = home_path

        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    cls._glass_sizes = data if isinstance(data, list) else data.get("glass_sizes", [])
                print(f"GlassSizeStore: Loaded {len(cls._glass_sizes)} glass sizes from {file_path}")
            except Exception as ex:
                print(f"GlassSizeStore: Failed to load glass size file: {ex}")
        else:
            print(f"GlassSizeStore: File not found at {file_path}, using defaults.")
            # Default fallback if file doesn't exist yet
            cls._glass_sizes = [
                {"name": "Standard Glass (250ml)", "multiplier": 1.0, "capacity_ml": 250},
                {"name": "Large Glass (400ml)", "multiplier": 1.6, "capacity_ml": 400}
            ]

        return cls._glass_sizes

    @classmethod
    def get_glass_sizes(cls):
        if not cls._glass_sizes:
            cls.load()
        return cls._glass_sizes