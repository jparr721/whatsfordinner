import gzip
import json
import pickle
from dataclasses import dataclass
from typing import Any, Dict, List

from thefuzz import fuzz


@dataclass
class Recipe:
    name: str
    ingredients: List[str]
    directions: List[str]
    categories: List[str]

    def is_dinner(self):
        return "dessert" in self.categories or "desserts" in self.categories

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

    def to_json(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "ingredients": self.ingredients,
            "directions": self.directions,
            "categories": self.categories,
        }


if __name__ == "__main__":
    with gzip.open("processed.bin.gz", "rb") as f:
        recipes = pickle.load(f)

    for r, recipe in enumerate(recipes):
        for i, ingredient in enumerate(recipe.ingredients):
            ingredient = ingredient.replace("½", "1/2")
            ingredient = ingredient.replace("¼", "1/4")
            ingredient = ingredient.replace("¾", "3/4")
            recipes[r].ingredients[i] = ingredient

    all_categories = set()
    for recipe in recipes:
        all_categories.update(recipe.categories)

    # lowercase all categories
    all_categories = {category.lower() for category in all_categories}

    # strip all categories
    all_categories = {category.strip() for category in all_categories}

    # Group all categories that are similar (ratio above 85)
    similar_categories = {}
    for category in all_categories:
        similar_categories[category] = []
    for category in all_categories:
        for similar_category in all_categories:
            if (
                category != similar_category
                and fuzz.partial_ratio(category, similar_category) > 95
            ):
                similar_categories[category].append(similar_category)

    # Sort by key
    similar_categories = dict(sorted(similar_categories.items()))

    final_categories = set()
    for category, similar_categories in similar_categories.items():
        if len(similar_categories) == 0:
            final_categories.add(category)
        else:
            plural = max([category] + similar_categories, key=len)
            final_categories.add(plural)

    # Remove the *To Try* category
    final_categories.remove("*to try*")

    # Now, I need to go through the recipes and replace the categories with the final categories.
    # We will do this by iterating through the categories, and replacing each entry with the
    # entry from the final_categories whose ratio is the highest.
    for r, recipe in enumerate(recipes):
        new_categories = []
        for category in recipe.categories:
            best_match = max(
                final_categories, key=lambda x: fuzz.partial_ratio(category, x)
            )

            # Remove the *To Try* category
            if category.lower() == "*to try*":
                continue

            new_categories.append(best_match)

        recipes[r].categories = new_categories

    json_vals = [recipe.to_json() for recipe in recipes]
    with open("processed.json", "w") as f:
        json.dump(json_vals, f)
