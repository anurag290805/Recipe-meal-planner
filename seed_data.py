import sqlite3

DB_NAME = "recipes.db"


# ---------------------------------------------------------------------------
# Database connection
# ---------------------------------------------------------------------------

def get_connection() -> sqlite3.Connection:
    """
    Create and return a connection to the SQLite database.

    Enables foreign key constraints and sets row factory to dict-like rows.

    Returns:
        sqlite3.Connection: Open database connection.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ---------------------------------------------------------------------------
# Insert helper
# ---------------------------------------------------------------------------

def insert_recipe_with_ingredients(conn: sqlite3.Connection, recipe: dict) -> None:
    """
    Insert a single recipe and all its ingredients into the database.

    Uses parameterized queries to prevent SQL injection.
    Ingredients are linked to the recipe via the auto-generated recipe_id.

    Args:
        conn:   Open SQLite connection.
        recipe: Dict containing recipe fields and an 'ingredients' list.
    """
    recipe_sql = """
        INSERT INTO recipes (title, description, cuisine, cook_time, servings, tags)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor = conn.execute(recipe_sql, (
        recipe["title"],
        recipe["description"],
        recipe["cuisine"],
        recipe["cook_time"],
        recipe["servings"],
        recipe["tags"],
    ))

    recipe_id = cursor.lastrowid

    ingredient_sql = """
        INSERT INTO ingredients (recipe_id, name, quantity, unit)
        VALUES (?, ?, ?, ?)
    """
    for ing in recipe["ingredients"]:
        conn.execute(ingredient_sql, (
            recipe_id,
            ing["name"],
            ing["quantity"],
            ing["unit"],
        ))


# ---------------------------------------------------------------------------
# Full recipe dataset — 49 recipes
# ---------------------------------------------------------------------------

ALL_RECIPES = [

    # ================================================================ Indian
    {
        "title":       "Butter Chicken",
        "description": "A rich and creamy tomato-based curry with tender chicken. One of India's most beloved dishes.",
        "cuisine":     "Indian",
        "cook_time":   45,
        "servings":    4,
        "tags":        "indian, curry, creamy, non-veg",
        "ingredients": [
            {"name": "chicken breast",  "quantity": 500,  "unit": "g"},
            {"name": "butter",          "quantity": 3,    "unit": "tbsp"},
            {"name": "tomato puree",    "quantity": 200,  "unit": "ml"},
            {"name": "heavy cream",     "quantity": 100,  "unit": "ml"},
            {"name": "garlic cloves",   "quantity": 4,    "unit": "pieces"},
            {"name": "ginger",          "quantity": 10,   "unit": "g"},
            {"name": "garam masala",    "quantity": 2,    "unit": "tsp"},
            {"name": "salt",            "quantity": 1,    "unit": "tsp"},
        ],
    },
    {
        "title":       "Dal Tadka",
        "description": "Comforting yellow lentils tempered with cumin, garlic, and dried red chillies. A staple of Indian home cooking.",
        "cuisine":     "Indian",
        "cook_time":   35,
        "servings":    4,
        "tags":        "indian, vegetarian, lentils, comfort food",
        "ingredients": [
            {"name": "yellow lentils",  "quantity": 1,    "unit": "cups"},
            {"name": "onion",           "quantity": 1,    "unit": "pieces"},
            {"name": "tomato",          "quantity": 2,    "unit": "pieces"},
            {"name": "garlic cloves",   "quantity": 4,    "unit": "pieces"},
            {"name": "cumin seeds",     "quantity": 1,    "unit": "tsp"},
            {"name": "turmeric",        "quantity": 0.5,  "unit": "tsp"},
            {"name": "ghee",            "quantity": 2,    "unit": "tbsp"},
            {"name": "salt",            "quantity": 1,    "unit": "tsp"},
        ],
    },
    {
        "title":       "Palak Paneer",
        "description": "Fresh cottage cheese cubes in a vibrant spiced spinach gravy. A classic vegetarian Indian dish.",
        "cuisine":     "Indian",
        "cook_time":   30,
        "servings":    3,
        "tags":        "indian, vegetarian, paneer, healthy",
        "ingredients": [
            {"name": "paneer",          "quantity": 250,  "unit": "g"},
            {"name": "spinach",         "quantity": 400,  "unit": "g"},
            {"name": "onion",           "quantity": 1,    "unit": "pieces"},
            {"name": "garlic cloves",   "quantity": 3,    "unit": "pieces"},
            {"name": "ginger",          "quantity": 10,   "unit": "g"},
            {"name": "garam masala",    "quantity": 1,    "unit": "tsp"},
            {"name": "cream",           "quantity": 50,   "unit": "ml"},
            {"name": "oil",             "quantity": 2,    "unit": "tbsp"},
        ],
    },
    {
        "title":       "Chicken Biryani",
        "description": "Fragrant long-grain rice layered with spiced chicken, caramelized onions, and saffron. A celebratory one-pot dish.",
        "cuisine":     "Indian",
        "cook_time":   75,
        "servings":    6,
        "tags":        "indian, rice, non-veg, festive",
        "ingredients": [
            {"name": "chicken",         "quantity": 750,  "unit": "g"},
            {"name": "basmati rice",    "quantity": 2,    "unit": "cups"},
            {"name": "onion",           "quantity": 2,    "unit": "pieces"},
            {"name": "yogurt",          "quantity": 0.5,  "unit": "cups"},
            {"name": "biryani masala",  "quantity": 2,    "unit": "tbsp"},
            {"name": "saffron",         "quantity": 0.5,  "unit": "tsp"},
            {"name": "ghee",            "quantity": 3,    "unit": "tbsp"},
            {"name": "mint leaves",     "quantity": 20,   "unit": "g"},
        ],
    },
    {
        "title":       "Aloo Gobi",
        "description": "A dry spiced dish of potatoes and cauliflower cooked with turmeric, cumin, and coriander. A simple weeknight staple.",
        "cuisine":     "Indian",
        "cook_time":   25,
        "servings":    3,
        "tags":        "indian, vegetarian, vegan, dry curry",
        "ingredients": [
            {"name": "potato",          "quantity": 3,    "unit": "pieces"},
            {"name": "cauliflower",     "quantity": 0.5,  "unit": "pieces"},
            {"name": "onion",           "quantity": 1,    "unit": "pieces"},
            {"name": "turmeric",        "quantity": 0.5,  "unit": "tsp"},
            {"name": "cumin seeds",     "quantity": 1,    "unit": "tsp"},
            {"name": "coriander powder","quantity": 1,    "unit": "tsp"},
            {"name": "oil",             "quantity": 2,    "unit": "tbsp"},
            {"name": "salt",            "quantity": 1,    "unit": "tsp"},
        ],
    },
    {
        "title":       "Chole Bhature",
        "description": "Spiced chickpea curry served with deep-fried fluffy bread. A beloved North Indian street food combination.",
        "cuisine":     "Indian",
        "cook_time":   50,
        "servings":    4,
        "tags":        "indian, vegetarian, street food, chickpeas",
        "ingredients": [
            {"name": "chickpeas",       "quantity": 400,  "unit": "g"},
            {"name": "onion",           "quantity": 2,    "unit": "pieces"},
            {"name": "tomato",          "quantity": 2,    "unit": "pieces"},
            {"name": "ginger",          "quantity": 15,   "unit": "g"},
            {"name": "garlic cloves",   "quantity": 4,    "unit": "pieces"},
            {"name": "chole masala",    "quantity": 2,    "unit": "tbsp"},
            {"name": "flour",           "quantity": 2,    "unit": "cups"},
            {"name": "oil",             "quantity": 500,  "unit": "ml"},
        ],
    },
    {
        "title":       "Masoor Dal",
        "description": "Quick red lentil curry cooked with tomatoes and a tempering of mustard seeds and curry leaves.",
        "cuisine":     "Indian",
        "cook_time":   25,
        "servings":    3,
        "tags":        "indian, vegetarian, vegan, lentils, quick",
        "ingredients": [
            {"name": "red lentils",     "quantity": 1,    "unit": "cups"},
            {"name": "tomato",          "quantity": 2,    "unit": "pieces"},
            {"name": "mustard seeds",   "quantity": 1,    "unit": "tsp"},
            {"name": "curry leaves",    "quantity": 10,   "unit": "pieces"},
            {"name": "turmeric",        "quantity": 0.5,  "unit": "tsp"},
            {"name": "oil",             "quantity": 2,    "unit": "tbsp"},
            {"name": "salt",            "quantity": 1,    "unit": "tsp"},
        ],
    },
    {
        "title":       "Masala Omelette",
        "description": "A spiced Indian-style omelette with onion, green chilli, coriander, and tomato. Breakfast in under 10 minutes.",
        "cuisine":     "Indian",
        "cook_time":   10,
        "servings":    1,
        "tags":        "indian, breakfast, eggs, quick, high-protein",
        "ingredients": [
            {"name": "eggs",            "quantity": 3,    "unit": "pieces"},
            {"name": "onion",           "quantity": 0.5,  "unit": "pieces"},
            {"name": "green chilli",    "quantity": 1,    "unit": "pieces"},
            {"name": "tomato",          "quantity": 0.5,  "unit": "pieces"},
            {"name": "fresh coriander", "quantity": 10,   "unit": "g"},
            {"name": "turmeric",        "quantity": 0.25, "unit": "tsp"},
            {"name": "oil",             "quantity": 1,    "unit": "tbsp"},
        ],
    },
    {
        "title":       "Mango Kulfi",
        "description": "A creamy Indian frozen dessert made with condensed milk and fresh mango. Denser and richer than ice cream.",
        "cuisine":     "Indian",
        "cook_time":   15,
        "servings":    6,
        "tags":        "indian, dessert, frozen, sweet, mango",
        "ingredients": [
            {"name": "mango puree",      "quantity": 300, "unit": "ml"},
            {"name": "condensed milk",   "quantity": 200, "unit": "ml"},
            {"name": "heavy cream",      "quantity": 200, "unit": "ml"},
            {"name": "cardamom powder",  "quantity": 0.5, "unit": "tsp"},
            {"name": "pistachios",       "quantity": 30,  "unit": "g"},
        ],
    },
    {
        "title":       "Lentil Soup",
        "description": "A warming and hearty red lentil soup spiced with cumin and turmeric. Nutritious, budget-friendly, and filling.",
        "cuisine":     "Indian",
        "cook_time":   30,
        "servings":    4,
        "tags":        "vegetarian, vegan, soup, healthy, budget",
        "ingredients": [
            {"name": "red lentils",     "quantity": 1,    "unit": "cups"},
            {"name": "onion",           "quantity": 1,    "unit": "pieces"},
            {"name": "tomato",          "quantity": 2,    "unit": "pieces"},
            {"name": "garlic cloves",   "quantity": 3,    "unit": "pieces"},
            {"name": "cumin seeds",     "quantity": 1,    "unit": "tsp"},
            {"name": "turmeric",        "quantity": 0.5,  "unit": "tsp"},
            {"name": "vegetable stock", "quantity": 800,  "unit": "ml"},
        ],
    },

    # =============================================================== Italian
    {
        "title":       "Spaghetti Carbonara",
        "description": "Classic Roman pasta with a silky egg and pecorino sauce, crispy guanciale, and black pepper. No cream involved.",
        "cuisine":     "Italian",
        "cook_time":   25,
        "servings":    2,
        "tags":        "italian, pasta, quick, classic",
        "ingredients": [
            {"name": "spaghetti",       "quantity": 200,  "unit": "g"},
            {"name": "guanciale",       "quantity": 100,  "unit": "g"},
            {"name": "egg yolks",       "quantity": 3,    "unit": "pieces"},
            {"name": "pecorino romano", "quantity": 50,   "unit": "g"},
            {"name": "black pepper",    "quantity": 1,    "unit": "tsp"},
            {"name": "salt",            "quantity": 1,    "unit": "tsp"},
        ],
    },
    {
        "title":       "Margherita Pizza",
        "description": "Thin-crust Neapolitan pizza with San Marzano tomato sauce, fresh mozzarella, and basil. Simple and perfect.",
        "cuisine":     "Italian",
        "cook_time":   30,
        "servings":    2,
        "tags":        "italian, pizza, vegetarian, classic",
        "ingredients": [
            {"name": "pizza dough",      "quantity": 300, "unit": "g"},
            {"name": "tomato sauce",     "quantity": 150, "unit": "ml"},
            {"name": "fresh mozzarella", "quantity": 150, "unit": "g"},
            {"name": "fresh basil",      "quantity": 10,  "unit": "g"},
            {"name": "olive oil",        "quantity": 2,   "unit": "tbsp"},
            {"name": "salt",             "quantity": 0.5, "unit": "tsp"},
        ],
    },
    {
        "title":       "Risotto al Funghi",
        "description": "Creamy Arborio rice slowly cooked with porcini mushrooms, white wine, and parmesan. A true Italian comfort dish.",
        "cuisine":     "Italian",
        "cook_time":   40,
        "servings":    3,
        "tags":        "italian, vegetarian, mushroom, creamy",
        "ingredients": [
            {"name": "arborio rice",     "quantity": 300, "unit": "g"},
            {"name": "porcini mushrooms","quantity": 200, "unit": "g"},
            {"name": "white wine",       "quantity": 100, "unit": "ml"},
            {"name": "parmesan",         "quantity": 50,  "unit": "g"},
            {"name": "butter",           "quantity": 2,   "unit": "tbsp"},
            {"name": "vegetable stock",  "quantity": 1,   "unit": "litres"},
            {"name": "onion",            "quantity": 1,   "unit": "pieces"},
        ],
    },
    {
        "title":       "Pesto Pasta",
        "description": "Al dente pasta tossed in a vibrant homemade basil pesto with pine nuts and parmesan. Ready in under 20 minutes.",
        "cuisine":     "Italian",
        "cook_time":   20,
        "servings":    2,
        "tags":        "italian, pasta, quick, vegetarian",
        "ingredients": [
            {"name": "pasta",           "quantity": 200,  "unit": "g"},
            {"name": "fresh basil",     "quantity": 40,   "unit": "g"},
            {"name": "pine nuts",       "quantity": 30,   "unit": "g"},
            {"name": "parmesan",        "quantity": 40,   "unit": "g"},
            {"name": "garlic cloves",   "quantity": 2,    "unit": "pieces"},
            {"name": "olive oil",       "quantity": 4,    "unit": "tbsp"},
        ],
    },
    {
        "title":       "Caprese Salad",
        "description": "Sliced fresh tomatoes and mozzarella drizzled with olive oil and balsamic glaze. An Italian summer classic.",
        "cuisine":     "Italian",
        "cook_time":   5,
        "servings":    2,
        "tags":        "italian, vegetarian, salad, quick, no-cook",
        "ingredients": [
            {"name": "fresh mozzarella","quantity": 200,  "unit": "g"},
            {"name": "tomato",          "quantity": 3,    "unit": "pieces"},
            {"name": "fresh basil",     "quantity": 15,   "unit": "g"},
            {"name": "olive oil",       "quantity": 3,    "unit": "tbsp"},
            {"name": "balsamic glaze",  "quantity": 2,    "unit": "tbsp"},
            {"name": "salt",            "quantity": 0.5,  "unit": "tsp"},
        ],
    },
    {
        "title":       "Tiramisu",
        "description": "Classic Italian dessert with espresso-soaked ladyfinger biscuits layered with mascarpone cream and dusted with cocoa.",
        "cuisine":     "Italian",
        "cook_time":   30,
        "servings":    6,
        "tags":        "italian, dessert, no-bake, classic",
        "ingredients": [
            {"name": "ladyfinger biscuits","quantity": 200,"unit": "g"},
            {"name": "mascarpone",        "quantity": 250, "unit": "g"},
            {"name": "eggs",              "quantity": 3,   "unit": "pieces"},
            {"name": "sugar",             "quantity": 80,  "unit": "g"},
            {"name": "espresso",          "quantity": 200, "unit": "ml"},
            {"name": "cocoa powder",      "quantity": 2,   "unit": "tbsp"},
        ],
    },
    {
        "title":       "Bruschetta",
        "description": "Toasted baguette slices rubbed with garlic and topped with fresh tomato, basil, and olive oil.",
        "cuisine":     "Italian",
        "cook_time":   10,
        "servings":    4,
        "tags":        "italian, snack, vegetarian, quick, appetizer",
        "ingredients": [
            {"name": "baguette",        "quantity": 1,    "unit": "pieces"},
            {"name": "tomato",          "quantity": 3,    "unit": "pieces"},
            {"name": "garlic cloves",   "quantity": 2,    "unit": "pieces"},
            {"name": "fresh basil",     "quantity": 15,   "unit": "g"},
            {"name": "olive oil",       "quantity": 3,    "unit": "tbsp"},
            {"name": "salt",            "quantity": 0.5,  "unit": "tsp"},
        ],
    },
    {
        "title":       "Vegan Lentil Bolognese",
        "description": "A hearty plant-based ragù made with green lentils, tomatoes, and Italian herbs. Served over spaghetti.",
        "cuisine":     "Italian",
        "cook_time":   40,
        "servings":    4,
        "tags":        "vegan, pasta, lentils, italian, high-protein",
        "ingredients": [
            {"name": "green lentils",   "quantity": 1,    "unit": "cups"},
            {"name": "spaghetti",       "quantity": 300,  "unit": "g"},
            {"name": "tomato puree",    "quantity": 400,  "unit": "ml"},
            {"name": "onion",           "quantity": 1,    "unit": "pieces"},
            {"name": "carrot",          "quantity": 1,    "unit": "pieces"},
            {"name": "garlic cloves",   "quantity": 3,    "unit": "pieces"},
            {"name": "dried oregano",   "quantity": 1,    "unit": "tsp"},
            {"name": "olive oil",       "quantity": 2,    "unit": "tbsp"},
        ],
    },

    # =============================================================== Mexican
    {
        "title":       "Chicken Tacos",
        "description": "Juicy spiced chicken in warm corn tortillas, topped with fresh salsa, avocado, and lime. A weeknight favourite.",
        "cuisine":     "Mexican",
        "cook_time":   25,
        "servings":    4,
        "tags":        "mexican, tacos, non-veg, quick",
        "ingredients": [
            {"name": "chicken thighs",  "quantity": 500,  "unit": "g"},
            {"name": "corn tortillas",  "quantity": 8,    "unit": "pieces"},
            {"name": "avocado",         "quantity": 1,    "unit": "pieces"},
            {"name": "lime",            "quantity": 2,    "unit": "pieces"},
            {"name": "cumin",           "quantity": 1,    "unit": "tsp"},
            {"name": "chilli powder",   "quantity": 1,    "unit": "tsp"},
            {"name": "garlic cloves",   "quantity": 3,    "unit": "pieces"},
        ],
    },
    {
        "title":       "Black Bean Burritos",
        "description": "Hearty flour tortillas stuffed with seasoned black beans, rice, cheese, and sour cream. Great vegetarian option.",
        "cuisine":     "Mexican",
        "cook_time":   20,
        "servings":    4,
        "tags":        "mexican, vegetarian, beans, quick",
        "ingredients": [
            {"name": "black beans",     "quantity": 400,  "unit": "g"},
            {"name": "flour tortillas", "quantity": 4,    "unit": "pieces"},
            {"name": "cooked rice",     "quantity": 1,    "unit": "cups"},
            {"name": "cheddar cheese",  "quantity": 100,  "unit": "g"},
            {"name": "sour cream",      "quantity": 4,    "unit": "tbsp"},
            {"name": "cumin",           "quantity": 1,    "unit": "tsp"},
            {"name": "lime",            "quantity": 1,    "unit": "pieces"},
        ],
    },
    {
        "title":       "Guacamole",
        "description": "Fresh and chunky avocado dip with lime, coriander, and jalapeño. Best made just before serving.",
        "cuisine":     "Mexican",
        "cook_time":   10,
        "servings":    4,
        "tags":        "mexican, vegetarian, dip, quick, vegan",
        "ingredients": [
            {"name": "avocado",         "quantity": 3,    "unit": "pieces"},
            {"name": "lime",            "quantity": 1,    "unit": "pieces"},
            {"name": "red onion",       "quantity": 0.5,  "unit": "pieces"},
            {"name": "coriander",       "quantity": 15,   "unit": "g"},
            {"name": "jalapeño",        "quantity": 1,    "unit": "pieces"},
            {"name": "salt",            "quantity": 0.5,  "unit": "tsp"},
        ],
    },
    {
        "title":       "Quesadillas",
        "description": "Crispy flour tortillas filled with melted cheese and seasoned black beans. Ready in 10 minutes and endlessly customizable.",
        "cuisine":     "Mexican",
        "cook_time":   10,
        "servings":    2,
        "tags":        "mexican, quick, vegetarian, snack",
        "ingredients": [
            {"name": "flour tortillas", "quantity": 4,    "unit": "pieces"},
            {"name": "cheddar cheese",  "quantity": 150,  "unit": "g"},
            {"name": "black beans",     "quantity": 200,  "unit": "g"},
            {"name": "bell pepper",     "quantity": 0.5,  "unit": "pieces"},
            {"name": "sour cream",      "quantity": 2,    "unit": "tbsp"},
            {"name": "oil",             "quantity": 1,    "unit": "tbsp"},
        ],
    },

    # =============================================================== Chinese
    {
        "title":       "Kung Pao Chicken",
        "description": "A spicy stir-fry of diced chicken, peanuts, and dried chillies in a sweet and savoury sauce. A Sichuan classic.",
        "cuisine":     "Chinese",
        "cook_time":   20,
        "servings":    3,
        "tags":        "chinese, stir-fry, spicy, non-veg, quick",
        "ingredients": [
            {"name": "chicken breast",  "quantity": 400,  "unit": "g"},
            {"name": "peanuts",         "quantity": 80,   "unit": "g"},
            {"name": "dried red chilli","quantity": 6,    "unit": "pieces"},
            {"name": "soy sauce",       "quantity": 3,    "unit": "tbsp"},
            {"name": "rice vinegar",    "quantity": 2,    "unit": "tbsp"},
            {"name": "garlic cloves",   "quantity": 3,    "unit": "pieces"},
            {"name": "sesame oil",      "quantity": 1,    "unit": "tbsp"},
        ],
    },
    {
        "title":       "Egg Fried Rice",
        "description": "Classic Chinese takeaway-style fried rice with scrambled eggs, spring onion, and soy sauce. Uses leftover rice perfectly.",
        "cuisine":     "Chinese",
        "cook_time":   15,
        "servings":    2,
        "tags":        "chinese, rice, quick, vegetarian",
        "ingredients": [
            {"name": "cooked rice",     "quantity": 2,    "unit": "cups"},
            {"name": "eggs",            "quantity": 2,    "unit": "pieces"},
            {"name": "spring onion",    "quantity": 3,    "unit": "pieces"},
            {"name": "soy sauce",       "quantity": 2,    "unit": "tbsp"},
            {"name": "sesame oil",      "quantity": 1,    "unit": "tsp"},
            {"name": "vegetable oil",   "quantity": 2,    "unit": "tbsp"},
        ],
    },
    {
        "title":       "Sweet and Sour Pork",
        "description": "Crispy pork pieces tossed in a tangy pineapple and pepper sweet-sour sauce. A crowd-pleasing Chinese favourite.",
        "cuisine":     "Chinese",
        "cook_time":   35,
        "servings":    4,
        "tags":        "chinese, pork, non-veg, takeaway",
        "ingredients": [
            {"name": "pork shoulder",   "quantity": 500,  "unit": "g"},
            {"name": "pineapple chunks","quantity": 200,  "unit": "g"},
            {"name": "bell pepper",     "quantity": 2,    "unit": "pieces"},
            {"name": "tomato ketchup",  "quantity": 3,    "unit": "tbsp"},
            {"name": "rice vinegar",    "quantity": 2,    "unit": "tbsp"},
            {"name": "soy sauce",       "quantity": 2,    "unit": "tbsp"},
            {"name": "cornstarch",      "quantity": 3,    "unit": "tbsp"},
        ],
    },
    {
        "title":       "Vegetable Stir Fry",
        "description": "A colourful mix of crunchy vegetables tossed in a garlicky soy and ginger sauce. Quick, healthy, and satisfying.",
        "cuisine":     "Chinese",
        "cook_time":   15,
        "servings":    2,
        "tags":        "vegetarian, vegan, stir-fry, quick, healthy",
        "ingredients": [
            {"name": "broccoli",        "quantity": 150,  "unit": "g"},
            {"name": "bell pepper",     "quantity": 1,    "unit": "pieces"},
            {"name": "carrot",          "quantity": 1,    "unit": "pieces"},
            {"name": "snap peas",       "quantity": 100,  "unit": "g"},
            {"name": "soy sauce",       "quantity": 3,    "unit": "tbsp"},
            {"name": "garlic cloves",   "quantity": 3,    "unit": "pieces"},
            {"name": "ginger",          "quantity": 10,   "unit": "g"},
        ],
    },
    {
        "title":       "Miso Soup",
        "description": "A simple and restorative Japanese broth with miso paste, tofu, wakame seaweed, and spring onion.",
        "cuisine":     "Chinese",
        "cook_time":   10,
        "servings":    2,
        "tags":        "japanese, soup, vegan, quick, healthy",
        "ingredients": [
            {"name": "miso paste",      "quantity": 3,    "unit": "tbsp"},
            {"name": "tofu",            "quantity": 100,  "unit": "g"},
            {"name": "wakame seaweed",  "quantity": 5,    "unit": "g"},
            {"name": "spring onion",    "quantity": 2,    "unit": "pieces"},
            {"name": "water",           "quantity": 600,  "unit": "ml"},
        ],
    },

    # ================================================================= Thai
    {
        "title":       "Pad Thai",
        "description": "Stir-fried rice noodles with egg, bean sprouts, and peanuts in a tangy tamarind sauce. Thailand's most iconic street food.",
        "cuisine":     "Thai",
        "cook_time":   20,
        "servings":    2,
        "tags":        "thai, noodles, quick, street food",
        "ingredients": [
            {"name": "rice noodles",    "quantity": 200,  "unit": "g"},
            {"name": "eggs",            "quantity": 2,    "unit": "pieces"},
            {"name": "bean sprouts",    "quantity": 100,  "unit": "g"},
            {"name": "spring onion",    "quantity": 3,    "unit": "pieces"},
            {"name": "peanuts",         "quantity": 50,   "unit": "g"},
            {"name": "tamarind paste",  "quantity": 2,    "unit": "tbsp"},
            {"name": "fish sauce",      "quantity": 2,    "unit": "tbsp"},
            {"name": "palm sugar",      "quantity": 1,    "unit": "tbsp"},
        ],
    },
    {
        "title":       "Green Thai Curry",
        "description": "A fragrant and creamy coconut milk curry with green curry paste, vegetables, and jasmine rice.",
        "cuisine":     "Thai",
        "cook_time":   30,
        "servings":    4,
        "tags":        "thai, curry, coconut, vegetarian",
        "ingredients": [
            {"name": "green curry paste","quantity": 3,   "unit": "tbsp"},
            {"name": "coconut milk",    "quantity": 400,  "unit": "ml"},
            {"name": "tofu",            "quantity": 250,  "unit": "g"},
            {"name": "zucchini",        "quantity": 1,    "unit": "pieces"},
            {"name": "bell pepper",     "quantity": 1,    "unit": "pieces"},
            {"name": "fish sauce",      "quantity": 2,    "unit": "tbsp"},
            {"name": "fresh basil",     "quantity": 15,   "unit": "g"},
            {"name": "jasmine rice",    "quantity": 1.5,  "unit": "cups"},
        ],
    },
    {
        "title":       "Tom Yum Soup",
        "description": "A hot and sour Thai broth with lemongrass, kaffir lime leaves, galangal, and prawns. Bold and aromatic.",
        "cuisine":     "Thai",
        "cook_time":   25,
        "servings":    3,
        "tags":        "thai, soup, spicy, seafood",
        "ingredients": [
            {"name": "prawns",           "quantity": 300, "unit": "g"},
            {"name": "lemongrass",       "quantity": 2,   "unit": "pieces"},
            {"name": "kaffir lime leaves","quantity": 4,  "unit": "pieces"},
            {"name": "galangal",         "quantity": 20,  "unit": "g"},
            {"name": "mushrooms",        "quantity": 150, "unit": "g"},
            {"name": "fish sauce",       "quantity": 2,   "unit": "tbsp"},
            {"name": "lime juice",       "quantity": 2,   "unit": "tbsp"},
            {"name": "chilli",           "quantity": 3,   "unit": "pieces"},
        ],
    },

    # =========================================================== Mediterranean
    {
        "title":       "Greek Salad",
        "description": "Classic Horiatiki salad with ripe tomatoes, cucumber, olives, red onion, and a generous slab of feta cheese.",
        "cuisine":     "Mediterranean",
        "cook_time":   10,
        "servings":    2,
        "tags":        "mediterranean, vegetarian, salad, quick, no-cook",
        "ingredients": [
            {"name": "tomato",          "quantity": 3,    "unit": "pieces"},
            {"name": "cucumber",        "quantity": 1,    "unit": "pieces"},
            {"name": "feta cheese",     "quantity": 150,  "unit": "g"},
            {"name": "kalamata olives", "quantity": 80,   "unit": "g"},
            {"name": "red onion",       "quantity": 0.5,  "unit": "pieces"},
            {"name": "olive oil",       "quantity": 3,    "unit": "tbsp"},
            {"name": "dried oregano",   "quantity": 1,    "unit": "tsp"},
        ],
    },
    {
        "title":       "Hummus",
        "description": "Silky smooth blended chickpea dip with tahini, lemon, and garlic. Serve with warm pita or crudités.",
        "cuisine":     "Mediterranean",
        "cook_time":   10,
        "servings":    6,
        "tags":        "mediterranean, vegan, dip, snack, quick",
        "ingredients": [
            {"name": "chickpeas",       "quantity": 400,  "unit": "g"},
            {"name": "tahini",          "quantity": 3,    "unit": "tbsp"},
            {"name": "lemon",           "quantity": 1,    "unit": "pieces"},
            {"name": "garlic cloves",   "quantity": 2,    "unit": "pieces"},
            {"name": "olive oil",       "quantity": 3,    "unit": "tbsp"},
            {"name": "cumin",           "quantity": 0.5,  "unit": "tsp"},
            {"name": "salt",            "quantity": 0.5,  "unit": "tsp"},
        ],
    },
    {
        "title":       "Shakshuka",
        "description": "Eggs poached in a spiced tomato and pepper sauce. A popular Middle Eastern and North African breakfast dish.",
        "cuisine":     "Mediterranean",
        "cook_time":   25,
        "servings":    2,
        "tags":        "mediterranean, vegetarian, breakfast, eggs",
        "ingredients": [
            {"name": "eggs",            "quantity": 4,    "unit": "pieces"},
            {"name": "tomato",          "quantity": 400,  "unit": "g"},
            {"name": "bell pepper",     "quantity": 1,    "unit": "pieces"},
            {"name": "onion",           "quantity": 1,    "unit": "pieces"},
            {"name": "garlic cloves",   "quantity": 3,    "unit": "pieces"},
            {"name": "cumin",           "quantity": 1,    "unit": "tsp"},
            {"name": "paprika",         "quantity": 1,    "unit": "tsp"},
            {"name": "olive oil",       "quantity": 2,    "unit": "tbsp"},
        ],
    },
    {
        "title":       "Falafel",
        "description": "Crispy deep-fried chickpea patties seasoned with herbs and spices. Serve in pita with tahini and salad.",
        "cuisine":     "Mediterranean",
        "cook_time":   30,
        "servings":    4,
        "tags":        "mediterranean, vegan, snack, street food",
        "ingredients": [
            {"name": "dried chickpeas", "quantity": 300,  "unit": "g"},
            {"name": "onion",           "quantity": 1,    "unit": "pieces"},
            {"name": "garlic cloves",   "quantity": 4,    "unit": "pieces"},
            {"name": "fresh parsley",   "quantity": 30,   "unit": "g"},
            {"name": "cumin",           "quantity": 1,    "unit": "tsp"},
            {"name": "coriander powder","quantity": 1,    "unit": "tsp"},
            {"name": "flour",           "quantity": 2,    "unit": "tbsp"},
            {"name": "oil",             "quantity": 500,  "unit": "ml"},
        ],
    },
    {
        "title":       "Vegan Buddha Bowl",
        "description": "A nourishing bowl of roasted sweet potato, quinoa, chickpeas, avocado, and tahini dressing.",
        "cuisine":     "Mediterranean",
        "cook_time":   30,
        "servings":    2,
        "tags":        "vegan, healthy, bowl, high-protein",
        "ingredients": [
            {"name": "quinoa",          "quantity": 0.5,  "unit": "cups"},
            {"name": "sweet potato",    "quantity": 1,    "unit": "pieces"},
            {"name": "chickpeas",       "quantity": 200,  "unit": "g"},
            {"name": "avocado",         "quantity": 1,    "unit": "pieces"},
            {"name": "spinach",         "quantity": 60,   "unit": "g"},
            {"name": "tahini",          "quantity": 2,    "unit": "tbsp"},
            {"name": "lemon",           "quantity": 1,    "unit": "pieces"},
            {"name": "olive oil",       "quantity": 2,    "unit": "tbsp"},
        ],
    },

    # =============================================================== American
    {
        "title":       "Classic Beef Burger",
        "description": "Juicy homemade beef patty in a toasted brioche bun with lettuce, tomato, and melted cheddar. Backyard essential.",
        "cuisine":     "American",
        "cook_time":   20,
        "servings":    4,
        "tags":        "american, beef, grilled, non-veg",
        "ingredients": [
            {"name": "beef mince",      "quantity": 600,  "unit": "g"},
            {"name": "brioche buns",    "quantity": 4,    "unit": "pieces"},
            {"name": "cheddar cheese",  "quantity": 4,    "unit": "pieces"},
            {"name": "lettuce",         "quantity": 4,    "unit": "pieces"},
            {"name": "tomato",          "quantity": 1,    "unit": "pieces"},
            {"name": "salt",            "quantity": 1,    "unit": "tsp"},
            {"name": "black pepper",    "quantity": 0.5,  "unit": "tsp"},
        ],
    },
    {
        "title":       "Mac and Cheese",
        "description": "Ultra-creamy baked macaroni in a three-cheese sauce with a golden breadcrumb topping. The ultimate comfort food.",
        "cuisine":     "American",
        "cook_time":   40,
        "servings":    4,
        "tags":        "american, vegetarian, pasta, comfort food, baked",
        "ingredients": [
            {"name": "macaroni",        "quantity": 300,  "unit": "g"},
            {"name": "cheddar cheese",  "quantity": 200,  "unit": "g"},
            {"name": "gruyere cheese",  "quantity": 100,  "unit": "g"},
            {"name": "milk",            "quantity": 500,  "unit": "ml"},
            {"name": "butter",          "quantity": 3,    "unit": "tbsp"},
            {"name": "flour",           "quantity": 3,    "unit": "tbsp"},
            {"name": "breadcrumbs",     "quantity": 50,   "unit": "g"},
        ],
    },
    {
        "title":       "BBQ Pulled Pork",
        "description": "Slow-cooked pork shoulder rubbed with spices, shredded and smothered in smoky BBQ sauce. Perfect in a bun.",
        "cuisine":     "American",
        "cook_time":   240,
        "servings":    6,
        "tags":        "american, pork, slow-cook, bbq, non-veg",
        "ingredients": [
            {"name": "pork shoulder",   "quantity": 1.5,  "unit": "kg"},
            {"name": "bbq sauce",       "quantity": 200,  "unit": "ml"},
            {"name": "smoked paprika",  "quantity": 2,    "unit": "tsp"},
            {"name": "garlic powder",   "quantity": 1,    "unit": "tsp"},
            {"name": "brown sugar",     "quantity": 2,    "unit": "tbsp"},
            {"name": "salt",            "quantity": 1,    "unit": "tbsp"},
            {"name": "black pepper",    "quantity": 1,    "unit": "tsp"},
        ],
    },
    {
        "title":       "Pancakes",
        "description": "Fluffy American-style breakfast pancakes served with maple syrup and butter. Weekend morning perfection.",
        "cuisine":     "American",
        "cook_time":   20,
        "servings":    4,
        "tags":        "american, breakfast, vegetarian, quick, sweet",
        "ingredients": [
            {"name": "flour",           "quantity": 1.5,  "unit": "cups"},
            {"name": "milk",            "quantity": 1,    "unit": "cups"},
            {"name": "eggs",            "quantity": 2,    "unit": "pieces"},
            {"name": "butter",          "quantity": 2,    "unit": "tbsp"},
            {"name": "baking powder",   "quantity": 2,    "unit": "tsp"},
            {"name": "sugar",           "quantity": 2,    "unit": "tbsp"},
            {"name": "salt",            "quantity": 0.5,  "unit": "tsp"},
        ],
    },
    {
        "title":       "Grilled Salmon with Asparagus",
        "description": "Perfectly grilled salmon fillet with lemon butter and tender asparagus spears. Light, healthy, and elegant.",
        "cuisine":     "American",
        "cook_time":   20,
        "servings":    2,
        "tags":        "high-protein, healthy, seafood, quick, keto",
        "ingredients": [
            {"name": "salmon fillet",   "quantity": 2,    "unit": "pieces"},
            {"name": "asparagus",       "quantity": 200,  "unit": "g"},
            {"name": "butter",          "quantity": 2,    "unit": "tbsp"},
            {"name": "lemon",           "quantity": 1,    "unit": "pieces"},
            {"name": "garlic cloves",   "quantity": 2,    "unit": "pieces"},
            {"name": "olive oil",       "quantity": 1,    "unit": "tbsp"},
            {"name": "salt",            "quantity": 0.5,  "unit": "tsp"},
        ],
    },
    {
        "title":       "Chicken and Quinoa Salad",
        "description": "Grilled chicken breast sliced over quinoa with roasted vegetables and a lemon herb dressing. A meal-prep favourite.",
        "cuisine":     "American",
        "cook_time":   25,
        "servings":    2,
        "tags":        "high-protein, healthy, salad, meal-prep",
        "ingredients": [
            {"name": "chicken breast",  "quantity": 300,  "unit": "g"},
            {"name": "quinoa",          "quantity": 1,    "unit": "cups"},
            {"name": "cherry tomatoes", "quantity": 100,  "unit": "g"},
            {"name": "cucumber",        "quantity": 0.5,  "unit": "pieces"},
            {"name": "lemon",           "quantity": 1,    "unit": "pieces"},
            {"name": "olive oil",       "quantity": 2,    "unit": "tbsp"},
            {"name": "fresh parsley",   "quantity": 15,   "unit": "g"},
        ],
    },
    {
        "title":       "Tuna Stuffed Avocado",
        "description": "Creamy avocado halves filled with seasoned tuna, red onion, and capers. A no-cook high-protein snack or lunch.",
        "cuisine":     "American",
        "cook_time":   5,
        "servings":    2,
        "tags":        "high-protein, quick, no-cook, keto, snack",
        "ingredients": [
            {"name": "avocado",         "quantity": 2,    "unit": "pieces"},
            {"name": "tuna",            "quantity": 200,  "unit": "g"},
            {"name": "red onion",       "quantity": 0.25, "unit": "pieces"},
            {"name": "capers",          "quantity": 1,    "unit": "tbsp"},
            {"name": "lemon juice",     "quantity": 1,    "unit": "tbsp"},
            {"name": "black pepper",    "quantity": 0.5,  "unit": "tsp"},
        ],
    },
    {
        "title":       "Avocado Toast",
        "description": "Toasted sourdough topped with smashed avocado, poached eggs, chilli flakes, and a squeeze of lemon.",
        "cuisine":     "American",
        "cook_time":   10,
        "servings":    2,
        "tags":        "breakfast, vegetarian, quick, healthy",
        "ingredients": [
            {"name": "sourdough bread", "quantity": 2,    "unit": "pieces"},
            {"name": "avocado",         "quantity": 1,    "unit": "pieces"},
            {"name": "eggs",            "quantity": 2,    "unit": "pieces"},
            {"name": "lemon juice",     "quantity": 1,    "unit": "tbsp"},
            {"name": "chilli flakes",   "quantity": 0.5,  "unit": "tsp"},
            {"name": "salt",            "quantity": 0.5,  "unit": "tsp"},
        ],
    },
    {
        "title":       "Overnight Oats",
        "description": "No-cook oats soaked overnight in milk with honey, chia seeds, and topped with fresh berries in the morning.",
        "cuisine":     "American",
        "cook_time":   5,
        "servings":    1,
        "tags":        "breakfast, vegetarian, healthy, no-cook, quick",
        "ingredients": [
            {"name": "rolled oats",     "quantity": 0.5,  "unit": "cups"},
            {"name": "milk",            "quantity": 0.5,  "unit": "cups"},
            {"name": "chia seeds",      "quantity": 1,    "unit": "tbsp"},
            {"name": "honey",           "quantity": 1,    "unit": "tbsp"},
            {"name": "fresh berries",   "quantity": 60,   "unit": "g"},
        ],
    },
    {
        "title":       "Baked Sweet Potato Fries",
        "description": "Crispy oven-baked sweet potato fries seasoned with paprika and garlic powder. A healthier alternative to regular fries.",
        "cuisine":     "American",
        "cook_time":   35,
        "servings":    3,
        "tags":        "vegan, snack, baked, healthy, side",
        "ingredients": [
            {"name": "sweet potato",    "quantity": 3,    "unit": "pieces"},
            {"name": "olive oil",       "quantity": 2,    "unit": "tbsp"},
            {"name": "smoked paprika",  "quantity": 1,    "unit": "tsp"},
            {"name": "garlic powder",   "quantity": 0.5,  "unit": "tsp"},
            {"name": "salt",            "quantity": 1,    "unit": "tsp"},
        ],
    },
    {
        "title":       "Garlic Butter Shrimp",
        "description": "Plump prawns sautéed in a rich garlic butter sauce with lemon and parsley. On the table in 15 minutes.",
        "cuisine":     "American",
        "cook_time":   15,
        "servings":    2,
        "tags":        "seafood, quick, high-protein, keto",
        "ingredients": [
            {"name": "prawns",          "quantity": 300,  "unit": "g"},
            {"name": "butter",          "quantity": 3,    "unit": "tbsp"},
            {"name": "garlic cloves",   "quantity": 4,    "unit": "pieces"},
            {"name": "lemon juice",     "quantity": 2,    "unit": "tbsp"},
            {"name": "fresh parsley",   "quantity": 15,   "unit": "g"},
            {"name": "chilli flakes",   "quantity": 0.5,  "unit": "tsp"},
        ],
    },
    {
        "title":       "Vegetable Omelette",
        "description": "A fluffy three-egg omelette stuffed with sautéed mushrooms, spinach, and melted cheese. Quick and satisfying.",
        "cuisine":     "American",
        "cook_time":   10,
        "servings":    1,
        "tags":        "breakfast, vegetarian, quick, high-protein",
        "ingredients": [
            {"name": "eggs",            "quantity": 3,    "unit": "pieces"},
            {"name": "mushrooms",       "quantity": 80,   "unit": "g"},
            {"name": "spinach",         "quantity": 40,   "unit": "g"},
            {"name": "cheddar cheese",  "quantity": 30,   "unit": "g"},
            {"name": "butter",          "quantity": 1,    "unit": "tbsp"},
            {"name": "salt",            "quantity": 0.5,  "unit": "tsp"},
        ],
    },
    {
        "title":       "Mango Smoothie Bowl",
        "description": "A thick frozen mango and banana smoothie base topped with granola, fresh fruit, and chia seeds.",
        "cuisine":     "American",
        "cook_time":   10,
        "servings":    1,
        "tags":        "vegan, breakfast, healthy, quick, no-cook",
        "ingredients": [
            {"name": "frozen mango",    "quantity": 200,  "unit": "g"},
            {"name": "banana",          "quantity": 1,    "unit": "pieces"},
            {"name": "coconut milk",    "quantity": 100,  "unit": "ml"},
            {"name": "granola",         "quantity": 50,   "unit": "g"},
            {"name": "chia seeds",      "quantity": 1,    "unit": "tbsp"},
            {"name": "fresh berries",   "quantity": 50,   "unit": "g"},
        ],
    },
    {
        "title":       "Chocolate Lava Cake",
        "description": "Warm individual chocolate cakes with a gooey molten centre. An indulgent dessert that looks far harder than it is.",
        "cuisine":     "American",
        "cook_time":   15,
        "servings":    4,
        "tags":        "dessert, chocolate, baked, indulgent",
        "ingredients": [
            {"name": "dark chocolate",  "quantity": 150,  "unit": "g"},
            {"name": "butter",          "quantity": 100,  "unit": "g"},
            {"name": "eggs",            "quantity": 3,    "unit": "pieces"},
            {"name": "sugar",           "quantity": 60,   "unit": "g"},
            {"name": "flour",           "quantity": 30,   "unit": "g"},
            {"name": "cocoa powder",    "quantity": 1,    "unit": "tbsp"},
        ],
    },
    {
        "title":       "Banana Bread",
        "description": "Moist and tender loaf cake made with overripe bananas, brown sugar, and a hint of cinnamon. A classic bake.",
        "cuisine":     "American",
        "cook_time":   60,
        "servings":    8,
        "tags":        "american, dessert, baked, sweet, breakfast",
        "ingredients": [
            {"name": "overripe bananas","quantity": 3,    "unit": "pieces"},
            {"name": "flour",           "quantity": 1.5,  "unit": "cups"},
            {"name": "brown sugar",     "quantity": 0.75, "unit": "cups"},
            {"name": "eggs",            "quantity": 2,    "unit": "pieces"},
            {"name": "butter",          "quantity": 80,   "unit": "g"},
            {"name": "baking soda",     "quantity": 1,    "unit": "tsp"},
            {"name": "cinnamon",        "quantity": 1,    "unit": "tsp"},
        ],
    },
]


# ---------------------------------------------------------------------------
# Seeder
# ---------------------------------------------------------------------------

def seed_recipes() -> None:
    """
    Seed the database with all recipes, skipping any that already exist.

    Checks each recipe by title before inserting to prevent duplicates.
    Safe to run multiple times. Prints a summary on completion.
    """
    conn = get_connection()

    try:
        # Fetch all existing titles for duplicate checking
        existing_titles = {
            row[0].lower()
            for row in conn.execute("SELECT title FROM recipes").fetchall()
        }

        added_count = 0

        for recipe in ALL_RECIPES:
            if recipe["title"].lower() in existing_titles:
                continue  # skip — already in database

            insert_recipe_with_ingredients(conn, recipe)
            existing_titles.add(recipe["title"].lower())
            added_count += 1

        conn.commit()

        if added_count > 0:
            print(f"Database seeded with {added_count} new recipes.")
        else:
            print("Database is already fully seeded. Nothing new added.")

    except Exception as e:
        conn.rollback()
        print(f"Seeding failed: {e}")
        raise

    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    seed_recipes()