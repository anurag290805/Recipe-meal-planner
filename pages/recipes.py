from global_styles import inject_global_styles
inject_global_styles()
import streamlit as st

from database import (
    get_all_recipes,
    get_ingredients_by_recipe_id,
    delete_recipe,
)


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title = "Recipe Library",
    page_icon  = "📚",
    layout     = "wide",
)


# ---------------------------------------------------------------------------
# Warm-coral CSS — consistent with global dashboard style
# ---------------------------------------------------------------------------

st.markdown("""
<style>

/* ── Layout ───────────────────────────────────────────────────────────────── */
.block-container {
    padding-top: 1.8rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* ── Buttons ──────────────────────────────────────────────────────────────── */
div[data-testid="stButton"] > button,
div[data-testid="stButton"] > button p,
div[data-testid="stButton"] > button span {
    background-color: #1E2235 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    box-shadow: 0 3px 10px rgba(30, 34, 53, 0.18) !important;
    transition: all 0.18s ease !important;
}

div[data-testid="stButton"] > button:hover,
div[data-testid="stButton"] > button:hover p {
    background-color: #D94F3D !important;
    color: #FFFFFF !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(217, 79, 61, 0.28) !important;
}

/* ── Page links ───────────────────────────────────────────────────────────── */
div[data-testid="stPageLink"] a,
div[data-testid="stPageLink"] a span,
div[data-testid="stPageLink"] a p,
div[data-testid="stPageLink"] a * {
    background-color: #1E2235 !important;
    color: #FFFFFF !important;
    text-decoration: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.87rem !important;
    text-align: center !important;
    border: none !important;
    box-shadow: 0 3px 10px rgba(30, 34, 53, 0.2) !important;
    transition: all 0.18s ease !important;
}

div[data-testid="stPageLink"] a { display: block !important; padding: 0.5rem 0.8rem !important; }

div[data-testid="stPageLink"] a:hover,
div[data-testid="stPageLink"] a:hover * {
    background-color: #D94F3D !important;
    color: #FFFFFF !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(217, 79, 61, 0.3) !important;
}

/* ── Cards ────────────────────────────────────────────────────────────────── */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 14px !important;
    border: 1.5px solid #F0D9CF !important;
    background-color: #FFFCFA !important;
    box-shadow: 0 2px 12px rgba(30, 34, 53, 0.06) !important;
    transition: box-shadow 0.2s ease !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: 0 5px 20px rgba(30, 34, 53, 0.1) !important;
}

/* ── Expanders ────────────────────────────────────────────────────────────── */
details[data-testid="stExpander"] {
    border-radius: 10px !important;
    border: 1px solid #F0D9CF !important;
    background-color: #FFFAF7 !important;
}

/* ── Sidebar ──────────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background-color: #F8EDE5 !important;
    border-right: 1px solid #F0D9CF !important;
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
}

section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"] span,
section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"] p {
    font-size: 1rem !important;
    color: inherit !important;
    text-transform: capitalize !important;
}

/* ── Divider ──────────────────────────────────────────────────────────────── */
hr { border-color: #F0D9CF !important; }

/* ── Custom classes ───────────────────────────────────────────────────────── */

.cuisine-badge {
    display: inline-block;
    background: #E8F1F8;
    color: #1F6291;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-weight: 700;
    margin-right: 6px;
    letter-spacing: 0.02em;
}

.tag-chip {
    display: inline-block;
    background: #FDE8DF;
    color: #D94F3D;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.71rem;
    font-weight: 600;
    margin: 2px 2px 0 0;
}

.recipe-meta {
    font-size: 0.82rem;
    color: #A0897E;
    margin: 0.25rem 0 0.45rem 0;
    line-height: 1.5;
}

.recipe-desc {
    font-size: 0.87rem;
    color: #5C5247;
    line-height: 1.55;
    margin-bottom: 0.5rem;
}

.ing-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.28rem 0;
    border-bottom: 1px solid #F5EBE0;
    font-size: 0.86rem;
}

.ing-name { color: #1E2235; font-weight: 500; }
.ing-qty  { color: #A0897E; font-size: 0.82rem; }

.result-count {
    font-size: 0.83rem;
    color: #A0897E;
    margin-bottom: 1rem;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def parse_tags(tags_str: str) -> list[str]:
    """Parse a comma-separated tags string into a clean lowercase list."""
    if not tags_str:
        return []
    return [t.strip().lower() for t in tags_str.split(",") if t.strip()]


def render_tag_chips(tags_str: str, limit: int = 5) -> str:
    """Return HTML chip elements for up to `limit` tags."""
    tags = parse_tags(tags_str)
    if not tags:
        return ""
    return "".join(f'<span class="tag-chip">{t}</span>' for t in tags[:limit])


def render_cuisine_badge(cuisine: str) -> str:
    """Return a styled cuisine badge HTML element."""
    if not cuisine:
        return ""
    return f'<span class="cuisine-badge">{cuisine}</span>'


def format_quantity(qty: float | None) -> str:
    """Display quantity without trailing zeros (e.g. 2.0 → '2', 1.5 → '1.5')."""
    if qty is None:
        return ""
    return str(int(qty)) if float(qty) == int(qty) else str(round(qty, 2))


def get_unique_cuisines(recipes: list[dict]) -> list[str]:
    """Return sorted list of unique cuisines from all recipes."""
    return sorted({r["cuisine"] for r in recipes if r.get("cuisine")})


def get_unique_tags(recipes: list[dict]) -> list[str]:
    """Return sorted list of unique tags across all recipes."""
    tags: set[str] = set()
    for r in recipes:
        tags.update(parse_tags(r.get("tags", "")))
    return sorted(tags)


def apply_filters(
    recipes:         list[dict],
    search_query:    str,
    filter_cuisines: list[str],
    filter_tags:     list[str],
) -> list[dict]:
    """
    Apply search text, cuisine, and tag filters to the recipe list.
    All three filters are additive (AND logic).
    """
    result = recipes

    if search_query.strip():
        q = search_query.strip().lower()
        result = [r for r in result if q in r["title"].lower()]

    if filter_cuisines:
        result = [r for r in result if r.get("cuisine") in filter_cuisines]

    if filter_tags:
        result = [
            r for r in result
            if any(tag in parse_tags(r.get("tags", "")) for tag in filter_tags)
        ]

    return result


def render_instructions(instructions_raw: str | None) -> None:
    """
    Render the cooking instructions section inside the detail expander.

    Each non-empty line is treated as one step and numbered automatically.
    Any leading 'Step N:' prefix the user typed is stripped to avoid
    double-numbering. Shows a warm fallback caption when instructions
    are absent.

    Args:
        instructions_raw: Raw instructions string from the database.
                          May be None, empty, or multi-line.
    """
    st.markdown(
        "<p style='font-size:0.78rem; font-weight:700; text-transform:uppercase; "
        "letter-spacing:0.07em; color:#A0897E; margin-bottom:0.3rem;'>📖 Instructions</p>",
        unsafe_allow_html=True,
    )

    instructions_clean = (instructions_raw or "").strip()

    if not instructions_clean:
        st.caption("Instructions not added yet. Edit this recipe to add step-by-step instructions.")
        return

    # Split into individual steps; ignore blank lines
    lines = [line.strip() for line in instructions_clean.splitlines() if line.strip()]

    for i, line in enumerate(lines, start=1):
        # Strip any 'Step N:' / 'Step N.' prefix the user may have typed
        if line.lower().startswith("step"):
            parts = line.split(":", 1)
            if len(parts) == 2:
                line = parts[1].strip()

        st.markdown(f"**{i}.** {line}")


# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------

all_recipes = get_all_recipes()


# ---------------------------------------------------------------------------
# Page header
# ---------------------------------------------------------------------------

st.title("📚 Recipe Library")
st.markdown(
    '<p style="color:#A0897E; margin-top:-0.4rem; margin-bottom:1.2rem; font-size:0.97rem;">'
    "Search and manage your recipe collection. Click any card to view ingredients and details."
    "</p>",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Empty state
# ---------------------------------------------------------------------------

if not all_recipes:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(
            '<p style="text-align:center; color:#A0897E; padding:1.2rem 0; font-size:1rem;">'
            "🍽️ Your recipe collection is empty. Add your first recipe to get started."
            "</p>",
            unsafe_allow_html=True,
        )
        _, ctr, _ = st.columns([1, 2, 1])
        with ctr:
            st.page_link("pages/add_recipe.py", label="➕ Add Your First Recipe", use_container_width=True)
    st.stop()


# ---------------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("### 🔍 Filter Recipes")

    filter_cuisines = st.multiselect(
        label   = "Cuisine",
        options = get_unique_cuisines(all_recipes),
        help    = "Show only recipes from selected cuisines.",
    )

    filter_tags = st.multiselect(
        label   = "Tags",
        options = get_unique_tags(all_recipes),
        help    = "Show recipes that match any of these tags.",
    )

    st.divider()
    st.page_link("pages/add_recipe.py", label="➕ Add New Recipe", use_container_width=True)


# ---------------------------------------------------------------------------
# Search bar
# ---------------------------------------------------------------------------

search_query = st.text_input(
    label            = "",
    placeholder      = "🔎  Search recipes by name…",
    label_visibility = "collapsed",
)

# ---------------------------------------------------------------------------
# Apply filters
# ---------------------------------------------------------------------------

filtered_recipes = apply_filters(all_recipes, search_query, filter_cuisines, filter_tags)

# Result count summary
active_filters = bool(search_query.strip() or filter_cuisines or filter_tags)
count_label    = "filtered" if active_filters else "total"
st.markdown(
    f'<p class="result-count">Showing <strong>{len(filtered_recipes)}</strong> '
    f'{count_label} recipes</p>',
    unsafe_allow_html=True,
)

# No results from search/filter
if not filtered_recipes:
    st.warning("No recipes match your search or filters. Try adjusting them.", icon="🔍")
    st.stop()


# ---------------------------------------------------------------------------
# Recipe card renderer
# ---------------------------------------------------------------------------

def render_recipe_card(recipe: dict) -> None:
    """
    Render a full recipe card with title, metadata, description,
    tags, expandable ingredient + instruction detail, and edit/delete actions.

    Args:
        recipe: Dict of recipe fields from the database.
    """
    with st.container(border=True):

        # ── Title ──────────────────────────────────────────────────────────
        st.markdown(f"### {recipe['title']}")

        # ── Cuisine badge + cook time + servings ───────────────────────────
        cuisine_html = render_cuisine_badge(recipe.get("cuisine", ""))
        st.markdown(
            f'<div class="recipe-meta">'
            f'{cuisine_html}'
            f'⏱ {recipe.get("cook_time", "?")} mins &nbsp;·&nbsp; '
            f'👥 {recipe.get("servings", "?")} servings'
            f'</div>',
            unsafe_allow_html=True,
        )

        # ── Description preview ────────────────────────────────────────────
        desc = (recipe.get("description") or "").strip()
        if desc:
            preview = desc[:115] + "…" if len(desc) > 115 else desc
            st.markdown(
                f'<p class="recipe-desc">{preview}</p>',
                unsafe_allow_html=True,
            )

        # ── Tag chips ──────────────────────────────────────────────────────
        chips = render_tag_chips(recipe.get("tags", ""))
        if chips:
            st.markdown(chips, unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom:0.5rem'></div>", unsafe_allow_html=True)

        # ── Expandable detail section ──────────────────────────────────────
        with st.expander("🥕 Ingredients & Instructions"):

            # ── Ingredients ───────────────────────────────────────────────
            st.markdown(
                "<p style='font-size:0.78rem; font-weight:700; text-transform:uppercase; "
                "letter-spacing:0.07em; color:#A0897E; margin-bottom:0.3rem;'>🥕 Ingredients</p>",
                unsafe_allow_html=True,
            )

            ingredients = get_ingredients_by_recipe_id(recipe["id"])

            if ingredients:
                for ing in ingredients:
                    qty_str  = format_quantity(ing.get("quantity"))
                    unit_str = ing.get("unit", "")
                    name_str = ing.get("name", "").title()
                    st.markdown(
                        f'<div class="ing-row">'
                        f'<span class="ing-name">{name_str}</span>'
                        f'<span class="ing-qty">{qty_str} {unit_str}</span>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.caption("No ingredients recorded for this recipe.")

            # Full description in detail view (if truncated on the card)
            if desc and len(desc) > 115:
                st.markdown("")
                st.markdown(
                    f'<p style="font-size:0.87rem; color:#5C5247; line-height:1.55; '
                    f'margin-top:0.6rem;">{desc}</p>',
                    unsafe_allow_html=True,
                )

            # All tags
            if recipe.get("tags"):
                st.markdown(
                    f'<p style="font-size:0.79rem; color:#A0897E; margin-top:0.5rem;">'
                    f'🏷️ {recipe["tags"]}</p>',
                    unsafe_allow_html=True,
                )

            # ── Instructions ───────────────────────────────────────────────
            # Separated from ingredients by a divider for clear visual hierarchy.
            # render_instructions() handles None, empty, and multi-line strings.
            st.divider()
            render_instructions(recipe.get("instructions"))

        # ── Edit & Delete actions ──────────────────────────────────────────
        btn_col, del_col, _ = st.columns([1, 1, 2])
        recipe_id            = recipe["id"]
        confirm_key          = f"confirm_del_{recipe_id}"

        with btn_col:
            if st.button("✏️ Edit", key=f"edit_{recipe_id}", use_container_width=True):
                st.query_params["recipe_id"] = str(recipe_id)
                st.switch_page("pages/add_recipe.py")

        with del_col:
            if st.session_state.get(confirm_key):
                # Confirmation prompt replaces the delete button
                st.markdown(
                    '<p style="font-size:0.8rem; color:#D94F3D; margin:0.3rem 0 0.2rem;">Delete?</p>',
                    unsafe_allow_html=True,
                )
                y_col, n_col = st.columns(2)
                with y_col:
                    if st.button("✅", key=f"yes_{recipe_id}", use_container_width=True):
                        delete_recipe(recipe_id)
                        st.session_state.pop(confirm_key, None)
                        st.toast(f"'{recipe['title']}' deleted.", icon="🗑️")
                        st.rerun()
                with n_col:
                    if st.button("✕", key=f"no_{recipe_id}", use_container_width=True):
                        st.session_state.pop(confirm_key, None)
                        st.rerun()
            else:
                if st.button("🗑️ Delete", key=f"del_{recipe_id}", use_container_width=True):
                    st.session_state[confirm_key] = True
                    st.rerun()


# ---------------------------------------------------------------------------
# 2-column responsive card grid
# ---------------------------------------------------------------------------

left_col, right_col = st.columns(2, gap="medium")

# Interleave recipes across two columns for balanced heights
for i, recipe in enumerate(filtered_recipes):
    target_col = left_col if i % 2 == 0 else right_col
    with target_col:
        render_recipe_card(recipe)
