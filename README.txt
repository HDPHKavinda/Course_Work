DIGITAL RECIPE BOOK MANAGER
===========================

COURSEWORK SUBMISSION
Student UOW ID: [Your Student ID Here]
Python Version: 3.13.12

DESCRIPTION
-----------
This is a complete Digital Recipe Book Manager implemented in Python. The program allows users to add, view, search, filter, edit, delete, and export recipes. All data persists between program runs using a structured text file format.

FILES INCLUDED
--------------
- main.py: Core validation functions for recipe input
- storage_display.py: Recipe storage, persistence, search, and advanced features
- recipe_manager.py: Main menu-driven interface
- recipes.txt: Sample recipe data file (5 recipes included)
- recipe_Pasta_Carbonara.txt: Sample exported recipe file

HOW TO RUN THE PROGRAM
----------------------
1. Ensure Python 3.13 or later is installed
2. Open a terminal/command prompt
3. Navigate to the Course_Work directory
4. Run: python recipe_manager.py

The program will automatically load any existing recipes from recipes.txt on startup.

MAIN FEATURES IMPLEMENTED
-------------------------

TASK 1 - Input Validation (25%)
- Recipe name validation (3-50 chars, letters/spaces/hyphens/apostrophes only)
- Cooking time validation (HH:MM format, 00:05 to 12:00)
- Category validation (BREAKFAST, LUNCH, DINNER, DESSERT, SNACK, BEVERAGE)
- Ingredient validation (name, quantity, unit)
- Duplicate ingredient prevention within recipes
- Duplicate recipe name prevention across all recipes

TASK 2 - Recipe Management (25%)
- Add at least 3 recipes with user prompts
- Auto-generated unique IDs (RCP001, RCP002, etc.)
- Store recipes in memory with persistence
- Display all recipes with full details
- Ask "Add another recipe? (yes/no)" after each recipe

TASK 3 - File Management & Persistence (25%)
- Save all recipes to recipes.txt in structured format
- Load recipes from recipes.txt on program startup
- Auto-save after every recipe addition
- Export individual recipes to recipe_<name>.txt files
- Robust error handling for file operations
- Validation of loaded data format

TASK 4 - Search & Advanced Features (35%)
- Ingredient-based search (case-insensitive, multi-term AND search)
- Advanced filtering by category, cooking time range, ingredient count
- Edit existing recipes (name, category, time, ingredients, tags)
- Delete recipes with confirmation
- Duplicate recipes with new IDs
- Comprehensive recipe book statistics
- User-friendly menu system with input validation

MENU OPTIONS
------------
1. Add New Recipe - Interactive recipe creation with validation
2. View All Recipes - Display all stored recipes
3. View Recipe by ID - Show specific recipe details
4. Search by Ingredient - Find recipes containing specific ingredients
5. Filter Recipes - Advanced filtering by multiple criteria
6. Edit Recipe - Modify existing recipe fields
7. Delete Recipe - Remove recipe with confirmation
8. Duplicate Recipe - Create copy with new ID
9. View Statistics - Recipe book summary and analytics
10. Save Recipes - Manual save to file
11. Load from File - Reload recipes from disk
12. Export Recipe - Export single recipe to text file
13. Exit - Save and quit program

SAMPLE RECIPES INCLUDED
-----------------------
- Pasta Carbonara (LUNCH, 30 min)
- Banana Pancakes (BREAKFAST, 25 min)
- Chicken Curry (DINNER, 60 min)
- Greek Salad (LUNCH, 15 min)
- Chocolate Brownies (DESSERT, 45 min)

PROGRAM FLOW
------------
1. Program starts and loads existing recipes
2. Displays welcome message and main menu
3. User selects menu option
4. Program executes chosen function
5. Returns to menu (except Exit)
6. On Exit, automatically saves all recipes

ERROR HANDLING
--------------
- Invalid menu choices
- Empty or invalid input fields
- File read/write errors
- Duplicate recipe names
- Invalid recipe data in saved files
- Missing or corrupted recipe files

TECHNICAL DETAILS
-----------------
- Modular design with separate validation, storage, and UI modules
- Data persistence using structured text file format
- Case-insensitive search and filtering
- Input validation throughout the application
- Graceful error handling and user feedback
- No external dependencies required

KNOWN LIMITATIONS
-----------------
- Recipe IDs are auto-generated and cannot be reused
- File format is custom text-based (not JSON/XML)
- No graphical user interface
- All data stored in memory during runtime
- No backup/undo functionality

This implementation meets all coursework requirements for Tasks 1-4 with robust error handling, comprehensive features, and clean code organization.