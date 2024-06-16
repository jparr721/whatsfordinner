import pickle
from typing import List, Dict, Any
from dataclasses import dataclass
import random
import gzip


@dataclass
class Recipe:
    name: str
    ingredients: List[str]
    directions: List[str]
    categories: List[str]

    def is_dinner(self):
        return "dessert" in categories or "desserts" in categories

    @staticmethod
    def from_json(data: Dict[str, Any]):
        keys = data.keys()
        for key in ["name", "ingredients", "directions"]:
            if key not in keys:
                raise KeyError(f"Recipe missing key: {key}")

        return Recipe(
            data["name"].strip(),
            data["ingredients"].strip().split("\n"),
            data["directions"].strip().split("\n"),
            data["categories"],
        )


def decide(recipe: Recipe):
    print(f"Let's make, {recipe.name}")
    for ingredient in recipe.ingredients:
        if ingredient == "":
            continue
        if not any(
            c in ingredient.lower()
            for c in [
                "taste",
                "pinch",
                "bit",
                "salt",
                "pepper",
                "paprika",
                "cumin",
                "chili",
                "handful",
                "fresh",
                "½",
                "¼",
            ]
        ) and not any(c.isdigit() for c in ingredient):
            print(f"\n{ingredient.title()}\n{len(ingredient)*'='}")
            continue

        input_ = input(f"{ingredient}? [Y/n]: ").lower()
        if input_ == "" or input_ == "y":
            continue
        else:
            print("This one won't work :(")
            return
    else:
        print("LETS FUCKING GOOOOO")


if __name__ == "__main__":
    with gzip.open("processed.bin.gz", "rb") as f:
        data = pickle.load(f)
        choice = random.choice(data)
        decide(choice)
