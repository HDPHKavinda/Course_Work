import os
import re
import main

recipe_counter = 0
recipes_storage = {}
DEFAULT_RECIPES_FILE = "recipes.txt"


def generate_recipe_id():
    global recipe_counter
    recipe_counter += 1
    return f"RCP{recipe_counter:03d}"


def recipe_name_exists(recipe_name, exclude_id=None):
    for recipe_id, recipe_data in recipes_storage.items():
        if exclude_id and recipe_id == exclude_id:
            continue
        if recipe_data["name"].lower() == recipe_name.lower():
            return True
    return False


def parse_ingredients_line(ingredient_text):
    if not ingredient_text:
        return []

    ingredients = []
    for item in ingredient_text.split("|"):
        parts = item.split(",")
        if len(parts) != 3:
            return None
        name = parts[0].strip()
        try:
            quantity = float(parts[1].strip())
        except ValueError:
            return None
        unit = parts[2].strip()
        if not name or unit not in main.units or quantity <= 0:
            return None
        ingredients.append({"name": name, "quantity": quantity, "unit": unit})
    return ingredients


def format_ingredients_line(ingredients):
    return "|".join(
        f"{ingredient['name']},{ingredient['quantity']},{ingredient['unit']}"
        for ingredient in ingredients
    )


def format_tags_line(tags):
    return ",".join(sorted(tags))


def sanitize_filename(name):
    safe_name = re.sub(r"[^A-Za-z0-9 _-]", "", name).strip()
    return safe_name.replace(" ", "_") or "recipe"


def store_recipe(recipe_name, ingredients, cooking_time, category, tags=None, recipe_id=None):
    global recipe_counter
    if recipe_id is None:
        recipe_id = generate_recipe_id()
    else:
        match = re.match(r"^RCP(\d{3})$", recipe_id)
        if match:
            loaded_number = int(match.group(1))
            recipe_counter = max(recipe_counter, loaded_number)

    if tags is None:
        tags = {"italian", "quick", "comfort-food"}
    recipe_data = {
        "name": recipe_name,
        "ingredients": [
            {"name": item["name"], "quantity": item["quantity"], "unit": item["unit"]}
            for item in ingredients
        ],
        "cooking_time": cooking_time,
        "category": category.upper(),
        "tags": set(tags)
    }
    recipes_storage[recipe_id] = recipe_data
    return recipe_id, recipe_data


def save_recipes_to_file(filename=DEFAULT_RECIPES_FILE):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for recipe_id, recipe_data in recipes_storage.items():
                file.write("===RECIPE===\n")
                file.write(f"ID:{recipe_id}\n")
                file.write(f"NAME:{recipe_data['name']}\n")
                file.write(f"CATEGORY:{recipe_data['category']}\n")
                file.write(f"TIME:{recipe_data['cooking_time']}\n")
                file.write(f"INGREDIENTS:{format_ingredients_line(recipe_data['ingredients'])}\n")
                file.write(f"TAGS:{format_tags_line(recipe_data['tags'])}\n")
                file.write("===END===\n")
        return True
    except OSError as error:
        print(f"Error saving recipes: {error}")
        return False


def load_recipes_from_file(filename=DEFAULT_RECIPES_FILE):
    global recipe_counter
    recipes_storage.clear()
    recipe_counter = 0

    if not os.path.exists(filename):
        print("No saved recipes found. Starting fresh.")
        return 0

    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = [line.rstrip("\n") for line in file]
    except OSError as error:
        print(f"Error reading recipes file: {error}")
        return 0

    if not any(line.strip() for line in lines):
        print("No saved recipes found. Starting fresh.")
        return 0

    current_block = None
    loaded_count = 0

    for raw_line in lines:
        line = raw_line.strip()
        if line == "===RECIPE===":
            if current_block is not None:
                print("Formatting issue detected. Starting with empty recipe list.")
                recipes_storage.clear()
                recipe_counter = 0
                return 0
            current_block = {}
            continue

        if line == "===END===":
            if current_block is None:
                print("Formatting issue detected. Starting with empty recipe list.")
                return 0

            required_fields = {"ID", "NAME", "CATEGORY", "TIME", "INGREDIENTS", "TAGS"}
            if not required_fields.issubset(current_block):
                print("Missing recipe fields in saved file. Starting with empty recipe list.")
                recipes_storage.clear()
                recipe_counter = 0
                return 0

            recipe_id = current_block["ID"].strip()
            recipe_name = current_block["NAME"].strip()
            category_name = current_block["CATEGORY"].strip()
            cooking_time = current_block["TIME"].strip()
            ingredients_text = current_block["INGREDIENTS"].strip()
            tags_text = current_block["TAGS"].strip()

            if not re.match(r"^RCP\d{3}$", recipe_id):
                print("Invalid recipe ID format in saved file. Starting with empty recipe list.")
                recipes_storage.clear()
                recipe_counter = 0
                return 0

            ingredients = parse_ingredients_line(ingredients_text)
            if ingredients is None:
                print("Invalid ingredient format in saved file. Starting with empty recipe list.")
                recipes_storage.clear()
                recipe_counter = 0
                return 0

            if main.category_selection_valid(category_name) != "Category is valid":
                print("Invalid category in saved file. Starting with empty recipe list.")
                recipes_storage.clear()
                recipe_counter = 0
                return 0

            if main.cooking_time_valid(cooking_time) != "Cooking time is valid":
                print("Invalid cooking time in saved file. Starting with empty recipe list.")
                recipes_storage.clear()
                recipe_counter = 0
                return 0

            tags = {tag.strip() for tag in tags_text.split(",") if tag.strip()}
            if recipe_name_exists(recipe_name):
                print("Duplicate recipe name found in saved file. Starting with empty recipe list.")
                recipes_storage.clear()
                recipe_counter = 0
                return 0

            store_recipe(recipe_name, ingredients, cooking_time, category_name, tags=tags, recipe_id=recipe_id)
            loaded_count += 1
            current_block = None
            continue

        if current_block is None:
            continue

        if ":" not in line:
            print("Formatting issue detected in saved file. Starting with empty recipe list.")
            recipes_storage.clear()
            recipe_counter = 0
            return 0

        key, value = line.split(":", 1)
        current_block[key.strip().upper()] = value.strip()

    if current_block is not None:
        print("Formatting issue detected in saved file. Starting with empty recipe list.")
        recipes_storage.clear()
        recipe_counter = 0
        return 0

    if loaded_count == 0:
        print("No saved recipes found. Starting fresh.")
    else:
        print(f"Loaded {loaded_count} recipes successfully")
    return loaded_count


def export_recipe_to_file(recipe_id):
    recipe = recipes_storage.get(recipe_id)
    if recipe is None:
        return False, "Recipe not found"

    filename = f"recipe_{sanitize_filename(recipe['name'])}.txt"
    try:
        with open(filename, "w", encoding="utf-8") as file:
            total_minutes = main.cooking_time_to_minutes(recipe["cooking_time"])
            file.write(f"RECIPE: {recipe['name']}\n")
            file.write("=" * 40 + "\n")
            file.write(f"Category: {recipe['category']}\n")
            file.write(f"Cooking Time: {total_minutes} minutes\n")
            file.write("INGREDIENTS:\n")
            for ingredient in recipe["ingredients"]:
                file.write(f"- {ingredient['name']}: {ingredient['quantity']} {ingredient['unit']}\n")
            file.write(f"TAGS: {format_tags_line(recipe['tags'])}\n")
            file.write("=" * 40 + "\n")
        return True, filename
    except OSError as error:
        return False, str(error)


def get_recipe_by_id(recipe_id):
    return recipes_storage.get(recipe_id)


def find_recipes_by_ingredient(query):
    terms = [term.strip().lower() for term in re.split(r"[;,\s]+", query) if term.strip()]
    if not terms:
        return []

    matches = []
    for recipe_id, recipe_data in recipes_storage.items():
        ingredient_names = [ingredient["name"].lower() for ingredient in recipe_data["ingredients"]]
        if all(any(term in ingredient for ingredient in ingredient_names) for term in terms):
            matches.append((recipe_id, recipe_data))
    return matches


def filter_recipes(category_name=None, min_time=None, max_time=None, min_ingredients=None, max_ingredients=None):
    results = []
    for recipe_id, recipe_data in recipes_storage.items():
        if category_name and recipe_data["category"] != category_name.upper():
            continue

        total_minutes = main.cooking_time_to_minutes(recipe_data["cooking_time"])
        if total_minutes is None:
            continue

        if min_time is not None and total_minutes < min_time:
            continue
        if max_time is not None and total_minutes > max_time:
            continue

        ingredient_count = len(recipe_data["ingredients"])
        if min_ingredients is not None and ingredient_count < min_ingredients:
            continue
        if max_ingredients is not None and ingredient_count > max_ingredients:
            continue

        results.append((recipe_id, recipe_data))
    return results


def update_recipe(recipe_id, name=None, category_name=None, cooking_time=None, ingredients=None, tags=None):
    recipe = recipes_storage.get(recipe_id)
    if recipe is None:
        return False

    if name:
        recipe["name"] = name
    if category_name:
        recipe["category"] = category_name.upper()
    if cooking_time:
        recipe["cooking_time"] = cooking_time
    if ingredients is not None:
        recipe["ingredients"] = ingredients
    if tags is not None:
        recipe["tags"] = set(tags)

    return save_recipes_to_file()


def delete_recipe(recipe_id):
    if recipe_id in recipes_storage:
        del recipes_storage[recipe_id]
        return save_recipes_to_file()
    return False


def duplicate_recipe(original_id, new_name):
    original = recipes_storage.get(original_id)
    if original is None:
        return None
    new_ingredients = [ingredient.copy() for ingredient in original["ingredients"]]
    new_tags = set(original["tags"])
    new_id, _ = store_recipe(new_name, new_ingredients, original["cooking_time"], original["category"], tags=new_tags)
    return new_id


def compute_statistics():
    total_recipes = len(recipes_storage)
    category_counts = {cat: 0 for cat in main.category}
    time_distribution = {"Quick (<30 min)": 0, "Medium (30-60 min)": 0, "Long (>60 min)": 0}
    ingredient_frequency = {}
    ingredient_counts = []

    for recipe_data in recipes_storage.values():
        category_counts[recipe_data["category"]] = category_counts.get(recipe_data["category"], 0) + 1
        minutes = main.cooking_time_to_minutes(recipe_data["cooking_time"])
        if minutes is None:
            continue
        if minutes < 30:
            time_distribution["Quick (<30 min)"] += 1
        elif minutes <= 60:
            time_distribution["Medium (30-60 min)"] += 1
        else:
            time_distribution["Long (>60 min)"] += 1

        ingredient_counts.append(len(recipe_data["ingredients"]))
        for ingredient in recipe_data["ingredients"]:
            name_lower = ingredient["name"].title()
            ingredient_frequency[name_lower] = ingredient_frequency.get(name_lower, 0) + 1

    average_ingredients = round(sum(ingredient_counts) / total_recipes, 1) if total_recipes else 0
    sorted_ingredients = sorted(ingredient_frequency.items(), key=lambda item: item[1], reverse=True)
    top_ingredients = sorted_ingredients[:3]

    largest = None
    smallest = None
    if recipes_storage:
        largest = max(recipes_storage.items(), key=lambda item: len(item[1]["ingredients"]))
        smallest = min(recipes_storage.items(), key=lambda item: len(item[1]["ingredients"]))

    return {
        "total_recipes": total_recipes,
        "category_counts": category_counts,
        "time_distribution": time_distribution,
        "top_ingredients": top_ingredients,
        "average_ingredients": average_ingredients,
        "largest": largest,
        "smallest": smallest,
    }


def display_all_recipes():
    if not recipes_storage:
        print("\nNo recipes stored yet.")
        return

    print("\n" + "=" * 60)
    print(f"ALL STORED RECIPES - Total: {len(recipes_storage)}")
    print("=" * 60)
    for recipe_id, recipe_data in recipes_storage.items():
        print(f"\nRecipe ID: {recipe_id}")
        print(f"   Name: {recipe_data['name']}")
        print(f"   Category: {recipe_data['category']}")
        print(f"   Cooking Time: {recipe_data['cooking_time']}")
        print(f"   Ingredients ({len(recipe_data['ingredients'])}):")
        for ingredient in recipe_data['ingredients']:
            print(f"      • {ingredient['name']}: {ingredient['quantity']} {ingredient['unit']}")
        print(f"   Tags: {format_tags_line(recipe_data['tags'])}")
    print("\n" + "=" * 60)

