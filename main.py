#Task_1
import re  # is use
#Recipe name validation
def recipe_name_valid(recipe_name):
    if not recipe_name or not recipe_name.strip():   #none or space only
        return "Recipe name cannot be empty or spaces only"
    if len(recipe_name) < 3 or len(recipe_name) > 50:        
        return "Recipe name must be between 3 and 50 characters"

    pattern = r"^[A-Za-z:'\- ]+$"             #pattern allows letters, spaces, apostrophes, and hyphens
    if not re.match(pattern, recipe_name):
        return "Recipe name contains invalid characters"
    if not re.search(r"[A-Za-z]", recipe_name):
        return "Recipe name must contain at least one letter"
    return "Recipe name is valid"

#Ingredient input
units = ["g", "kg", "ml", "l", "cup", "tbsp", "tsp", "piece"]
recipe_ingredients = []
def ingredient_input(name,quantity,unit):
    if len(name) < 3 or len(name) > 50:
        return "Ingredient name must be between 3 and 50 characters"
    if type(quantity) not in [int, float] or quantity <= 0:
        return "Quantity must be a positive number and integer or float"
    if unit not in units:
        return "Invalid unit. Please use a valid unit."
    if name in [ingredient["name"] for ingredient in recipe_ingredients]:  #one line "for" to check if ingredient already in there
        return "Ingredient already exists in the recipe."
    return "Ingredient input is valid" and recipe_ingredients.append({"name": name, "quantity": quantity, "unit": unit})

#Cooking time validation
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
    #wanna canculate cooking time  
    total_minutes = hours * 60 + minutes
    min_allowed = 0 * 60 + 5
    max_allowed = 12 * 60 + 0
    if total_minutes < min_allowed or total_minutes > max_allowed:
        return "Cooking time must be between 00:05 and 12:00"
    return "Cooking time is valid"

#category selection
category = ["BREAKFAST", "LUNCH", "DINNER", "DESSERT", "SNACK", "BEVERAGE"]
def category_selection_valid(category_input):
    if category_input.upper() not in category:
        return "Invalid category. Please select a valid category."
    return "Category is valid"

def validate_recipe_input (recipe_name, cooking_time, category):
    name_validation = recipe_name_valid(recipe_name)
    time_validation = cooking_time_valid(cooking_time)
    category_validation = category_selection_valid(category)
    if name_validation != "Recipe name is valid":
        return name_validation
    if time_validation != "Cooking time is valid":
        return time_validation
    if category_validation != "Category is valid":
        return category_validation
    return f"Recipe validation successfully\n Name: {recipe_name} \n Ingredients: {len(recipe_ingredients)} \n category: {category} \n cooking time: {cooking_time}"



print(validate_recipe_input("pankates","00:30","Breakfast"))