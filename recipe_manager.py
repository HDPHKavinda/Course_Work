import main
import storage_display


def prompt_nonempty_text(prompt_text):
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("Please enter a value.")


def prompt_recipe_name(existing_id=None):
    while True:
        recipe_name = prompt_nonempty_text("Enter recipe name: ")
        name_validation = main.recipe_name_valid(recipe_name)
        if name_validation != "Recipe name is valid":
            print(name_validation)
            continue
        if storage_display.recipe_name_exists(recipe_name, exclude_id=existing_id):
            print("Recipe name already exists. Please choose a different name.")
            continue
        return recipe_name


def prompt_cooking_time():
    while True:
        cooking_time = prompt_nonempty_text("Enter cooking time (HH:MM): ")
        time_validation = main.cooking_time_valid(cooking_time)
        if time_validation != "Cooking time is valid":
            print(time_validation)
            continue
        return cooking_time


def prompt_category():
    print("Available categories:", ", ".join(main.category))
    while True:
        category = prompt_nonempty_text("Enter category: ")
        category_validation = main.category_selection_valid(category)
        if category_validation != "Category is valid":
            print(category_validation)
            continue
        return category.upper()


def prompt_ingredients():
    ingredients = []
    print("Enter ingredients. Type 'done' when finished.")
    while True:
        ingredient_name = input("  Ingredient name (or 'done'): ").strip()
        if ingredient_name.lower() == "done":
            if not ingredients:
                print("Please add at least one ingredient.")
                continue
            break
        if not ingredient_name:
            print("Ingredient name cannot be empty.")
            continue

        try:
            quantity_input = input(f"  Quantity for {ingredient_name}: ").strip()
            quantity = float(quantity_input)
        except ValueError:
            print("Quantity must be a number.")
            continue

        unit = input("  Unit (g, kg, ml, l, cup, tbsp, tsp, piece): ").strip()
        ingredient_validation = main.ingredient_input(ingredient_name, quantity, unit, ingredients)
        if ingredient_validation != "Ingredient input is valid":
            print(ingredient_validation)
        else:
            print(f"{ingredient_name} added successfully")
    return ingredients


def prompt_tags():
    raw_tags = input("Enter tags separated by commas (or blank for default tags): ").strip()
    if not raw_tags:
        return {"italian", "quick", "comfort-food"}
    return {tag.strip().lower() for tag in raw_tags.split(",") if tag.strip()}


def display_recipe_details(recipe_id, recipe_data):
    print("\n" + "=" * 40)
    print(f"Recipe ID: {recipe_id}")
    print(f"Name: {recipe_data['name']}")
    print(f"Category: {recipe_data['category']}")
    print(f"Cooking Time: {recipe_data['cooking_time']}")
    print(f"Tags: {', '.join(sorted(recipe_data['tags']))}")
    print("Ingredients:")
    for ingredient in recipe_data['ingredients']:
        print(f"  - {ingredient['name']}: {ingredient['quantity']} {ingredient['unit']}")
    print("=" * 40)


def parse_time_input(value):
    if not value:
        return None
    value = value.strip()
    if value.isdigit():
        return int(value)
    minutes = main.cooking_time_to_minutes(value)
    if minutes is None:
        raise ValueError("Time must be minutes or HH:MM format")
    return minutes


def add_new_recipe():
    recipe_name = prompt_recipe_name()
    cooking_time = prompt_cooking_time()
    category = prompt_category()
    ingredients = prompt_ingredients()
    tags = prompt_tags()

    recipe_id, _ = storage_display.store_recipe(recipe_name, ingredients, cooking_time, category, tags=tags)
    print(f"\nRecipe added with ID {recipe_id}.")
    print("Auto-saving recipes...")
    if storage_display.save_recipes_to_file():
        print("All recipes saved successfully.")
    else:
        print("Failed to save recipes.")


def view_recipe_by_id():
    recipe_id = prompt_nonempty_text("Enter recipe ID: ").upper()
    recipe_data = storage_display.get_recipe_by_id(recipe_id)
    if not recipe_data:
        print("Recipe not found.")
        return
    display_recipe_details(recipe_id, recipe_data)


def search_by_ingredient():
    query = prompt_nonempty_text("Enter ingredient name or names (comma-separated): ")
    matches = storage_display.find_recipes_by_ingredient(query)
    if not matches:
        print(f"No recipes found containing '{query}'.")
        return

    print(f"Found {len(matches)} recipes containing '{query}':")
    print("-" * 40)
    for recipe_id, recipe_data in matches:
        print(f"{recipe_id} | {recipe_data['name']} | {recipe_data['category']}")


def filter_recipes_menu():
    print("Enter filter values or press Enter to skip a filter.")
    category_name = input("Category: ").strip().upper()
    if category_name and main.category_selection_valid(category_name) != "Category is valid":
        print("Invalid category. Filter will ignore category.")
        category_name = None

    try:
        min_time = parse_time_input(input("Minimum cooking time (minutes or HH:MM): "))
        max_time = parse_time_input(input("Maximum cooking time (minutes or HH:MM): "))
    except ValueError as error:
        print(error)
        return

    try:
        min_ingredients_raw = input("Minimum ingredient count: ").strip()
        max_ingredients_raw = input("Maximum ingredient count: ").strip()
        min_ingredients = int(min_ingredients_raw) if min_ingredients_raw else None
        max_ingredients = int(max_ingredients_raw) if max_ingredients_raw else None
    except ValueError:
        print("Ingredient counts must be whole numbers.")
        return

    matches = storage_display.filter_recipes(
        category_name=category_name or None,
        min_time=min_time,
        max_time=max_time,
        min_ingredients=min_ingredients,
        max_ingredients=max_ingredients,
    )
    if not matches:
        print("No recipes match the selected filters.")
        return

    print(f"Found {len(matches)} recipes matching filters:")
    print("-" * 40)
    for recipe_id, recipe_data in matches:
        print(f"{recipe_id} | {recipe_data['name']} | {recipe_data['category']} | {recipe_data['cooking_time']} | Ingredients: {len(recipe_data['ingredients'])}")


def edit_recipe_menu():
    recipe_id = prompt_nonempty_text("Enter recipe ID to edit: ").upper()
    recipe_data = storage_display.get_recipe_by_id(recipe_id)
    if not recipe_data:
        print("Recipe not found.")
        return

    while True:
        print("\nChoose field to edit:")
        print("1. Name")
        print("2. Category")
        print("3. Cooking Time")
        print("4. Ingredients")
        print("5. Tags")
        print("6. Return to menu")
        choice = input("Choice: ").strip()
        if choice == "1":
            new_name = prompt_recipe_name(existing_id=recipe_id)
            storage_display.update_recipe(recipe_id, name=new_name)
            print("Recipe name updated.")
        elif choice == "2":
            new_category = prompt_category()
            storage_display.update_recipe(recipe_id, category_name=new_category)
            print("Recipe category updated.")
        elif choice == "3":
            new_time = prompt_cooking_time()
            storage_display.update_recipe(recipe_id, cooking_time=new_time)
            print("Recipe cooking time updated.")
        elif choice == "4":
            modify_ingredients = recipe_data["ingredients"].copy()
            while True:
                print("\nCurrent ingredients:")
                for ingredient in modify_ingredients:
                    print(f" - {ingredient['name']}: {ingredient['quantity']} {ingredient['unit']}")
                print("a. Add ingredient")
                print("r. Remove ingredient")
                print("d. Done")
                action = input("Choice: ").strip().lower()
                if action == "a":
                    ingredient_name = prompt_nonempty_text("  Ingredient name: ")
                    try:
                        quantity = float(input("  Quantity: ").strip())
                    except ValueError:
                        print("Quantity must be a number.")
                        continue
                    unit = input("  Unit: ").strip()
                    result = main.ingredient_input(ingredient_name, quantity, unit, modify_ingredients)
                    if result != "Ingredient input is valid":
                        print(result)
                    else:
                        print("Ingredient added.")
                elif action == "r":
                    remove_name = prompt_nonempty_text("  Ingredient name to remove: ")
                    filter_list = [ing for ing in modify_ingredients if ing["name"].lower() != remove_name.lower()]
                    if len(filter_list) == len(modify_ingredients):
                        print("Ingredient not found.")
                    else:
                        modify_ingredients = filter_list
                        print("Ingredient removed.")
                elif action == "d":
                    if not modify_ingredients:
                        print("At least one ingredient is required.")
                        continue
                    storage_display.update_recipe(recipe_id, ingredients=modify_ingredients)
                    print("Ingredients updated.")
                    break
                else:
                    print("Invalid choice.")
        elif choice == "5":
            new_tags = prompt_tags()
            storage_display.update_recipe(recipe_id, tags=new_tags)
            print("Tags updated.")
        elif choice == "6":
            break
        else:
            print("Invalid choice.")


def delete_recipe_menu():
    recipe_id = prompt_nonempty_text("Enter recipe ID to delete: ").upper()
    recipe_data = storage_display.get_recipe_by_id(recipe_id)
    if not recipe_data:
        print("Recipe not found.")
        return

    confirm = input(f"Are you sure you want to delete {recipe_id} ({recipe_data['name']})? (yes/no): ").strip().lower()
    if confirm in ["yes", "y"]:
        if storage_display.delete_recipe(recipe_id):
            print(f"Recipe {recipe_id} deleted successfully.")
        else:
            print("Failed to delete recipe.")
    else:
        print("Deletion cancelled.")


def duplicate_recipe_menu():
    source_id = prompt_nonempty_text("Enter recipe ID to duplicate: ").upper()
    if not storage_display.get_recipe_by_id(source_id):
        print("Recipe not found.")
        return
    new_name = prompt_recipe_name()
    new_id = storage_display.duplicate_recipe(source_id, new_name)
    if new_id:
        storage_display.save_recipes_to_file()
        print(f"Recipe duplicated as {new_id}.")
    else:
        print("Failed to duplicate recipe.")


def display_statistics():
    stats = storage_display.compute_statistics()
    print("\n" + "=" * 40)
    print("RECIPE BOOK SUMMARY")
    print("=" * 40)
    print(f"Total Recipes: {stats['total_recipes']}")
    print("Recipes by Category:")
    for category_name, count in stats["category_counts"].items():
        print(f"  {category_name}: {count}")
    print("Cooking Time Distribution:")
    for label, count in stats["time_distribution"].items():
        print(f"  {label}: {count} recipes")
    print("Most Used Ingredients:")
    if stats["top_ingredients"]:
        for rank, (ingredient, count) in enumerate(stats["top_ingredients"], start=1):
            print(f"  {rank}. {ingredient} - appears in {count} recipes")
    else:
        print("  No ingredients tracked yet.")
    print(f"Average Ingredients per Recipe: {stats['average_ingredients']}")
    if stats["largest"]:
        print(f"Largest Recipe: {stats['largest'][0]} with {len(stats['largest'][1]['ingredients'])} ingredients")
    if stats["smallest"]:
        print(f"Smallest Recipe: {stats['smallest'][0]} with {len(stats['smallest'][1]['ingredients'])} ingredients")
    print("=" * 40)


def save_recipes_menu():
    if storage_display.save_recipes_to_file():
        print("Recipes saved successfully to recipes.txt")
    else:
        print("Could not save recipes. Please try again.")


def load_recipes_menu():
    count = storage_display.load_recipes_from_file()
    if count:
        print(f"Loaded {count} recipes successfully.")


def export_recipe_menu():
    recipe_id = prompt_nonempty_text("Enter recipe ID to export: ").upper()
    success, result = storage_display.export_recipe_to_file(recipe_id)
    if success:
        print(f"Recipe exported to {result}")
    else:
        print(f"Export failed: {result}")


def display_menu():
    print("\n" + "=" * 40)
    print("DIGITAL RECIPE BOOK MANAGER")
    print("=" * 40)
    print("1. Add New Recipe")
    print("2. View All Recipes")
    print("3. View Recipe by ID")
    print("4. Search by Ingredient")
    print("5. Filter Recipes")
    print("6. Edit Recipe")
    print("7. Delete Recipe")
    print("8. Duplicate Recipe")
    print("9. View Statistics")
    print("10. Save Recipes")
    print("11. Load from File")
    print("12. Export Recipe")
    print("13. Exit")
    print("=" * 40)


def main():
    print("Welcome to the Digital Recipe Book Manager")
    storage_display.load_recipes_from_file()

    while True:
        display_menu()
        choice = input("Enter your choice (1-13): ").strip()
        if choice == "1":
            add_new_recipe()
        elif choice == "2":
            storage_display.display_all_recipes()
        elif choice == "3":
            view_recipe_by_id()
        elif choice == "4":
            search_by_ingredient()
        elif choice == "5":
            filter_recipes_menu()
        elif choice == "6":
            edit_recipe_menu()
        elif choice == "7":
            delete_recipe_menu()
        elif choice == "8":
            duplicate_recipe_menu()
        elif choice == "9":
            display_statistics()
        elif choice == "10":
            save_recipes_menu()
        elif choice == "11":
            load_recipes_menu()
        elif choice == "12":
            export_recipe_menu()
        elif choice == "13":
            print("Saving recipes before exit...")
            storage_display.save_recipes_to_file()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 13.")


if __name__ == "__main__":
    main()