from global_styles import inject_global_styles
inject_global_styles()

import streamlit as st
from datetime import date, timedelta

from database import (
    get_meal_plan,
    get_ingredients_by_recipe_id,
)


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Grocery List",
    page_icon="🛒",
    layout="wide",
)


# ---------------------------------------------------------------------------
# CSS — minimal, stable selectors
# ---------------------------------------------------------------------------

st.markdown("""
<style>

.block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1100px; }

/* Category header */
.cat-header {
    font-size: 1rem;
    font-weight: 700;
    color: #1E2235;
    margin-bottom: 0.1rem;
}

.cat-badge {
    display: inline-block;
    background: #FDE8DF;
    color: #D94F3D;
    border-radius: 20px;
    padding: 1px 9px;
    font-size: 0.72rem;
    font-weight: 700;
    margin-left: 6px;
    vertical-align: middle;
}

/* Item quantity — right-aligned */
.qty-label {
    font-size: 0.84rem;
    color: #A0897E;
    text-align: right;
    padding-top: 0.45rem;
}

/* Manual items section */
.manual-header {
    font-size: 0.95rem;
    font-weight: 700;
    color: #1E2235;
    margin-bottom: 0.2rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #F8EDE5 !important;
    border-right: 1px solid #F0D9CF !important;
    padding: 1rem 0.5rem !important;
}

section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"] {
    display: block !important;
    background-color: #FFFAF7 !important;
    border: 1px solid #F0D9CF !important;
    border-radius: 10px !important;
    margin: 0.3rem 0.5rem !important;
    padding: 0.6rem 1rem !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    color: #1E2235 !important;
    text-transform: capitalize !important;
    text-decoration: none !important;
    transition: all 0.15s ease !important;
    box-shadow: 0 1px 4px rgba(30, 34, 53, 0.06) !important;
}

section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"]:hover {
    background-color: #FDE8DF !important;
    border-color: #D94F3D !important;
    color: #D94F3D !important;
    transform: translateX(3px) !important;
}

section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"][aria-current="page"] {
    background-color: #D94F3D !important;
    border-color: #D94F3D !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    box-shadow: 0 3px 10px rgba(217, 79, 61, 0.25) !important;
}

section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"] span,
section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"] p {
    font-size: 1rem !important;
    font-weight: inherit !important;
    color: inherit !important;
    text-transform: capitalize !important;
}

hr { border-color: #F0D9CF !important; }

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 14px !important;
    border: 1.5px solid #F0D9CF !important;
    background-color: #FFFCFA !important;
    box-shadow: 0 2px 12px rgba(30,34,53,0.06) !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "🥦 Produce": [
        "onion", "tomato", "garlic", "ginger", "potato", "carrot", "spinach",
        "lettuce", "cucumber", "pepper", "chilli", "lemon", "lime", "apple",
        "banana", "mango", "coriander", "parsley", "basil", "mint", "celery",
        "broccoli", "cauliflower", "mushroom", "zucchini", "eggplant", "avocado",
        "spring onion", "scallion", "cabbage", "beetroot", "radish", "peas",
        "capsicum", "leek", "fennel", "artichoke", "asparagus",
    ],
    "🍗 Meat & Protein": [
        "chicken", "beef", "lamb", "pork", "fish", "prawn", "shrimp", "salmon",
        "tuna", "egg", "tofu", "paneer", "mutton", "turkey", "bacon", "sausage",
        "mince", "steak", "breast", "thigh", "fillet", "chorizo", "anchovy",
    ],
    "🥛 Dairy": [
        "milk", "cream", "butter", "cheese", "yogurt", "curd", "ghee",
        "mozzarella", "parmesan", "ricotta", "condensed milk", "evaporated milk",
        "sour cream", "crème fraîche",
    ],
    "🌾 Grains & Pantry": [
        "rice", "flour", "pasta", "bread", "noodle", "oat", "lentil", "dal",
        "chickpea", "kidney bean", "black bean", "sugar", "salt", "oil",
        "vinegar", "soy sauce", "tomato puree", "tomato paste", "stock",
        "broth", "cornstarch", "baking", "yeast", "honey", "jam", "spice",
        "masala", "cumin", "turmeric", "paprika", "chilli powder",
        "garam masala", "oregano", "thyme", "bay leaf", "cardamom",
        "cinnamon", "clove", "mustard", "ketchup", "mayo", "sauce",
        "coriander powder", "pepper",
    ],
}

CATEGORY_ORDER = [
    "🥦 Produce",
    "🍗 Meat & Protein",
    "🥛 Dairy",
    "🌾 Grains & Pantry",
    "🧂 Other",
]


# ---------------------------------------------------------------------------
# Week helpers
# ---------------------------------------------------------------------------

def get_current_week_start() -> str:
    """Return ISO Monday date string for the current week."""
    today  = date.today()
    monday = today - timedelta(days=today.weekday())
    return monday.isoformat()


def format_week_label(week_start_str: str) -> str:
    monday = date.fromisoformat(week_start_str)
    sunday = monday + timedelta(days=6)
    return f"{monday.strftime('%a %d %b')} → {sunday.strftime('%a %d %b %Y')}"


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def get_planned_recipe_ids(meal_plan: list[dict]) -> list[int]:
    """Extract unique, non-null recipe IDs from the meal plan."""
    seen: set[int] = set()
    ids: list[int] = []
    for slot in meal_plan:
        rid = slot.get("recipe_id")
        if rid is not None and rid not in seen:
            seen.add(rid)
            ids.append(rid)
    return ids


# ---------------------------------------------------------------------------
# ⭐ Ingredient merging
# ---------------------------------------------------------------------------

def merge_ingredients(all_ingredients: list[dict]) -> dict[str, dict[str, float]]:
    """
    Merge a flat list of ingredient dicts by name + unit.

    Strategy:
      - Normalize names to lowercase for grouping.
      - Same name + same unit  → sum quantities together.
      - Same name + diff unit  → keep as separate unit entries.
      - Skip entries with blank names.

    Returns:
        { "chicken breast": { "grams": 350.0 }, "flour": { "cups": 1.0, "grams": 200.0 } }
    """
    merged: dict[str, dict[str, float]] = {}

    for ing in all_ingredients:
        name = (ing.get("name") or "").strip()
        if not name:
            continue

        name_key = name.lower()
        unit     = (ing.get("unit") or "unit").strip().lower()
        quantity = float(ing.get("quantity") or 0.0)

        # Ensure the name bucket exists
        if name_key not in merged:
            merged[name_key] = {}

        # Add to existing unit total, or create a new unit entry
        merged[name_key][unit] = merged[name_key].get(unit, 0.0) + quantity

    return merged


# ---------------------------------------------------------------------------
# Ingredient categorization
# ---------------------------------------------------------------------------

def categorize_ingredient(name: str) -> str:
    """Return the category for an ingredient name using keyword matching."""
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in name:
                return category
    return "🧂 Other"


def build_categorized_list(merged: dict[str, dict[str, float]]) -> dict[str, list[dict]]:
    """
    Group merged ingredients into display categories.

    Each item in a category list: { name, quantity, unit }
    Items sorted alphabetically within each category.
    """
    categories: dict[str, list[dict]] = {cat: [] for cat in CATEGORY_ORDER}

    for name_key, unit_map in merged.items():
        cat = categorize_ingredient(name_key)
        for unit, qty in unit_map.items():
            categories[cat].append({
                "name":     name_key.title(),
                "quantity": qty,
                "unit":     unit,
            })

    # Sort alphabetically within each category
    for cat in categories:
        categories[cat].sort(key=lambda x: x["name"])

    return categories


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def format_qty(qty: float) -> str:
    """Display quantity without unnecessary trailing zeros."""
    return str(int(qty)) if qty == int(qty) else str(round(qty, 2))


def checkbox_key(name: str, unit: str, prefix: str = "chk") -> str:
    """Generate a stable session state key for a checkbox."""
    safe = f"{name}_{unit}".replace(" ", "_").lower()
    return f"{prefix}_{safe}"


def count_checked(keys: list[str]) -> int:
    """Count how many checkbox keys are True in session state."""
    return sum(1 for k in keys if st.session_state.get(k, False))


# ---------------------------------------------------------------------------
# Session state init
# ---------------------------------------------------------------------------

if "manual_items" not in st.session_state:
    st.session_state.manual_items: list[str] = [] # type: ignore


# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------

week_start = get_current_week_start()
meal_plan  = get_meal_plan(week_start)


# ---------------------------------------------------------------------------
# Page header
# ---------------------------------------------------------------------------

st.title("🛒 Grocery List")
st.markdown(
    '<p style="color:#A0897E; margin-top:-0.4rem; margin-bottom:0.4rem; font-size:0.97rem;">'
    "Your shopping list, auto-built from this week's meal plan. Tick as you go!"
    "</p>",
    unsafe_allow_html=True,
)
st.caption(f"📆 {format_week_label(week_start)}")
st.divider()


# ---------------------------------------------------------------------------
# Empty state — no meals planned
# ---------------------------------------------------------------------------

planned_ids = get_planned_recipe_ids(meal_plan)

if not planned_ids:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(
            '<p style="text-align:center; color:#A0897E; padding:1.2rem 0; font-size:1rem;">'
            "📅 No meals planned for this week yet."
            "</p>",
            unsafe_allow_html=True,
        )
        _, ctr, _ = st.columns([1, 2, 1])
        with ctr:
            st.page_link("pages/meal_planner.py", label="📅 Go to Meal Planner", use_container_width=True)
    st.stop()


# ---------------------------------------------------------------------------
# Collect, merge, and categorize ingredients
# ---------------------------------------------------------------------------

all_ingredients: list[dict] = []
for rid in planned_ids:
    all_ingredients.extend(get_ingredients_by_recipe_id(rid))

merged      = merge_ingredients(all_ingredients)
categorized = build_categorized_list(merged)

# Build a flat list of all checkbox keys (for progress tracking)
all_chk_keys: list[str] = []
for cat in CATEGORY_ORDER:
    for item in categorized[cat]:
        all_chk_keys.append(checkbox_key(item["name"], item["unit"]))

# Manual item keys
manual_chk_keys = [checkbox_key(item, "manual", prefix="manual_chk") for item in st.session_state.manual_items]
all_chk_keys_total = all_chk_keys + manual_chk_keys

total_items   = len(all_chk_keys_total)
checked_items = count_checked(all_chk_keys_total)


# ---------------------------------------------------------------------------
# Progress bar
# ---------------------------------------------------------------------------

progress_pct = checked_items / total_items if total_items else 0.0

prog_col, clear_col = st.columns([6, 1])

with prog_col:
    st.progress(
        value = progress_pct,
        text  = f"**{checked_items} / {total_items}** items checked  ({int(progress_pct * 100)}% done)",
    )

with clear_col:
    if st.button("🔄 Clear all", use_container_width=True, help="Reset all checkboxes"):
        for k in all_chk_keys_total:
            st.session_state[k] = False
        st.rerun()

st.markdown("<div style='margin-bottom:0.8rem;'></div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Category sections
# ---------------------------------------------------------------------------

for cat in CATEGORY_ORDER:
    items = categorized.get(cat, [])
    if not items:
        continue

    # Category header with item count badge
    st.markdown(
        f'<div class="cat-header">{cat} <span class="cat-badge">{len(items)}</span></div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        # Two items per visual row using columns
        # Each item: [checkbox+name col] [qty col]
        for item in items:
            chk_key  = checkbox_key(item["name"], item["unit"])
            qty_text = f"{format_qty(item['quantity'])} {item['unit']}"
            is_done  = st.session_state.get(chk_key, False)

            name_col, qty_col = st.columns([4, 1])

            with name_col:
                # Strike-through name when checked
                label = f"~~{item['name']}~~" if is_done else item["name"]
                st.checkbox(label=label, key=chk_key)

            with qty_col:
                color = "#C8BDB8" if is_done else "#A0897E"
                st.markdown(
                    f'<div class="qty-label" style="color:{color};">{qty_text}</div>',
                    unsafe_allow_html=True,
                )

    st.markdown("<div style='margin-bottom:0.6rem;'></div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Manual items section
# ---------------------------------------------------------------------------

st.divider()

st.markdown(
    '<div class="manual-header">➕ Extra Items</div>'
    '<p style="font-size:0.83rem; color:#A0897E; margin-top:0.1rem; margin-bottom:0.7rem;">'
    "Anything else you need that isn't from your recipes."
    "</p>",
    unsafe_allow_html=True,
)

# Input row
input_col, add_col = st.columns([5, 1])

with input_col:
    new_item = st.text_input(
        label            = "Extra item",
        placeholder      = "e.g. Washing-up liquid, kitchen roll…",
        label_visibility = "collapsed",
    )

with add_col:
    if st.button("Add ➕", use_container_width=True):
        if new_item.strip():
            st.session_state.manual_items.append(new_item.strip())
            st.rerun()

# Display manual items
if st.session_state.manual_items:
    with st.container(border=True):
        for i, item in enumerate(st.session_state.manual_items):
            m_key    = checkbox_key(item, "manual", prefix="manual_chk")
            is_done  = st.session_state.get(m_key, False)
            label    = f"~~{item}~~" if is_done else item

            item_col, rm_col = st.columns([5, 1])

            with item_col:
                st.checkbox(label=label, key=m_key)

            with rm_col:
                if st.button("✕", key=f"rm_manual_{i}", help="Remove", use_container_width=True):
                    st.session_state.manual_items.pop(i)
                    # Clean up the checkbox key to avoid ghost state
                    st.session_state.pop(m_key, None)
                    st.rerun()
else:
    st.caption("No extra items yet.")


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)
st.divider()
st.caption("💡 Tip: Update your meal plan anytime and come back here for a fresh list.")
st.page_link("pages/meal_planner.py", label="📅 Update Meal Plan")
