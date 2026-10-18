class UnitConverter:

    CONVERSIONS = {
        # metric
        "ml": 1.0,
        "millilitre": 1.0,
        "millilitre": 1.0,
        "millilitres": 1.0,
        "l": 1000.0,
        "litre": 1000.0,
        "litres": 1000.0,
        # UK
        "uk teaspoon": 5.919,
        "uk tbsp": 17.758,
        "uk tablespoon": 17.758,
        "uk floz": 28.413,
        "uk fluid ounce": 28.413,
        "uk gill": 142.065,
        "uk pint": 568.261,
        "uk quart": 1136.523,
        "uk gallon": 4546.09,
        # US
        "us teaspoon": 4.929,
        "us tbsp": 14.787,
        "us tablespoon": 14.787,
        "us floz": 29.574,
        "us fluid ounce": 29.574,
        "us cup": 236.588,
        "us pint": 473.176,
        "us quart": 946.353,
        "us gallon": 3785.412,
    }

    @classmethod
    def to_ml(cls, amount, unit):
        key = unit.strip().lower()
        if key not in cls.CONVERSIONS:
            print(f"Unknown unit encountered: " f"'{unit}'")

            raise ValueError(f"Unknown unit: {unit}")

        return amount * cls.CONVERSIONS[key]
