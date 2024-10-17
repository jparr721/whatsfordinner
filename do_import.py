import json

import psycopg2

if __name__ == "__main__":
    conn = psycopg2.connect(
        host="apps1.aspen.networks",
        database="jarredtv",
        user="jarredtv",
        password="jarredtv",
    )
    cur = conn.cursor()

    with open("processed.json", "r") as f:
        recipes = json.load(f)

    for recipe in recipes:
        cur.execute(
            "INSERT INTO recipes (name, ingredients, directions, categories) VALUES (%s, %s, %s, %s)",
            (
                recipe["name"],
                recipe["ingredients"],
                recipe["directions"],
                recipe["categories"],
            ),
        )

    conn.commit()
    cur.close()
    conn.close()
