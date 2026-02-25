from database import create_tables, add_recipe, get_all_recipes # type: ignore

create_tables()
add_recipe("Pasta Carbonara", "Classic Italian pasta", "Italian", 20, 2, "quick, pasta")
print(get_all_recipes())