import os
import json
from dataclasses import dataclass
from typing import List, Dict, Any
import pickle


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


if __name__ == "__main__":
    recipes = []
    allcategories = set()

    for file in os.listdir("recipes"):
        fullpath = os.path.join("recipes", file)
        content = json.load(open(fullpath))
        for key in content.keys():
            for category in content["categories"]:
                allcategories.add(category.lower())
        recipes.append(Recipe.from_json(content))

    with open("processed.bin", "wb+") as f:
        pickle.dump(recipes, f)
