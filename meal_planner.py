from global_styles import inject_global_styles
inject_global_styles()

import streamlit as st
from datetime import date, timedelta

from database import (
    get_all_recipes,
    save_meal_plan,
    get_meal_plan,
    clear_meal_slot,
)


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Weekly Meal Planner",
    page_icon="📅",
    layout="wide",
)


# ---------------------------------------------------------------------------
# CSS — minimal, targeted, stable selectors only
# ---------------------------------------------------------------------------

st.markdown("""
<style>

.block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1300px; }

/* Week nav label */
.week-label {
    text-align: center;
    font-size: 1.1rem;
    font-weight: 700;
    color: #1E2235;
    padding: 0.45rem 0;
}

/* Day header */
.day-header {
    text-align: center;
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #6B5B52;
    padding: 0.3rem 0 0.15rem 0;
}

.day-date {
    text-align: center;
    font-size: 0.75rem;
    color: #A0897E;
    margin-top: -0.1rem;
    margin-bottom: 0.3rem;
}

/* Today highlight badge */
.today-badge {
    text-align: center;
    font-size: 0.68rem;
    font-weight: 700;
    background: #D94F3D;
    color: #fff;
    border-radius: 20px;
    padding: 1px 8px;
    margin: 0 auto 0.3rem auto;
    width: fit-content;
}

/* Meal row label */
.meal-label {
    font-size: 0.82rem;
    font-weight: 700;
    color: #1E2235;
    padding: 0.6rem 0.3rem;
    text-align: right;
}

/* Meal type colour strips */
.row-breakfast { border-left: 4px solid #F6C94E; border-radius: 6px; padding: 0.25rem 0.4rem; background: #FFFDF0; margin-bottom: 0.15rem; }
.row-lunch     { border-left: 4px solid #4DB6AC; border-radius: 6px; padding: 0.25rem 0.4rem; background: #F0FAFA; margin-bottom: 0.15rem; }
.row-dinner    { border-left: 4px solid #D94F3D; border-radius: 6px; padding: 0.25rem 0.4rem; background: #FFF5F3; margin-bottom: 0.15rem; }

/* Summary panel */
.summary-box {
    background: #FFFAF7;
    border: 1.5px solid #F0D9CF;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-top: 0.5rem;
}

.summary-title {
    font-size: 0.9rem;
    font-weight: 700;
    color: #1E2235;
    margin-bottom: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.summary-stat {
    font-size: 1.5rem;
    font-weight: 800;
    color: #D94F3D;
    line-height: 1.1;
}

.summary-sub {
    font-size: 0.75rem;
    color: #A0897E;
    margin-bottom: 0.9rem;
}

/* Sidebar */
section[data-testid="stSidebar"] { background-color: #F8EDE5 !important; border-right: 1px solid #F0D9CF !important; }
section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"] {
    display: block !important; background-color: #FFFAF7 !important;
    border: 1px solid #F0D9CF !important; border-radius: 10px !important;
    margin: 0.3rem 0.5rem !important; padding: 0.6rem 1rem !important;
    font-weight: 500 !important; color: #1E2235 !important;
    transition: all 0.15s ease !important;
}
section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"]:hover {
    background-color: #FDE8DF !important; border-color: #D94F3D !important; color: #D94F3D !important;
}
section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"][aria-current="page"] {
    background-color: #D94F3D !important; border-color: #D94F3D !important; color: #FFFFFF !important; font-weight: 700 !important;
}

hr { border-color: #F0D9CF !important; }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DAYS       = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MEAL_TYPES = ["Breakfast", "Lunch", "Dinner"]
NO_PLAN    = "— Not Planned —"

MEAL_ROW_CLASS = {
    "Breakfast": "row-breakfast",
    "Lunch":     "row-lunch",
    "Dinner":    "row-dinner",
}

MEAL_EMOJI = {
    "Breakfast": "🌅",
    "Lunch":     "☀️",
    "Dinner":    "🌙",
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_monday(ref: date) -> date:
    """Return the Monday of the week containing ref."""
    return ref - timedelta(days=ref.weekday())


def get_week_dates(monday: date) -> list[date]:
    """Return the 7 dates of the week starting from monday."""
    return [monday + timedelta(days=i) for i in range(7)]


def format_week_label(monday: date) -> str:
    sunday = monday + timedelta(days=6)
    return f"{monday.strftime('%d %b')} – {sunday.strftime('%d %b %Y')}"


def build_meal_lookup(meal_plan: list[dict]) -> dict:
    """
    Convert flat meal plan list → nested dict for O(1) lookups.
    Structure: { day: { meal_type: recipe_title } }
    """
    lookup: dict[str, dict[str, str]] = {}
    for slot in meal_plan:
        day       = slot["day"]
        meal_type = slot["meal_type"]
        title     = slot.get("recipe_title") or NO_PLAN
        lookup.setdefault(day, {})[meal_type] = title
    return lookup


def build_recipe_options(recipes: list[dict]) -> list[str]:
    return [NO_PLAN] + [r["title"] for r in recipes]


def init_week_state() -> None:
    """Initialise selected_monday in session state once."""
    if "selected_monday" not in st.session_state:
        st.session_state.selected_monday = get_monday(date.today())


def clear_planner_selections() -> None:
    """Remove all selectbox session state keys so they reload for a new week."""
    for day in DAYS:
        for meal_type in MEAL_TYPES:
            key = f"plan_{day}_{meal_type}"
            st.session_state.pop(key, None)


def count_planned(meal_lookup: dict) -> int:
    total = 0
    for day in DAYS:
        for mt in MEAL_TYPES:
            if meal_lookup.get(day, {}).get(mt, NO_PLAN) != NO_PLAN:
                total += 1
    return total


# ---------------------------------------------------------------------------
# Session state boot
# ---------------------------------------------------------------------------

init_week_state()


# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------

all_recipes    = get_all_recipes()
recipe_options = build_recipe_options(all_recipes)
week_start     = st.session_state.selected_monday.isoformat()
meal_plan      = get_meal_plan(week_start)
meal_lookup    = build_meal_lookup(meal_plan)
week_dates     = get_week_dates(st.session_state.selected_monday)
today          = date.today()

total_slots   = len(DAYS) * len(MEAL_TYPES)   # 21
planned_count = count_planned(meal_lookup)
remaining     = total_slots - planned_count


# ---------------------------------------------------------------------------
# Page header
# ---------------------------------------------------------------------------

st.title("📅 Weekly Meal Planner")
st.markdown(
    '<p style="color:#A0897E; margin-top:-0.4rem; margin-bottom:1rem; font-size:0.97rem;">'
    "Plan your meals for the week — then save and head to the Grocery List."
    "</p>",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Empty state — no recipes
# ---------------------------------------------------------------------------

if not all_recipes:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(
            '<p style="text-align:center; color:#A0897E; padding:1rem 0;">'
            "🍽️ You need some recipes before planning meals."
            "</p>",
            unsafe_allow_html=True,
        )
        _, ctr, _ = st.columns([1, 2, 1])
        with ctr:
            st.page_link("pages/add_recipe.py", label="➕ Add Your First Recipe", use_container_width=True)
    st.stop()


# ---------------------------------------------------------------------------
# Main layout: planner (left/center) + summary panel (right)
# ---------------------------------------------------------------------------


# ── Stats + quick links (above planner) ─────────────────────────────────────

m1, m2, m3, _spacer, link1_col, link2_col = st.columns([1, 1, 1, 2, 1.3, 1.3], gap="small")

with m1:
    with st.container(border=True):
        st.metric(label="📊 Planned", value=planned_count, help="Meal slots filled this week")

with m2:
    with st.container(border=True):
        st.metric(label="⬜ Remaining", value=remaining, help="Empty slots this week")

with m3:
    with st.container(border=True):
        st.metric(label="📅 Total Slots", value=total_slots)

with link1_col:
    st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)
    st.page_link("pages/grocery_list.py", label="🛒 Grocery List", use_container_width=True)

with link2_col:
    st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)
    st.page_link("pages/add_recipe.py", label="➕ Add Recipe", use_container_width=True)

st.markdown("<div style='margin-bottom:0.6rem;'></div>", unsafe_allow_html=True)


# ── Week navigation ───────────────────────────────────────────────────────
nav_left, nav_center, nav_right = st.columns([1, 3, 1])

with nav_left:
    if st.button("⬅️ Prev Week", use_container_width=True):
        st.session_state.selected_monday -= timedelta(weeks=1)
        clear_planner_selections()
        st.rerun()

with nav_center:
    st.markdown(
        f'<div class="week-label">📆 {format_week_label(st.session_state.selected_monday)}</div>',
        unsafe_allow_html=True,
    )

with nav_right:
    if st.button("Next Week ➡️", use_container_width=True):
        st.session_state.selected_monday += timedelta(weeks=1)
        clear_planner_selections()
        st.rerun()

st.markdown("<div style='margin-bottom:0.6rem;'></div>", unsafe_allow_html=True)

# ── Refresh data after potential week navigation ───────────────────────────
week_start   = st.session_state.selected_monday.isoformat()
meal_plan    = get_meal_plan(week_start)
meal_lookup  = build_meal_lookup(meal_plan)
week_dates   = get_week_dates(st.session_state.selected_monday)

# ── Day header row ────────────────────────────────────────────────────────
# 1 label col + 7 day cols
header_cols = st.columns([0.8] + [1] * 7)
header_cols[0].markdown("")   # spacer for row labels

for i, (day, day_date) in enumerate(zip(DAYS, week_dates)):
    is_today = (day_date == today)
    with header_cols[i + 1]:
        if is_today:
            st.markdown(f'<div class="day-header" style="color:#D94F3D;">{day[:3]}</div>', unsafe_allow_html=True)
            st.markdown('<div class="today-badge">TODAY</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="day-header">{day[:3]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="day-date">{day_date.strftime("%-d %b")}</div>', unsafe_allow_html=True)

st.markdown("<hr style='margin:0.4rem 0 0.6rem 0;'>", unsafe_allow_html=True)

# ── Meal rows ─────────────────────────────────────────────────────────────
for meal_type in MEAL_TYPES:
    row_cols = st.columns([0.8] + [1] * 7)

    # Row label
    with row_cols[0]:
        st.markdown(
            f'<div class="meal-label">{MEAL_EMOJI[meal_type]}<br>{meal_type}</div>',
            unsafe_allow_html=True,
        )

    # One selectbox per day cell
    for i, day in enumerate(DAYS):
        saved_title  = meal_lookup.get(day, {}).get(meal_type, NO_PLAN)
        select_key   = f"plan_{day}_{meal_type}"
        default_idx  = recipe_options.index(saved_title) if saved_title in recipe_options else 0
        with row_cols[i + 1]:
            st.selectbox(
                label            = f"{day} {meal_type}",
                options          = recipe_options,
                index            = default_idx,
                key              = select_key,
                label_visibility = "collapsed",
            )

    st.markdown("<div style='margin-bottom:0.3rem;'></div>", unsafe_allow_html=True)

# ── Save button ───────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)
st.divider()

save_col, _ = st.columns([2, 5])
with save_col:
    save_clicked = st.button("💾 Save Plan", type="primary", use_container_width=True)

if save_clicked:
    saved_count   = 0
    cleared_count = 0

    for day in DAYS:
        for meal_type in MEAL_TYPES:
            key            = f"plan_{day}_{meal_type}"
            selected_title = st.session_state.get(key, NO_PLAN)

            if selected_title == NO_PLAN:
                clear_meal_slot(week_start, day, meal_type)
                cleared_count += 1
            else:
                matching = [r for r in all_recipes if r["title"] == selected_title]
                if matching:
                    save_meal_plan(week_start, day, meal_type, matching[0]["id"])
                    saved_count += 1

    # Refresh summary counts after save
    meal_plan    = get_meal_plan(week_start)
    meal_lookup  = build_meal_lookup(meal_plan)
    planned_count = count_planned(meal_lookup)

    st.success(f"✅ Plan saved! {saved_count} meal(s) planned this week.")

# Footer tip
st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)
st.caption("💡 Tip: After saving, visit the Grocery List to see all ingredients for this week's meals.")