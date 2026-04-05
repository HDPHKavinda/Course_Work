import main

#counter
recipe_counter = 0
recipes_storage = {}

def generate_recipe_id():
    global recipe_counter    #to update real value of recipe_counter 
    recipe_counter += 1
    recipe_id = f"RCP{recipe_counter:03d}"  # Format: RCP + 3 digit number
    return recipe_id

#Data structure design
def store_recipe(recipe_name, ingredients, cooking_time, category):
    recipe_id = generate_recipe_id()
    
    recipe = {
        recipe_id: {
            "name": recipe_name,
            "ingredients": [(ingredient["name"], ingredient["quantity"], ingredient["unit"]) for ingredient in main.recipe_ingredients],
            "cooking_time": cooking_time,
            "category": category,
            "tags": {"italian", "quick", "comfort-food"}
        }
    }
    
    # Store in global storage to prevent duplicates
    recipes_storage.update(recipe)
    return recipe_id, recipe

#Multiple recipe entry with user prompt
def add_multiple_recipes():
    total_recipes_added = 0
    min_recipes = 3
    
    print("\n" + "="*60)
    print("RECIPE MANAGEMENT SYSTEM - Add Multiple Recipes")
    print("="*60)
    
    while True:
        print(f"\n--- Recipe #{total_recipes_added + 1} ---")
        # Get recipe input from user
        recipe_name = input("Enter recipe name: ").strip()
        # Validate recipe name using main module validation
        name_validation = main.recipe_name_valid(recipe_name)
        if name_validation != "Recipe name is valid":
            print(f"{name_validation}")
            continue
        
        # Get cooking time
        cooking_time = input("Enter cooking time (HH:MM format): ").strip()
        
        # Validate cooking time using main module validation
        time_validation = main.cooking_time_valid(cooking_time)
        if time_validation != "Cooking time is valid":
            print(f"{time_validation}")
            continue
        
        # Get category
        print("Available categories:", ", ".join(main.category))
        category = input("Enter category: ").strip()
        
        # Validate category using main module validation
        category_validation = main.category_selection_valid(category)
        if category_validation != "Category is valid":
            print(f"{category_validation}")
            continue
        
        # Clear previous ingredients list
        main.recipe_ingredients = []
        
        # Get ingredients
        print("Enter ingredients (type 'done' when finished):")
        while True:
            ingredient_name = input("  Ingredient name (or 'done'): ").strip()
            if ingredient_name.lower() == 'done':
                if len(main.recipe_ingredients) == 0:
                    print("Please add at least one ingredient.")
                    continue
                break
            
            try:
                quantity = float(input(f"  Quantity for {ingredient_name}: "))
                unit = input(f"  Unit (g, kg, ml, l, cup, tbsp, tsp, piece): ").strip()
                
                ingredient_validation = main.ingredient_input(ingredient_name, quantity, unit)
                if ingredient_validation != "Ingredient input is valid":
                    print(f"{ingredient_validation}")
                else:
                    print(f"{ingredient_name} added successfully")
            except ValueError:
                print("Quantity must be a number")
        
        # Store recipe
        recipe_id, recipe = store_recipe(recipe_name, main.recipe_ingredients, cooking_time, category)
        total_recipes_added += 1
        
        print(f"\n✓ Recipe stored successfully!")
        print(f"  Recipe ID: {recipe_id}")
        print(f"  Name: {recipe_name}")
        print(f"  Category: {category}")
        print(f"  Cooking Time: {cooking_time}")
        print(f"  Ingredients: {len(main.recipe_ingredients)}")
        print(f"  Total Recipes Added: {total_recipes_added}")
        
        # Ask if user wants to add another recipe
        if total_recipes_added >= min_recipes:
            while True:
                add_another = input(f"\nAdd another recipe? (yes/no): ").strip().lower()
                if add_another in ['yes', 'y']:
                    break
                elif add_another in ['no', 'n']:
                    print("\n" + "="*60)
                    print(f"SUMMARY: Total recipes added: {total_recipes_added}")
                    print("All recipes stored successfully!")
                    print("="*60)
                    display_all_recipes()
                    return total_recipes_added
                else:
                    print("Please enter 'yes' or 'no'")
        else:
            print(f"\nYou need to add at least {min_recipes - total_recipes_added} more recipe(s).")

#Display all stored recipes
def display_all_recipes():
    if not recipes_storage:
        print("\nNo recipes stored yet.")
        return
    
    print("\n" + "="*60)
    print(f"ALL STORED RECIPES - Total: {len(recipes_storage)}")
    print("="*60)
    
    for recipe_id, recipe_data in recipes_storage.items():
        print(f"\nRecipe ID: {recipe_id}")
        print(f"   Name: {recipe_data['name']}")
        print(f"   Category: {recipe_data['category']}")
        print(f"   Cooking Time: {recipe_data['cooking_time']}")
        print(f"   Ingredients ({len(recipe_data['ingredients'])}):")
        for ingredient in recipe_data['ingredients']:
            print(f"      • {ingredient[0]}: {ingredient[1]} {ingredient[2]}")
    print("\n" + "="*60)
