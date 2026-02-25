from global_styles import inject_global_styles
inject_global_styles()

import streamlit as st

from database import (
    get_all_recipes,
    get_ingredients_by_recipe_id,
)


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="What Can I Cook?",
    page_icon="🤔",
    layout="wide",
)


# ---------------------------------------------------------------------------
# CSS — minimal, stable selectors
# ---------------------------------------------------------------------------

st.markdown("""
<style>

.block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1100px; }

/* Full match card accent */
.full-match-accent {
    border-left: 5px solid #3DAA6A !important;
    background-color: #F4FBF7 !important;
}

/* Partial match card accent */
.partial-match-accent {
    border-left: 5px solid #F6C94E !important;
    background-color: #FFFDF0 !important;
}

/* Missing ingredient chip */
.missing-chip {
    display: inline-block;
    background: #FFE8E5;
    color: #C0392B;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-weight: 600;
    margin: 2px 3px 2px 0;
    border: 1px solid #F5C6C0;
}

/* Match % badge */
.pct-badge {
    font-size: 1.4rem;
    font-weight: 800;
    color: #D94F3D;
    line-height: 1;
}

/* Cuisine tag */
.cuisine-tag {
    display: inline-block;
    background: #E8F1F8;
    color: #1F6291;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-weight: 700;
    margin-right: 6px;
}

/* Summary metric */
.summary-num {
    font-size: 1.6rem;
    font-weight: 800;
    color: #1E2235;
    line-height: 1.1;
}

.summary-label {
    font-size: 0.76rem;
    color: #A0897E;
    font-weight: 500;
    margin-top: 0.1rem;
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
    transition: box-shadow 0.2s ease !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: 0 5px 20px rgba(30,34,53,0.1) !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def parse_user_ingredients(raw: str) -> set[str]:
    """
    Parse a free-text ingredient list into a normalized set.

    Accepts comma-separated or newline-separated input.
    Normalizes: lowercase, stripped whitespace, no empties, deduplicated.
    """
    unified = raw.replace("\n", ",")
    return {p.strip().lower() for p in unified.split(",") if p.strip()}


def get_recipe_ingredient_names(recipe_id: int) -> set[str]:
    """Fetch and normalize all ingredient names for a recipe."""
    ings = get_ingredients_by_recipe_id(recipe_id)
    return {
        ing["name"].strip().lower()
        for ing in ings
        if (ing.get("name") or "").strip()
    }


def match_recipes(
    user_ingredients: set[str],
    all_recipes: list[dict],
) -> tuple[list[dict], list[dict]]:
    """
    Compare user's ingredients against every recipe.

    For each recipe:
      - Compute intersection (matched) and difference (missing).
      - Classify as full match (nothing missing) or partial match.
      - Partial matches sorted descending by match percentage.

    Returns:
        (full_matches, partial_matches) — each a list of result dicts.
    """
    full_matches:    list[dict] = []
    partial_matches: list[dict] = []

    for recipe in all_recipes:
        recipe_ings = get_recipe_ingredient_names(recipe["id"])

        # Skip recipes with no ingredients — can't meaningfully score them
        if not recipe_ings:
            continue

        matched   = user_ingredients & recipe_ings          # set intersection
        missing   = recipe_ings - user_ingredients          # what user lacks
        total     = len(recipe_ings)
        match_pct = round(len(matched) / total * 100, 1)

        result = {
            "id":        recipe["id"],
            "title":     recipe["title"],
            "cuisine":   recipe.get("cuisine", ""),
            "cook_time": recipe.get("cook_time"),
            "servings":  recipe.get("servings"),
            "total":     total,
            "matched":   len(matched),
            "missing":   sorted(missing),
            "match_pct": match_pct,
        }

        if not missing:
            full_matches.append(result)
        elif matched:
            # Only include partials where the user has at least one ingredient
            partial_matches.append(result)

    # Best partial matches first
    partial_matches.sort(key=lambda r: r["match_pct"], reverse=True)

    return full_matches, partial_matches


def render_missing_chips(missing: list[str]) -> str:
    """Return HTML chip spans for missing ingredients."""
    return "".join(
        f'<span class="missing-chip">+ {item.title()}</span>'
        for item in missing
    )


def render_cuisine_tag(cuisine: str) -> str:
    if not cuisine:
        return ""
    return f'<span class="cuisine-tag">{cuisine}</span>'


# ---------------------------------------------------------------------------
# Page header
# ---------------------------------------------------------------------------

st.title("🤔 What Can I Cook?")
st.markdown(
    '<p style="color:#A0897E; margin-top:-0.4rem; margin-bottom:1.2rem; font-size:0.97rem;">'
    "Tell us what's in your kitchen and we'll find recipes you can make right now — "
    "or almost make with just a few extra ingredients."
    "</p>",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Load all recipes — early empty state
# ---------------------------------------------------------------------------

all_recipes = get_all_recipes()

if not all_recipes:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(
            '<p style="text-align:center; color:#A0897E; padding:1.2rem 0; font-size:1rem;">'
            "🍽️ You don't have any recipes yet. Add some to use this feature!"
            "</p>",
            unsafe_allow_html=True,
        )
        _, ctr, _ = st.columns([1, 2, 1])
        with ctr:
            st.page_link("pages/add_recipe.py", label="➕ Add Your First Recipe", use_container_width=True)
    st.stop()


# ---------------------------------------------------------------------------
# Ingredient input section
# ---------------------------------------------------------------------------

with st.container(border=True):
    st.markdown(
        '<p style="font-weight:700; font-size:1rem; color:#1E2235; margin-bottom:0.1rem;">'
        "🧺 What's in your kitchen?"
        "</p>",
        unsafe_allow_html=True,
    )
    st.caption("Enter ingredients one per line, or comma-separated. Quantities don't matter — just the names.")

    raw_input = st.text_area(
        label            = "Ingredients",
        placeholder      = "e.g.\nchicken breast\ngarlic\ntomato\nrice\n\nor: chicken, garlic, tomato, rice",
        height           = 160,
        label_visibility = "collapsed",
    )

    user_ingredients = parse_user_ingredients(raw_input)

    col_feedback, col_btn = st.columns([4, 1])

    with col_feedback:
        if user_ingredients:
            st.caption(
                f"✅ **{len(user_ingredients)}** ingredient(s) detected: "
                f"{', '.join(sorted(user_ingredients))}"
            )
        else:
            st.caption("Start typing to see your ingredient count.")

    with col_btn:
        search_clicked = st.button(
            "🔍 Find Recipes",
            type="primary",
            use_container_width=True,
            disabled=not bool(user_ingredients),
        )


# ---------------------------------------------------------------------------
# First-load state — nothing entered yet
# ---------------------------------------------------------------------------

if not user_ingredients and not search_clicked:
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👆 Enter the ingredients you have above and click **Find Recipes** to get started.")
    st.stop()

if not user_ingredients:
    st.warning("Please enter at least one ingredient to search.")
    st.stop()


# ---------------------------------------------------------------------------
# Run matching algorithm
# ---------------------------------------------------------------------------

full_matches, partial_matches = match_recipes(user_ingredients, all_recipes)

total_matched = len(full_matches) + len(partial_matches)

st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Results summary bar
# ---------------------------------------------------------------------------

s1, s2, s3 = st.columns(3, gap="medium")

with s1:
    with st.container(border=True):
        st.markdown(
            f'<div class="summary-num" style="color:#3DAA6A;">{len(full_matches)}</div>'
            f'<div class="summary-label">recipes ready to cook</div>',
            unsafe_allow_html=True,
        )

with s2:
    with st.container(border=True):
        st.markdown(
            f'<div class="summary-num" style="color:#D4A017;">{len(partial_matches)}</div>'
            f'<div class="summary-label">recipes almost there</div>',
            unsafe_allow_html=True,
        )

with s3:
    with st.container(border=True):
        st.markdown(
            f'<div class="summary-num">{len(all_recipes)}</div>'
            f'<div class="summary-label">total recipes checked</div>',
            unsafe_allow_html=True,
        )

st.markdown("<div style='margin-top:1.4rem;'></div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# ✅ Full match section
# ---------------------------------------------------------------------------

st.markdown(
    '<p style="font-size:1.2rem; font-weight:800; color:#1E2235; margin-bottom:0.6rem;">'
    "✅ Ready to Cook Right Now"
    "</p>",
    unsafe_allow_html=True,
)

if full_matches:
    st.markdown(
        f'<p style="color:#A0897E; font-size:0.87rem; margin-bottom:0.8rem;">'
        f"You have every ingredient needed for {len(full_matches)} recipe(s)."
        f"</p>",
        unsafe_allow_html=True,
    )

    # Two-column grid for full match cards
    cols = st.columns(2, gap="medium")

    for i, recipe in enumerate(full_matches):
        with cols[i % 2]:
            with st.container(border=True):
                # Green accent via inline style on the container's inner div
                st.markdown(
                    f'<div style="border-left:5px solid #3DAA6A; border-radius:6px; '
                    f'background:#F4FBF7; padding:0.8rem 1rem; margin:-0.5rem;">'
                    f'<div style="font-size:1.1rem; font-weight:800; color:#1E2235; margin-bottom:0.3rem;">'
                    f'🍽️ {recipe["title"]}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                # Cuisine + meta line
                meta_parts = []
                if recipe["cuisine"]:
                    meta_parts.append(recipe["cuisine"])
                if recipe["cook_time"]:
                    meta_parts.append(f"⏱ {recipe['cook_time']} mins")
                if recipe["servings"]:
                    meta_parts.append(f"👥 {recipe['servings']} servings")

                if meta_parts:
                    st.markdown(
                        f'<p style="font-size:0.82rem; color:#6B9E7A; margin:0.1rem 0 0.4rem 0;">'
                        f'{" · ".join(meta_parts)}</p>',
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    f'<p style="font-size:0.85rem; color:#3DAA6A; font-weight:600; margin:0;">'
                    f'✅ All {recipe["total"]} ingredients available'
                    f'</p>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)
                st.page_link(
                    "pages/recipes.py",
                    label="📖 View Recipe",
                    use_container_width=True,
                )

else:
    st.info(
        "No recipes fully match your ingredients yet. "
        "Check the partial matches below — you might only need one or two more items!",
        icon="💡",
    )

st.markdown("<div style='margin-top:1.6rem;'></div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 🟡 Partial match section
# ---------------------------------------------------------------------------

st.markdown(
    '<p style="font-size:1.2rem; font-weight:800; color:#1E2235; margin-bottom:0.6rem;">'
    "🟡 Almost There"
    "</p>",
    unsafe_allow_html=True,
)

if partial_matches:
    st.markdown(
        f'<p style="color:#A0897E; font-size:0.87rem; margin-bottom:0.8rem;">'
        f"{len(partial_matches)} recipe(s) need just a few more ingredients — sorted by best match."
        f"</p>",
        unsafe_allow_html=True,
    )

    for recipe in partial_matches:
        with st.container(border=True):
            # Yellow accent strip + layout
            left_col, right_col = st.columns([4, 1])

            with left_col:
                st.markdown(
                    f'<div style="border-left:5px solid #F6C94E; border-radius:6px; '
                    f'background:#FFFDF0; padding:0.7rem 1rem; margin:-0.5rem 0 0 -0.5rem;">'
                    f'<div style="font-size:1.05rem; font-weight:800; color:#1E2235;">'
                    f'🍳 {recipe["title"]}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                if recipe["cuisine"]:
                    st.markdown(
                        f'<p style="font-size:0.8rem; color:#8B7355; margin:0.2rem 0 0.4rem 0;">'
                        f'{recipe["cuisine"]}</p>',
                        unsafe_allow_html=True,
                    )

                # Progress bar for match level
                st.progress(
                    value=recipe["match_pct"] / 100,
                    text=f"{recipe['matched']} of {recipe['total']} ingredients available",
                )

                # Missing ingredient chips
                if recipe["missing"]:
                    chips_html = render_missing_chips(recipe["missing"])
                    st.markdown(
                        f'<p style="font-size:0.78rem; color:#A0897E; margin:0.4rem 0 0.2rem 0; font-weight:600;">'
                        f'Still need:</p>'
                        f'<div style="margin-bottom:0.5rem;">{chips_html}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

            with right_col:
                st.markdown(
                    f'<div style="text-align:center; padding-top:0.4rem;">'
                    f'<div class="pct-badge">{recipe["match_pct"]}%</div>'
                    f'<div style="font-size:0.72rem; color:#A0897E; margin-top:0.2rem;">match</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

else:
    if full_matches:
        st.caption("🎉 All matching recipes are full matches — your pantry is well-stocked!")
    else:
        st.info(
            "No recipes matched your ingredients. Try adding more ingredients above, "
            "or add more recipes to your collection.",
            icon="🍽️",
        )


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

st.markdown("<div style='margin-top:1.4rem;'></div>", unsafe_allow_html=True)
st.divider()

if total_matched == 0:
    st.caption("💡 Tip: Add more recipes to your library to get better results.")
else:
    st.caption(
        f"Checked {len(all_recipes)} recipes · "
        f"{len(full_matches)} full match(es) · "
        f"{len(partial_matches)} partial match(es)."
    )

st.page_link("pages/add_recipe.py", label="➕ Add More Recipes")