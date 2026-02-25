import streamlit as st


def inject_global_styles() -> None:
    """
    Inject global CSS into the Streamlit app.

    Improves:
        - Button and page link appearance (dark, high-contrast, premium feel)
        - Container / card polish (soft shadow, warmer background, smooth border)
        - General spacing and typography refinements
    """
    st.markdown("""
    <style>

    /* ── Page padding ─────────────────────────────────────────────────────── */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ── Buttons — dark coral, white text, premium feel ───────────────────── */

    /* Primary st.button */
    div[data-testid="stButton"] > button[kind="primary"],
    div[data-testid="stButton"] > button {
        background-color: #2D3142;
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
        font-size: 0.9rem;
        letter-spacing: 0.02em;
        transition: background-color 0.2s ease, transform 0.15s ease, box-shadow 0.15s ease;
        box-shadow: 0 2px 6px rgba(45, 49, 66, 0.18);
        cursor: pointer;
    }

    div[data-testid="stButton"] > button:hover {
        background-color: #D94F3D;
        transform: translateY(-2px);
        box-shadow: 0 5px 14px rgba(217, 79, 61, 0.28);
    }

    div[data-testid="stButton"] > button:active {
        transform: translateY(0px);
        box-shadow: 0 2px 6px rgba(45, 49, 66, 0.18);
    }

    /* Page links — match button style */
    div[data-testid="stPageLink"] > a {
        background-color: #2D3142 !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        text-decoration: none !important;
        display: block !important;
        text-align: center !important;
        transition: background-color 0.2s ease, transform 0.15s ease, box-shadow 0.15s ease !important;
        box-shadow: 0 2px 6px rgba(45, 49, 66, 0.18) !important;
        border: none !important;
    }

    div[data-testid="stPageLink"] > a:hover {
        background-color: #D94F3D !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 14px rgba(217, 79, 61, 0.28) !important;
        color: #FFFFFF !important;
    }

    /* ── Containers / Cards — subtle warmth and depth ─────────────────────── */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px !important;
        border: 1px solid #EAD9CC !important;
        background-color: #FFFAF7 !important;
        box-shadow: 0 2px 10px rgba(45, 49, 66, 0.07) !important;
        transition: box-shadow 0.2s ease !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 4px 18px rgba(45, 49, 66, 0.11) !important;
    }

    /* ── Metric cards — tighten internal spacing ──────────────────────────── */
    div[data-testid="stMetric"] {
        padding: 0.4rem 0.2rem;
    }

    div[data-testid="stMetricLabel"] p {
        font-size: 0.78rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        color: #8C8FA8 !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        color: #1E2235 !important;
    }

    /* ── Sidebar — slightly warmer, cleaner feel ──────────────────────────── */
    section[data-testid="stSidebar"] {
        background-color: #F5EBE0;
        border-right: 1px solid #EAD9CC;
    }

    /* ── Dividers — softer tone ───────────────────────────────────────────── */
    hr {
        border-color: #EAD9CC !important;
        margin: 1.2rem 0 !important;
    }

    /* ── Expanders — rounded, warm borders ───────────────────────────────── */
    details[data-testid="stExpander"] {
        border-radius: 12px !important;
        border: 1px solid #EAD9CC !important;
        background-color: #FFFAF7 !important;
    }

    /* ── Input fields — warmer feel ──────────────────────────────────────── */
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stNumberInput"] input {
        border-radius: 8px !important;
        border: 1.5px solid #DDD0C4 !important;
        background-color: #FFFDF9 !important;
    }

    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stTextArea"] textarea:focus,
    div[data-testid="stNumberInput"] input:focus {
        border-color: #D94F3D !important;
        box-shadow: 0 0 0 3px rgba(217, 79, 61, 0.12) !important;
    }

    /* ── Success / info / warning alerts — rounded ───────────────────────── */
    div[data-testid="stAlert"] {
        border-radius: 10px !important;
    }

    </style>
    """, unsafe_allow_html=True)