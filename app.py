from global_styles import inject_global_styles
inject_global_styles()
import streamlit as st
from datetime import date, timedelta

from database import create_tables, get_all_recipes, get_meal_plan


# ---------------------------------------------------------------------------
# Page config — must be first Streamlit call
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title = "Recipe Manager & Meal Planner",
    page_icon  = "🍽️",
    layout     = "wide",
)


# ---------------------------------------------------------------------------
# Global CSS
# ---------------------------------------------------------------------------

st.markdown("""
<style>

/* ── Layout ───────────────────────────────────────────────────────────────── */
.block-container {
    padding-top: 1.8rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* ── Hero banner ──────────────────────────────────────────────────────────── */
.hero {
    background: linear-gradient(135deg, #FFF0EC 0%, #FDE8DF 60%, #F9DDD3 100%);
    border-radius: 18px;
    padding: 2.2rem 2.8rem;
    border-left: 6px solid #D94F3D;
    margin-bottom: 1.8rem;
    box-shadow: 0 4px 20px rgba(217, 79, 61, 0.08);
}

.hero h1 {
    font-size: 2.1rem;
    font-weight: 800;
    color: #1E2235;
    margin: 0 0 0.5rem 0;
    line-height: 1.2;
}

.hero p {
    font-size: 1rem;
    color: #6B5B52;
    margin: 0;
    line-height: 1.6;
    max-width: 620px;
}

/* ── Page links — dark background, WHITE text forced ─────────────────────── */
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

div[data-testid="stPageLink"] a {
    display: block !important;
    padding: 0.55rem 0.8rem !important;
}

div[data-testid="stPageLink"] a:hover,
div[data-testid="stPageLink"] a:hover * {
    background-color: #D94F3D !important;
    color: #FFFFFF !important;
}

div[data-testid="stPageLink"] a:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(217, 79, 61, 0.3) !important;
}

/* ── st.button — dark, white text ────────────────────────────────────────── */
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

/* ── Sidebar — larger text, individual item backgrounds ──────────────────── */
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
    text-decoration: none !important;
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
    box-shadow: 0 3px 10px rgba(217, 79, 61, 0.25) !important;
}

section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"] span,
section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"] p {
    font-size: 1rem !important;
    font-weight: inherit !important;
    color: inherit !important;
    text-transform: capitalize !important;
}

/* ── Bordered containers / cards ─────────────────────────────────────────── */
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

/* ── Metrics ─────────────────────────────────────────────────────────────── */
div[data-testid="stMetricLabel"] p {
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
    color: #A0897E !important;
}

div[data-testid="stMetricValue"] div {
    font-size: 1.9rem !important;
    font-weight: 800 !important;
    color: #1E2235 !important;
}

/* ── Divider ─────────────────────────────────────────────────────────────── */
hr { border-color: #F0D9CF !important; }

/* ── Tag chips ───────────────────────────────────────────────────────────── */
.tag-chip {
    display: inline-block;
    background: #FDE8DF;
    color: #D94F3D;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-weight: 600;
    margin: 2px 2px 0 0;
}

.action-desc {
    font-size: 0.75rem;
    color: #A0897E;
    text-align: center;
    margin-top: 0.25rem;
    line-height: 1.35;
}

.section-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #1E2235;
    margin-bottom: 0.6rem;
}

.recipe-meta {
    font-size: 0.82rem;
    color: #A0897E;
    margin: 0.25rem 0 0.4rem 0;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Initialise database
# ---------------------------------------------------------------------------

create_tables()


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_current_week_start() -> str:
    """Return ISO Monday date string for the current week."""
    today  = date.today()
    monday = today - timedelta(days=today.weekday())
    return monday.isoformat()


def get_todays_dinner(meal_plan: list[dict]) -> str | None:
    """Return tonight's dinner recipe title, or None if not planned."""
    today_name = date.today().strftime("%A")
    for slot in meal_plan:
        if slot["day"] == today_name and slot["meal_type"] == "Dinner":
            return slot.get("recipe_title")
    return None


def count_planned_meals(meal_plan: list[dict]) -> int:
    """Count non-empty meal slots in the plan."""
    return sum(1 for slot in meal_plan if slot.get("recipe_id") is not None)


def render_tag_chips(tags_str: str) -> str:
    """Convert comma-separated tags into HTML chip elements."""
    if not tags_str:
        return ""
    tags = [t.strip() for t in tags_str.split(",") if t.strip()][:4]
    return "".join(f'<span class="tag-chip">{tag}</span>' for tag in tags)


# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------

week_start      = get_current_week_start()
all_recipes     = get_all_recipes()
meal_plan       = get_meal_plan(week_start)

total_recipes   = len(all_recipes)
meals_planned   = count_planned_meals(meal_plan)
tonights_dinner = get_todays_dinner(meal_plan)

# Last 3 recipes, newest first
recent_recipes  = list(reversed(all_recipes[-3:])) if all_recipes else []


# ---------------------------------------------------------------------------
# Hero section
# ---------------------------------------------------------------------------

st.markdown("""
<div class="hero">
    <h1>Welcome back to your kitchen 👋</h1>
    <p>
        Plan your meals, manage your recipe collection, and generate
        your grocery list — all in one place.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Stat cards
# ---------------------------------------------------------------------------

st.markdown('<p class="section-title">📊 This Week at a Glance</p>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    with st.container(border=True):
        st.metric(
            label = "🥘  Total Recipes",
            value = total_recipes,
            help  = "Recipes saved in your collection.",
        )

with c2:
    with st.container(border=True):
        st.metric(
            label = "📅  Meals Planned This Week",
            value = meals_planned,
            help  = "Slots filled in your weekly meal planner.",
        )

with c3:
    with st.container(border=True):
        st.metric(
            label = "🌙  Tonight's Dinner",
            value = tonights_dinner or "Not planned yet",
            help  = "Dinner slot for today from your meal plan.",
        )

# Contextual guidance
if total_recipes == 0:
    st.info("👋 **Welcome!** You don't have any recipes yet. Add your first one below!", icon="💡")
elif meals_planned == 0:
    st.info("📅 **Tip:** Plan your meals this week to unlock your grocery list.", icon="💡")

st.markdown("<br>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Quick actions
# ---------------------------------------------------------------------------

st.markdown('<p class="section-title">⚡ Quick Actions</p>', unsafe_allow_html=True)

a1, a2, a3, a4, a5 = st.columns(5, gap="small")

with a1:
    with st.container(border=True):
        st.page_link("pages/add_recipe.py", label="➕ Add New Recipe", use_container_width=True)
        st.markdown('<p class="action-desc">Save a recipe to your collection</p>', unsafe_allow_html=True)

with a2:
    with st.container(border=True):
        st.page_link("pages/recipes.py", label="📚 Browse Recipes", use_container_width=True)
        st.markdown('<p class="action-desc">Search, view and manage recipes</p>', unsafe_allow_html=True)

with a3:
    with st.container(border=True):
        st.page_link("pages/meal_planner.py", label="📅 Meal Planner", use_container_width=True)
        st.markdown('<p class="action-desc">Plan breakfast, lunch & dinner</p>', unsafe_allow_html=True)

with a4:
    with st.container(border=True):
        st.page_link("pages/grocery_list.py", label="🛒 Grocery List", use_container_width=True)
        st.markdown('<p class="action-desc">Auto-generated from your meal plan</p>', unsafe_allow_html=True)

with a5:
    with st.container(border=True):
        st.page_link("pages/what_can_i_cook.py", label="🤔 What Can I Cook?", use_container_width=True)
        st.markdown('<p class="action-desc">Match recipes to your ingredients</p>', unsafe_allow_html=True)

st.divider()


# ---------------------------------------------------------------------------
# Recently added recipes
# ---------------------------------------------------------------------------

st.markdown('<p class="section-title">🕐 Recently Added</p>', unsafe_allow_html=True)

if not recent_recipes:
    st.markdown(
        '<p style="color:#A0897E; text-align:center; padding:1.5rem 0;">'
        '🍽️ No recipes yet — add your first recipe to get started!'
        '</p>',
        unsafe_allow_html=True,
    )
else:
    cols = st.columns(len(recent_recipes), gap="medium")

    for col, recipe in zip(cols, recent_recipes):
        with col:
            with st.container(border=True):
                st.markdown(f"### {recipe['title']}")
                st.markdown(
                    f'<p class="recipe-meta">'
                    f'🍴 {recipe.get("cuisine", "—")} &nbsp;·&nbsp; '
                    f'⏱ {recipe.get("cook_time", "?")} mins &nbsp;·&nbsp; '
                    f'👥 {recipe.get("servings", "?")} servings'
                    f'</p>',
                    unsafe_allow_html=True,
                )
                desc = recipe.get("description", "")
                if desc:
                    st.caption(desc[:85] + "…" if len(desc) > 85 else desc)
                chips = render_tag_chips(recipe.get("tags", ""))
                if chips:
                    st.markdown(chips, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)
st.divider()
st.caption(
    f"📆 Week of {week_start}  •  "
    f"🍽️ Recipe Manager & Meal Planner  •  "
    f"Built with Python & Streamlit"
)