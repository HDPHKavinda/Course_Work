import re

units = ["g", "kg", "ml", "l", "cup", "tbsp", "tsp", "piece"]
category = ["BREAKFAST", "LUNCH", "DINNER", "DESSERT", "SNACK", "BEVERAGE"]

def recipe_name_valid(recipe_name):
    if not recipe_name or not recipe_name.strip():
        return "Recipe name cannot be empty or spaces only"
    if len(recipe_name) < 3 or len(recipe_name) > 50:
        return "Recipe name must be between 3 and 50 characters"

    pattern = r"^[A-Za-z:'\- ]+$"
    if not re.match(pattern, recipe_name):
        return "Recipe name contains invalid characters"
    if not re.search(r"[A-Za-z]", recipe_name):
        return "Recipe name must contain at least one letter"
    return "Recipe name is valid"


def ingredient_input(name, quantity, unit, ingredient_list):
    if not name or not name.strip():
        return "Ingredient name cannot be empty"
    if len(name) < 3 or len(name) > 50:
        return "Ingredient name must be between 3 and 50 characters"
    if type(quantity) not in [int, float] or quantity <= 0:
        return "Quantity must be a positive number and integer or float"
    if unit not in units:
        return "Invalid unit. Please use a valid unit."
    if name.lower() in [ingredient["name"].lower() for ingredient in ingredient_list]:
        return "Ingredient already exists in the recipe."

    ingredient_list.append({"name": name, "quantity": quantity, "unit": unit})
    return "Ingredient input is valid"


def cooking_time_valid(cooking_time):
    if not cooking_time or not cooking_time.strip():
        return "Cooking time cannot be empty"
    if not re.match(r"^[0-9]{2}:[0-9]{2}$", cooking_time):
        return "Cooking time must be in HH:MM format"

    hours, minutes = cooking_time.split(":")
    hours = int(hours)
    minutes = int(minutes)

    if hours < 0 or hours > 12:
        return "Hour must be between 00 and 12"
    if minutes < 0 or minutes > 59:
        return "Minute must be between 00 and 59"

    total_minutes = hours * 60 + minutes
    if total_minutes < 5 or total_minutes > 12 * 60:
        return "Cooking time must be between 00:05 and 12:00"
    return "Cooking time is valid"


def cooking_time_to_minutes(cooking_time):
    try:
        hours, minutes = cooking_time.split(":")
        return int(hours) * 60 + int(minutes)
    except (ValueError, AttributeError):
        return None


def category_selection_valid(category_input):
    if category_input.upper() not in category:
        return "Invalid category. Please select a valid category."
    return "Category is valid"


def validate_recipe_input(recipe_name, cooking_time, category, ingredient_count=0):
    name_validation = recipe_name_valid(recipe_name)
    time_validation = cooking_time_valid(cooking_time)
    category_validation = category_selection_valid(category)
    if name_validation != "Recipe name is valid":
        return name_validation
    if time_validation != "Cooking time is valid":
        return time_validation
    if category_validation != "Category is valid":
        return category_validation
    if ingredient_count <= 0:
        return "At least one ingredient is required"
    return f"Recipe validation successfully\n Name: {recipe_name} \n Ingredients: {ingredient_count} \n category: {category} \n cooking time: {cooking_time}"


if __name__ == "__main__":
    print(validate_recipe_input("pancakes", "00:30", "Breakfast", 1))