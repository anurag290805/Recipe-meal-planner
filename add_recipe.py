from global_styles import inject_global_styles
inject_global_styles()

import sqlite3
import streamlit as st

from database import (
    add_recipe,
    update_recipe,
    add_ingredient,
    get_recipe_by_id,
    get_ingredients_by_recipe_id,
)


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Add / Edit Recipe",
    page_icon="📝",
    layout="wide",
)


# ---------------------------------------------------------------------------
# CSS — minimal, stable
# ---------------------------------------------------------------------------

st.markdown("""
<style>

.block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1200px; }

/* Step indicator */
.step-bar {
    display: flex;
    align-items: center;
    gap: 0;
    margin-bottom: 1.4rem;
    padding: 0.7rem 1.2rem;
    background: #FFFAF7;
    border: 1.5px solid #F0D9CF;
    border-radius: 12px;
}

.step-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.83rem;
    font-weight: 600;
    color: #C4A99A;
    flex: 1;
}

.step-item.active { color: #D94F3D; }
.step-item.done   { color: #3DAA6A; }

.step-dot {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: #F0D9CF;
    color: #A0897E;
    font-size: 0.72rem;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.step-item.active .step-dot { background: #D94F3D; color: #fff; }
.step-item.done   .step-dot { background: #3DAA6A; color: #fff; }

.step-connector {
    flex: 0 0 2rem;
    height: 2px;
    background: #F0D9CF;
    margin: 0 0.4rem;
}

/* Preview card internals */
.preview-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: #1E2235;
    margin-bottom: 0.25rem;
    word-break: break-word;
}

.preview-meta {
    font-size: 0.82rem;
    color: #A0897E;
    line-height: 1.7;
}

.preview-placeholder {
    font-size: 0.9rem;
    color: #C4A99A;
    font-style: italic;
}

/* Instructions preview inside card */
.preview-instructions {
    font-size: 0.8rem;
    color: #5C5247;
    line-height: 1.55;
    margin-top: 0.5rem;
    padding-top: 0.5rem;
    border-top: 1px solid #F0D9CF;
}

.preview-instructions-label {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #A0897E;
    margin-bottom: 0.25rem;
}

/* Tag chip */
.tag-chip {
    display: inline-block;
    background: #FDE8DF;
    color: #D94F3D;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.71rem;
    font-weight: 600;
    margin: 2px 3px 2px 0;
}

/* Cuisine badge */
.cuisine-badge {
    display: inline-block;
    background: #E8F1F8;
    color: #1F6291;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-weight: 700;
    margin-right: 6px;
}

/* Edit mode banner */
.edit-banner {
    background: #FDE8DF;
    border: 1px solid #F0C4B5;
    border-radius: 10px;
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
    font-weight: 600;
    color: #D94F3D;
    margin-bottom: 1rem;
    display: inline-block;
}

/* Section label */
.section-label {
    font-size: 1rem;
    font-weight: 700;
    color: #1E2235;
    margin-bottom: 0.4rem;
}

hr { border-color: #F0D9CF !important; }

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 14px !important;
    border: 1.5px solid #F0D9CF !important;
    background-color: #FFFCFA !important;
    box-shadow: 0 2px 12px rgba(30,34,53,0.06) !important;
}

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

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CUISINE_OPTIONS = ["Indian", "Italian", "Mexican", "Chinese", "American", "Mediterranean", "Other"]
UNIT_OPTIONS    = ["grams", "kg", "ml", "litres", "cups", "tbsp", "tsp", "pieces", "slices", "other"]


# ---------------------------------------------------------------------------
# Helper: detect edit mode
# ---------------------------------------------------------------------------

def get_edit_recipe_id() -> int | None:
    """Return recipe_id from query params if present and valid, else None."""
    params = st.query_params
    if "recipe_id" in params:
        try:
            return int(params["recipe_id"])
        except (ValueError, TypeError):
            return None
    return None


# ---------------------------------------------------------------------------
# Helper: ingredient session state
# ---------------------------------------------------------------------------

def init_ingredient_rows(prefill: list[dict] | None = None) -> None:
    """
    Initialise ingredient_rows in session state exactly once per page load.

    In Edit Mode, populate from the database. In Add Mode, start with one
    blank row. A guard key prevents re-initialisation on reruns.
    """
    if "ingredient_rows" not in st.session_state:
        if prefill:
            st.session_state.ingredient_rows = [
                {
                    "name":     row["name"],
                    "quantity": float(row["quantity"] or 0.0),
                    "unit":     row["unit"] if row["unit"] in UNIT_OPTIONS else "grams",
                }
                for row in prefill
            ]
        else:
            st.session_state.ingredient_rows = [{"name": "", "quantity": 0.0, "unit": "grams"}]


def collect_valid_ingredients() -> list[dict]:
    """Return only ingredient rows where the name is non-empty."""
    return [
        row for row in st.session_state.ingredient_rows
        if row["name"].strip()
    ]


# ---------------------------------------------------------------------------
# Helper: step indicator HTML
# ---------------------------------------------------------------------------

def render_step_indicator(has_title: bool, has_ingredients: bool) -> None:
    """
    Render a 3-step horizontal progress indicator.
    Steps advance based on form completion state.
    """
    step1_cls = "active" if not has_title else "done"
    step2_cls = "active" if has_title and not has_ingredients else ("done" if has_ingredients else "")
    step3_cls = "active" if has_title and has_ingredients else ""

    st.markdown(
        f"""
        <div class="step-bar">
            <div class="step-item {step1_cls}">
                <div class="step-dot">{"✓" if step1_cls == "done" else "1"}</div>
                Recipe Details
            </div>
            <div class="step-connector"></div>
            <div class="step-item {step2_cls}">
                <div class="step-dot">{"✓" if step2_cls == "done" else "2"}</div>
                Ingredients
            </div>
            <div class="step-connector"></div>
            <div class="step-item {step3_cls}">
                <div class="step-dot">3</div>
                Save
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Helper: live preview card
# ---------------------------------------------------------------------------

def render_preview_card(
    title: str,
    cuisine: str,
    cook_time: int,
    servings: int,
    tags: str,
    ingredient_count: int,
    instructions: str,
) -> None:
    """Render a real-time recipe preview inside a bordered container."""
    with st.container(border=True):
        st.markdown(
            '<p style="font-size:0.75rem; font-weight:700; text-transform:uppercase; '
            'letter-spacing:0.07em; color:#A0897E; margin-bottom:0.6rem;">Live Preview</p>',
            unsafe_allow_html=True,
        )

        # Title
        if title.strip():
            st.markdown(
                f'<div class="preview-title">{title.strip()}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="preview-placeholder">Your recipe title will appear here…</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)

        # Cuisine badge
        if cuisine:
            st.markdown(f'<span class="cuisine-badge">{cuisine}</span>', unsafe_allow_html=True)

        # Meta line
        meta = []
        if cook_time:        meta.append(f"⏱ {cook_time} mins")
        if servings:         meta.append(f"👥 {servings} servings")
        if ingredient_count: meta.append(f"🥕 {ingredient_count} ingredient(s)")

        if meta:
            st.markdown(
                f'<p class="preview-meta">{"  ·  ".join(meta)}</p>',
                unsafe_allow_html=True,
            )

        # Tag chips
        if tags.strip():
            tag_list = [t.strip() for t in tags.split(",") if t.strip()][:6]
            chips    = "".join(f'<span class="tag-chip">{t}</span>' for t in tag_list)
            st.markdown(
                f'<div style="margin-top:0.4rem;">{chips}</div>',
                unsafe_allow_html=True,
            )

        # Instructions preview — show a short truncated snippet
        instructions_clean = instructions.strip()
        if instructions_clean:
            # Truncate at 120 chars and add ellipsis if longer
            preview_text = (
                instructions_clean[:120] + "…"
                if len(instructions_clean) > 120
                else instructions_clean
            )
            # Replace newlines with a separator so it reads cleanly in one block
            preview_text = preview_text.replace("\n", "  ·  ")
            st.markdown(
                f'<div class="preview-instructions">'
                f'<div class="preview-instructions-label">📖 Instructions preview</div>'
                f'{preview_text}'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="preview-instructions">'
                '<div class="preview-instructions-label">📖 Instructions</div>'
                '<span style="color:#C4A99A; font-style:italic;">No instructions added yet.</span>'
                '</div>',
                unsafe_allow_html=True,
            )

        if not any([title.strip(), cuisine, cook_time, servings, tags.strip()]):
            st.caption("Fill in the form on the left to see your recipe preview here.")


# ---------------------------------------------------------------------------
# Determine mode
# ---------------------------------------------------------------------------

recipe_id       = get_edit_recipe_id()
is_edit_mode    = recipe_id is not None
existing_recipe = get_recipe_by_id(recipe_id)           if is_edit_mode else None
existing_ings   = get_ingredients_by_recipe_id(recipe_id) if is_edit_mode else None

# Guard: recipe_id given but not in DB
if is_edit_mode and existing_recipe is None:
    st.error("Recipe not found. It may have been deleted.")
    st.stop()

# Initialise ingredient rows once per mode switch.
# Unique key per recipe_id resets state cleanly when switching targets.
state_init_key = f"init_done_{recipe_id}"
if state_init_key not in st.session_state:
    if "ingredient_rows" in st.session_state:
        del st.session_state["ingredient_rows"]
    init_ingredient_rows(prefill=existing_ings)
    st.session_state[state_init_key] = True


# ---------------------------------------------------------------------------
# Page header
# ---------------------------------------------------------------------------

st.title("📝 Add / Edit Recipe")
st.markdown(
    '<p style="color:#A0897E; margin-top:-0.4rem; margin-bottom:0.8rem; font-size:0.97rem;">'
    "Build your recipe step by step — details first, then ingredients, then save."
    "</p>",
    unsafe_allow_html=True,
)

if is_edit_mode:
    st.markdown(
        f'<div class="edit-banner">✏️ Editing: {existing_recipe["title"]}</div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Determine current ingredient count for step indicator & preview
# ---------------------------------------------------------------------------

valid_ings_now   = collect_valid_ingredients()
ingredient_count = len(valid_ings_now)


# ---------------------------------------------------------------------------
# Step indicator (uses live state, so placed after init)
# ---------------------------------------------------------------------------

# Read widget values from session_state where available so the preview
# and step indicator stay in sync on every rerun. Fall back to DB values
# in edit mode for the very first render before any interaction.
preview_title        = st.session_state.get("form_title",        existing_recipe["title"]        if is_edit_mode else "")
preview_cuisine      = st.session_state.get("form_cuisine",      existing_recipe["cuisine"]      if is_edit_mode else CUISINE_OPTIONS[0])
preview_cooktime     = st.session_state.get("form_cook_time",    int(existing_recipe["cook_time"]) if is_edit_mode and existing_recipe["cook_time"] else 30)
preview_servings     = st.session_state.get("form_servings",     int(existing_recipe["servings"]) if is_edit_mode and existing_recipe["servings"] else 2)
preview_tags         = st.session_state.get("form_tags",         existing_recipe["tags"]         if is_edit_mode and existing_recipe["tags"] else "")
# Instructions also tracked for live preview — falls back to DB value in edit mode
preview_instructions = st.session_state.get("form_instructions", (existing_recipe.get("instructions") or "") if is_edit_mode else "")

render_step_indicator(
    has_title       = bool(preview_title.strip()),
    has_ingredients = ingredient_count > 0,
)


# ---------------------------------------------------------------------------
# Two-column layout: form (left) + preview (right)
# ---------------------------------------------------------------------------

form_col, preview_col = st.columns([3, 2], gap="large")


# ── Live preview panel (right) ────────────────────────────────────────────
with preview_col:
    render_preview_card(
        title            = preview_title,
        cuisine          = preview_cuisine,
        cook_time        = preview_cooktime,
        servings         = preview_servings,
        tags             = preview_tags,
        ingredient_count = ingredient_count,
        instructions     = preview_instructions,   # new
    )

    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

    # Tips panel
    with st.container(border=True):
        st.markdown(
            '<p style="font-size:0.78rem; font-weight:700; text-transform:uppercase; '
            'letter-spacing:0.06em; color:#A0897E; margin-bottom:0.5rem;">💡 Tips</p>',
            unsafe_allow_html=True,
        )
        st.caption("• Write one instruction step per line for the clearest result.")
        st.caption("• Tags help you filter recipes later — try 'quick', 'vegan', 'weekend'.")
        st.caption("• Quantities don't need to be exact — approximate is fine.")
        st.caption("• You can always come back and edit this recipe later.")


# ── Recipe details form (left) ────────────────────────────────────────────
with form_col:

    st.markdown('<div class="section-label">📋 Recipe Details</div>', unsafe_allow_html=True)

    with st.form(key="recipe_form"):

        title = st.text_input(
            label       = "Recipe Title *",
            value       = existing_recipe["title"] if is_edit_mode else "",
            placeholder = "e.g. Spaghetti Bolognese",
            help        = "Give your recipe a clear, memorable name.",
            key         = "form_title",
        )

        description = st.text_area(
            label       = "Description",
            value       = existing_recipe["description"] if is_edit_mode else "",
            placeholder = "A short description of the dish — its origin, flavour, or what makes it special.",
            height      = 90,
            help        = "Optional but helpful. Shown on recipe cards.",
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            cuisine_index = (
                CUISINE_OPTIONS.index(existing_recipe["cuisine"])
                if is_edit_mode and existing_recipe.get("cuisine") in CUISINE_OPTIONS
                else 0
            )
            cuisine = st.selectbox(
                label   = "Cuisine",
                options = CUISINE_OPTIONS,
                index   = cuisine_index,
                key     = "form_cuisine",
            )

        with c2:
            cook_time = st.number_input(
                label     = "Cook Time (mins)",
                value     = int(existing_recipe["cook_time"]) if is_edit_mode and existing_recipe.get("cook_time") else 30,
                min_value = 0,
                step      = 5,
                help      = "Total time including prep.",
                key       = "form_cook_time",
            )

        with c3:
            servings = st.number_input(
                label     = "Servings",
                value     = int(existing_recipe["servings"]) if is_edit_mode and existing_recipe.get("servings") else 2,
                min_value = 1,
                step      = 1,
                help      = "How many people does this serve?",
                key       = "form_servings",
            )

        tags = st.text_input(
            label       = "Tags",
            value       = existing_recipe["tags"] if is_edit_mode and existing_recipe.get("tags") else "",
            placeholder = "e.g. vegan, quick, healthy, gluten-free",
            help        = "Comma-separated. Used for filtering in the Recipe Library.",
            key         = "form_tags",
        )

        # ── Cooking Instructions ───────────────────────────────────────────
        # Sits inside st.form so it submits together with all other fields.
        # Pre-filled from the database in edit mode via existing_recipe.
        # Each line the user writes is rendered as a numbered step in the
        # recipe detail view — no need for them to manually number steps.

        st.markdown("<div style='margin-top:0.6rem;'></div>", unsafe_allow_html=True)
        st.markdown(
            '<div class="section-label">📖 Cooking Instructions</div>',
            unsafe_allow_html=True,
        )
        st.caption("Write step-by-step instructions. Use a new line for each step.")

        instructions = st.text_area(
            label            = "Cooking Instructions",
            value            = (existing_recipe.get("instructions") or "") if is_edit_mode else "",
            placeholder      = (
                "Heat the oil in a large pan over medium heat.\n"
                "Add the onion and fry for 5 minutes until softened.\n"
                "Stir in the garlic and cook for 1 more minute.\n"
                "Add the remaining ingredients and simmer for 20 minutes.\n"
                "Season to taste and serve."
            ),
            height           = 210,
            help             = "Optional but recommended. One step per line.",
            label_visibility = "collapsed",
            key              = "form_instructions",
        )

        st.markdown("<div style='margin-top:0.4rem;'></div>", unsafe_allow_html=True)
        st.divider()

        submitted = st.form_submit_button(
            label               = "💾 Save Recipe",
            use_container_width = True,
            type                = "primary",
        )


# ---------------------------------------------------------------------------
# Ingredients section — outside the form (forms can't be nested)
# ---------------------------------------------------------------------------

st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

with form_col:
    st.markdown('<div class="section-label">🥕 Ingredients</div>', unsafe_allow_html=True)
    st.caption("Add all the ingredients this recipe needs. Blank rows are ignored on save.")

    for i, row in enumerate(st.session_state.ingredient_rows):
        with st.container(border=True):
            n_col, q_col, u_col = st.columns([3, 1.2, 1.8])

            with n_col:
                st.session_state.ingredient_rows[i]["name"] = st.text_input(
                    label       = f"Ingredient {i + 1}",
                    value       = row["name"],
                    placeholder = "e.g. Chicken breast",
                    key         = f"ing_name_{i}",
                )

            with q_col:
                st.session_state.ingredient_rows[i]["quantity"] = st.number_input(
                    label     = "Qty",
                    value     = float(row["quantity"]),
                    min_value = 0.0,
                    step      = 0.5,
                    key       = f"ing_qty_{i}",
                )

            with u_col:
                unit_val = row["unit"] if row["unit"] in UNIT_OPTIONS else "grams"
                st.session_state.ingredient_rows[i]["unit"] = st.selectbox(
                    label   = "Unit",
                    options = UNIT_OPTIONS,
                    index   = UNIT_OPTIONS.index(unit_val),
                    key     = f"ing_unit_{i}",
                )

    st.markdown("<div style='margin-top:0.4rem;'></div>", unsafe_allow_html=True)

    add_ing_col, _ = st.columns([2, 5])
    with add_ing_col:
        if st.button("➕ Add Ingredient", use_container_width=True):
            st.session_state.ingredient_rows.append({"name": "", "quantity": 0.0, "unit": "grams"})
            st.rerun()


# ---------------------------------------------------------------------------
# Save logic
# ---------------------------------------------------------------------------

if submitted:

    # ── Validation ─────────────────────────────────────────────────────────
    if not title.strip():
        st.error("⚠️ Recipe title is required. Please give your recipe a name.")
        st.stop()

    valid_ingredients = collect_valid_ingredients()

    if not valid_ingredients:
        st.warning("⚠️ No ingredients added. Consider adding at least one.", icon="🥕")
        # Don't hard-stop — allow saving without ingredients if user insists

    # Instructions are recommended but not required — show a soft nudge only
    if not instructions.strip():
        st.info(
            "No cooking instructions added. You can edit this recipe later to add them.",
            icon="📖",
        )

    # Guard against extremely large pastes that could affect performance
    safe_instructions = instructions.strip()[:15_000]

    # ── Persist ───────────────────────────────────────────────────────────
    try:
        if is_edit_mode:
            update_recipe(
                recipe_id    = recipe_id,
                title        = title.strip(),
                description  = description.strip(),
                cuisine      = cuisine,
                cook_time    = int(cook_time),
                servings     = int(servings),
                tags         = tags.strip(),
                instructions = safe_instructions,
            )

            # Overwrite ingredients: delete existing rows, re-insert fresh
            conn = sqlite3.connect("recipes.db")
            conn.execute("DELETE FROM ingredients WHERE recipe_id = ?", (recipe_id,))
            conn.commit()
            conn.close()

            for ing in valid_ingredients:
                add_ingredient(
                    recipe_id = recipe_id,
                    name      = ing["name"].strip(),
                    quantity  = ing["quantity"],
                    unit      = ing["unit"],
                )

            st.success(f"✅ **{title.strip()}** updated successfully!")

        else:
            new_id = add_recipe(
                title        = title.strip(),
                description  = description.strip(),
                cuisine      = cuisine,
                cook_time    = int(cook_time),
                servings     = int(servings),
                tags         = tags.strip(),
                instructions = safe_instructions,
            )

            for ing in valid_ingredients:
                add_ingredient(
                    recipe_id = new_id,
                    name      = ing["name"].strip(),
                    quantity  = ing["quantity"],
                    unit      = ing["unit"],
                )

            st.success(f"✅ **{title.strip()}** added to your recipe collection!")

            # Reset state so the form is blank and ready for the next recipe
            del st.session_state["ingredient_rows"]
            st.session_state.pop(state_init_key, None)

        st.markdown("<div style='margin-top:0.4rem;'></div>", unsafe_allow_html=True)
        st.page_link("pages/recipes.py", label="📚 Go to Recipe Library")

    except Exception as e:
        st.error(f"Something went wrong while saving: {e}")