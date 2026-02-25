import sqlite3
from typing import Optional

DB_NAME = "recipes.db"


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

def get_connection() -> sqlite3.Connection:
    """
    Create and return a connection to the SQLite database.

    Enables:
        - Row factory so all results are returned as dictionaries.
        - Foreign key constraint enforcement.

    Returns:
        sqlite3.Connection: An open database connection.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables() -> None:
    """
    Create all required tables if they do not already exist.

    Tables created:
        - recipes      (now includes `instructions` column)
        - ingredients  (CASCADE delete on recipe removal)
        - meal_plan

    Also runs a safe migration: if the database already exists without
    the `instructions` column, ALTER TABLE adds it without touching any
    existing data. Safe to call multiple times.
    """
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS recipes (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                title        TEXT    NOT NULL,
                description  TEXT,
                cuisine      TEXT,
                cook_time    INTEGER,
                servings     INTEGER,
                tags         TEXT,
                instructions TEXT
            );

            CREATE TABLE IF NOT EXISTS ingredients (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id   INTEGER NOT NULL,
                name        TEXT    NOT NULL,
                quantity    REAL,
                unit        TEXT,
                FOREIGN KEY (recipe_id)
                    REFERENCES recipes (id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS meal_plan (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                week_start  TEXT    NOT NULL,
                day         TEXT    NOT NULL,
                meal_type   TEXT    NOT NULL,
                recipe_id   INTEGER,
                FOREIGN KEY (recipe_id)
                    REFERENCES recipes (id)
            );
        """)

        # ── Migration: add `instructions` to existing databases ────────────
        # PRAGMA table_info returns one row per column. We check whether
        # `instructions` is already present before attempting ALTER TABLE,
        # because SQLite does not support IF NOT EXISTS on ADD COLUMN.
        existing_columns = {
            row[1] for row in conn.execute("PRAGMA table_info(recipes)").fetchall()
        }
        if "instructions" not in existing_columns:
            conn.execute("ALTER TABLE recipes ADD COLUMN instructions TEXT")


# ---------------------------------------------------------------------------
# Recipe functions
# ---------------------------------------------------------------------------

def add_recipe(
    title: str,
    description: str,
    cuisine: str,
    cook_time: int,
    servings: int,
    tags: str,
    instructions: str = "",
) -> int:
    """
    Insert a new recipe into the database.

    Args:
        title:        Name of the recipe (required).
        description:  Short description of the dish.
        cuisine:      Cuisine type e.g. 'Italian', 'Indian'.
        cook_time:    Cooking time in minutes.
        servings:     Number of servings the recipe produces.
        tags:         Comma-separated tags e.g. 'vegan, quick, healthy'.
        instructions: Step-by-step cooking method (one step per line).

    Returns:
        int: The auto-generated id of the newly inserted recipe.
    """
    sql = """
        INSERT INTO recipes (title, description, cuisine, cook_time, servings, tags, instructions)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    with get_connection() as conn:
        cursor = conn.execute(sql, (title, description, cuisine, cook_time, servings, tags, instructions))
        return cursor.lastrowid


def update_recipe(
    recipe_id: int,
    title: str,
    description: str,
    cuisine: str,
    cook_time: int,
    servings: int,
    tags: str,
    instructions: str = "",
) -> None:
    """
    Update an existing recipe's details by id.

    Args:
        recipe_id:    The id of the recipe to update.
        title:        Updated recipe name.
        description:  Updated description.
        cuisine:      Updated cuisine type.
        cook_time:    Updated cook time in minutes.
        servings:     Updated number of servings.
        tags:         Updated comma-separated tags.
        instructions: Updated step-by-step cooking method.
    """
    sql = """
        UPDATE recipes
        SET title        = ?,
            description  = ?,
            cuisine      = ?,
            cook_time    = ?,
            servings     = ?,
            tags         = ?,
            instructions = ?
        WHERE id = ?
    """
    with get_connection() as conn:
        conn.execute(sql, (title, description, cuisine, cook_time, servings, tags, instructions, recipe_id))


def delete_recipe(recipe_id: int) -> None:
    """
    Delete a recipe and all its associated ingredients from the database.

    Ingredients are removed automatically via ON DELETE CASCADE.

    Args:
        recipe_id: The id of the recipe to delete.
    """
    sql = "DELETE FROM recipes WHERE id = ?"
    with get_connection() as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute(sql, (recipe_id,))


def get_all_recipes() -> list[dict]:
    """
    Retrieve all recipes from the database, sorted alphabetically by title.

    Returns:
        list[dict]: A list of recipes, each represented as a dictionary.
                    Includes the instructions field.
                    Returns an empty list if no recipes exist.
    """
    sql = """
        SELECT id, title, description, cuisine, cook_time, servings, tags, instructions
        FROM   recipes
        ORDER  BY title ASC
    """
    with get_connection() as conn:
        rows = conn.execute(sql).fetchall()
        return [dict(row) for row in rows]


def get_recipe_by_id(recipe_id: int) -> Optional[dict]:
    """
    Retrieve a single recipe by its id.

    Args:
        recipe_id: The id of the recipe to fetch.

    Returns:
        dict: The recipe as a dictionary including instructions,
              or None if not found.
    """
    sql = """
        SELECT id, title, description, cuisine, cook_time, servings, tags, instructions
        FROM   recipes
        WHERE  id = ?
    """
    with get_connection() as conn:
        row = conn.execute(sql, (recipe_id,)).fetchone()
        return dict(row) if row else None


# ---------------------------------------------------------------------------
# Ingredient functions
# ---------------------------------------------------------------------------

def add_ingredient(
    recipe_id: int,
    name: str,
    quantity: float,
    unit: str,
) -> None:
    """
    Insert a single ingredient linked to a recipe.

    Args:
        recipe_id: The id of the recipe this ingredient belongs to.
        name:      Ingredient name e.g. 'chicken breast'.
        quantity:  Numeric amount e.g. 200.0.
        unit:      Unit of measurement e.g. 'grams', 'cups', 'tbsp'.
    """
    sql = """
        INSERT INTO ingredients (recipe_id, name, quantity, unit)
        VALUES (?, ?, ?, ?)
    """
    with get_connection() as conn:
        conn.execute(sql, (recipe_id, name, quantity, unit))


def get_ingredients_by_recipe_id(recipe_id: int) -> list[dict]:
    """
    Retrieve all ingredients for a given recipe, ordered by insertion order.

    Args:
        recipe_id: The id of the recipe whose ingredients to fetch.

    Returns:
        list[dict]: A list of ingredients as dictionaries.
                    Returns an empty list if the recipe has no ingredients.
    """
    sql = """
        SELECT id, recipe_id, name, quantity, unit
        FROM   ingredients
        WHERE  recipe_id = ?
        ORDER  BY id ASC
    """
    with get_connection() as conn:
        rows = conn.execute(sql, (recipe_id,)).fetchall()
        return [dict(row) for row in rows]


# ---------------------------------------------------------------------------
# Meal planner functions
# ---------------------------------------------------------------------------

def save_meal_plan(
    week_start: str,
    day: str,
    meal_type: str,
    recipe_id: Optional[int],
) -> None:
    """
    Save or replace a meal plan slot for a given week, day, and meal type.

    Uses INSERT OR REPLACE to upsert — if a slot already exists for the
    same week_start, day, and meal_type combination, it is overwritten.

    Args:
        week_start: ISO date string for the Monday of the week e.g. '2024-03-04'.
        day:        Day of the week e.g. 'Monday', 'Tuesday'.
        meal_type:  One of 'Breakfast', 'Lunch', or 'Dinner'.
        recipe_id:  The id of the recipe to assign, or None to leave it empty.
    """
    clear_meal_slot(week_start, day, meal_type)

    sql = """
        INSERT INTO meal_plan (week_start, day, meal_type, recipe_id)
        VALUES (?, ?, ?, ?)
    """
    with get_connection() as conn:
        conn.execute(sql, (week_start, day, meal_type, recipe_id))


def get_meal_plan(week_start: str) -> list[dict]:
    """
    Retrieve the full meal plan for a given week.

    Joins with the recipes table to include the recipe title alongside
    each planned slot for convenient display in the UI.

    Args:
        week_start: ISO date string for the Monday of the week e.g. '2024-03-04'.

    Returns:
        list[dict]: A list of meal plan slots as dictionaries, each containing
                    week_start, day, meal_type, recipe_id, and recipe title.
                    Returns an empty list if nothing is planned for that week.
    """
    sql = """
        SELECT
            mp.id,
            mp.week_start,
            mp.day,
            mp.meal_type,
            mp.recipe_id,
            r.title AS recipe_title
        FROM      meal_plan mp
        LEFT JOIN recipes   r  ON mp.recipe_id = r.id
        WHERE     mp.week_start = ?
        ORDER BY  mp.day, mp.meal_type
    """
    with get_connection() as conn:
        rows = conn.execute(sql, (week_start,)).fetchall()
        return [dict(row) for row in rows]


def clear_meal_slot(week_start: str, day: str, meal_type: str) -> None:
    """
    Remove a specific meal slot from the plan.

    Args:
        week_start: ISO date string for the Monday of the week e.g. '2024-03-04'.
        day:        Day of the week e.g. 'Monday'.
        meal_type:  One of 'Breakfast', 'Lunch', or 'Dinner'.
    """
    sql = """
        DELETE FROM meal_plan
        WHERE  week_start = ?
          AND  day        = ?
          AND  meal_type  = ?
    """
    with get_connection() as conn:
        conn.execute(sql, (week_start, day, meal_type))