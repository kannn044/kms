"""
Global CSS Design System for the Knowledge Management System.
Inject via inject_global_css() at the start of every page render.
"""
import streamlit as st

# Color palette
COLORS = {
    "bg_primary": "#0F1724",
    "bg_secondary": "#1A2332",
    "bg_card": "#1E2A3A",
    "bg_card_hover": "#243347",
    "bg_input": "#162030",
    "border": "#2A3A4E",
    "border_focus": "#6C63FF",
    "accent_primary": "#6C63FF",
    "accent_secondary": "#00D4AA",
    "accent_warning": "#FFB547",
    "accent_danger": "#FF6B6B",
    "accent_info": "#54A0FF",
    "text_primary": "#E8ECF1",
    "text_secondary": "#8899AA",
    "text_muted": "#5A6B7D",
    "gradient_start": "#6C63FF",
    "gradient_end": "#00D4AA",
}


def get_global_css():
    """Return the complete global CSS theme."""
    return f"""
    <style>
    /* ===== Google Font ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ===== Root & Global Reset ===== */
    html, body, [data-testid="stAppViewContainer"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}

    .stApp {{
        background: linear-gradient(135deg, {COLORS['bg_primary']} 0%, #141E30 50%, {COLORS['bg_primary']} 100%) !important;
    }}

    /* ===== Sidebar ===== */
    [data-testid="stSidebar"] {{
        background: {COLORS['bg_secondary']} !important;
        border-right: 1px solid {COLORS['border']} !important;
    }}

    [data-testid="stSidebar"] * {{
        font-family: 'Inter', sans-serif !important;
    }}

    /* ===== Animations ===== */
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}

    @keyframes shimmer {{
        0% {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
    }}

    @keyframes pulseGlow {{
        0%, 100% {{ box-shadow: 0 0 20px rgba(108, 99, 255, 0.2); }}
        50% {{ box-shadow: 0 0 40px rgba(108, 99, 255, 0.4); }}
    }}

    /* ===== Glass Card ===== */
    .glass-card {{
        background: linear-gradient(145deg, rgba(30, 42, 58, 0.8), rgba(26, 35, 50, 0.6)) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(108, 99, 255, 0.15);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        animation: fadeInUp 0.5s ease-out;
        transition: all 0.3s ease;
    }}

    .glass-card:hover {{
        border-color: rgba(108, 99, 255, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
    }}

    /* ===== Page Header ===== */
    .page-header {{
        background: linear-gradient(135deg, {COLORS['accent_primary']}22, {COLORS['accent_secondary']}22);
        border: 1px solid {COLORS['border']};
        border-radius: 20px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        animation: fadeInUp 0.4s ease-out;
    }}

    .page-header h1 {{
        background: linear-gradient(135deg, {COLORS['accent_primary']}, {COLORS['accent_secondary']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
    }}

    .page-header p {{
        color: {COLORS['text_secondary']};
        font-size: 1rem;
        margin: 0;
    }}

    /* ===== Metric Card ===== */
    .metric-card {{
        background: linear-gradient(145deg, {COLORS['bg_card']}, {COLORS['bg_secondary']});
        border: 1px solid {COLORS['border']};
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease-out;
    }}

    .metric-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
        border-color: rgba(108, 99, 255, 0.3);
    }}

    .metric-icon {{
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }}

    .metric-value {{
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, {COLORS['accent_primary']}, {COLORS['accent_secondary']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.25rem 0;
    }}

    .metric-label {{
        color: {COLORS['text_secondary']};
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    /* ===== Knowledge Card ===== */
    .knowledge-card {{
        background: {COLORS['bg_card']};
        border: 1px solid {COLORS['border']};
        border-radius: 14px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 0.75rem;
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease-out;
    }}

    .knowledge-card:hover {{
        border-color: {COLORS['accent_primary']}44;
        background: {COLORS['bg_card_hover']};
        transform: translateX(4px);
    }}

    .knowledge-card-title {{
        color: {COLORS['text_primary']};
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }}

    .knowledge-card-meta {{
        color: {COLORS['text_secondary']};
        font-size: 0.8rem;
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
    }}

    /* ===== Badge / Pill ===== */
    .badge {{
        display: inline-block;
        padding: 0.2rem 0.7rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.3px;
    }}

    .badge-category {{
        background: {COLORS['accent_primary']}22;
        color: {COLORS['accent_primary']};
        border: 1px solid {COLORS['accent_primary']}44;
    }}

    .badge-tag {{
        background: {COLORS['accent_secondary']}22;
        color: {COLORS['accent_secondary']};
        border: 1px solid {COLORS['accent_secondary']}44;
    }}

    .badge-approved {{
        background: #00D4AA22;
        color: #00D4AA;
        border: 1px solid #00D4AA44;
    }}

    .badge-pending {{
        background: #FFB54722;
        color: #FFB547;
        border: 1px solid #FFB54744;
    }}

    .badge-rejected {{
        background: #FF6B6B22;
        color: #FF6B6B;
        border: 1px solid #FF6B6B44;
    }}

    .badge-admin {{
        background: {COLORS['accent_primary']}22;
        color: {COLORS['accent_primary']};
        border: 1px solid {COLORS['accent_primary']}44;
    }}

    .badge-user {{
        background: {COLORS['accent_info']}22;
        color: {COLORS['accent_info']};
        border: 1px solid {COLORS['accent_info']}44;
    }}

    /* ===== Sidebar Styles ===== */
    .sidebar-profile {{
        text-align: center;
        padding: 1.5rem 1rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid {COLORS['border']};
    }}

    .sidebar-avatar {{
        width: 64px;
        height: 64px;
        border-radius: 50%;
        background: linear-gradient(135deg, {COLORS['accent_primary']}, {COLORS['accent_secondary']});
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 0.75rem auto;
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        box-shadow: 0 4px 15px rgba(108, 99, 255, 0.3);
    }}

    .sidebar-name {{
        color: {COLORS['text_primary']};
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }}

    .sidebar-role {{
        display: inline-block;
        padding: 0.15rem 0.6rem;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    /* ===== User Card (Admin) ===== */
    .user-card {{
        background: {COLORS['bg_card']};
        border: 1px solid {COLORS['border']};
        border-radius: 14px;
        padding: 1.25rem;
        margin-bottom: 0.75rem;
        transition: all 0.3s ease;
        animation: fadeInUp 0.4s ease-out;
    }}

    .user-card:hover {{
        border-color: {COLORS['accent_primary']}44;
        background: {COLORS['bg_card_hover']};
    }}

    /* ===== Profile Header ===== */
    .profile-header {{
        background: linear-gradient(135deg, {COLORS['accent_primary']}18, {COLORS['accent_secondary']}18);
        border: 1px solid {COLORS['border']};
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 1.5rem;
        animation: fadeInUp 0.4s ease-out;
    }}

    .profile-avatar-large {{
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(135deg, {COLORS['accent_primary']}, {COLORS['accent_secondary']});
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem auto;
        font-size: 2rem;
        font-weight: 700;
        color: white;
        box-shadow: 0 6px 20px rgba(108, 99, 255, 0.35);
    }}

    /* ===== Streamlit Component Overrides ===== */
    /* Form inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {{
        background-color: {COLORS['bg_input']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 10px !important;
        color: {COLORS['text_primary']} !important;
        font-family: 'Inter', sans-serif !important;
    }}

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: {COLORS['accent_primary']} !important;
        box-shadow: 0 0 0 2px {COLORS['accent_primary']}33 !important;
    }}

    /* Primary buttons */
    .stButton > button[kind="primary"],
    .stFormSubmitButton > button {{
        background: linear-gradient(135deg, {COLORS['accent_primary']}, #5A52E0) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(108, 99, 255, 0.25) !important;
    }}

    .stButton > button[kind="primary"]:hover,
    .stFormSubmitButton > button:hover {{
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(108, 99, 255, 0.4) !important;
    }}

    /* Secondary buttons */
    .stButton > button[kind="secondary"] {{
        background: transparent !important;
        color: {COLORS['text_secondary']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 10px !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
    }}

    .stButton > button[kind="secondary"]:hover {{
        border-color: {COLORS['accent_primary']} !important;
        color: {COLORS['accent_primary']} !important;
        background: {COLORS['accent_primary']}11 !important;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background: {COLORS['bg_card']} !important;
        border-radius: 12px !important;
        padding: 4px !important;
        gap: 4px !important;
        border: 1px solid {COLORS['border']} !important;
    }}

    .stTabs [data-baseweb="tab"] {{
        border-radius: 10px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        color: {COLORS['text_secondary']} !important;
    }}

    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {COLORS['accent_primary']}, #5A52E0) !important;
        color: white !important;
    }}

    /* Expander */
    .streamlit-expanderHeader {{
        background: {COLORS['bg_card']} !important;
        border: 1px solid {COLORS['border']} !important;
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
    }}

    /* Dataframe */
    .stDataFrame {{
        border: 1px solid {COLORS['border']} !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }}

    /* Metric override */
    [data-testid="stMetric"] {{
        background: {COLORS['bg_card']};
        border: 1px solid {COLORS['border']};
        border-radius: 14px;
        padding: 1rem;
        transition: all 0.3s ease;
    }}

    [data-testid="stMetric"]:hover {{
        border-color: {COLORS['accent_primary']}44;
        transform: translateY(-2px);
    }}

    [data-testid="stMetricValue"] {{
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
    }}

    /* Success / Error / Warning / Info */
    .stSuccess, .stAlert {{
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
    }}

    /* Divider */
    .section-divider {{
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, {COLORS['border']}, transparent);
        margin: 1.5rem 0;
    }}

    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 6px;
        height: 6px;
    }}

    ::-webkit-scrollbar-track {{
        background: {COLORS['bg_primary']};
    }}

    ::-webkit-scrollbar-thumb {{
        background: {COLORS['border']};
        border-radius: 3px;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: {COLORS['text_muted']};
    }}

    /* ===== Similarity Score Bar ===== */
    .score-bar-container {{
        background: {COLORS['bg_input']};
        border-radius: 8px;
        height: 8px;
        margin: 0.5rem 0;
        overflow: hidden;
    }}

    .score-bar {{
        height: 100%;
        border-radius: 8px;
        background: linear-gradient(90deg, {COLORS['accent_primary']}, {COLORS['accent_secondary']});
        transition: width 0.6s ease;
    }}

    /* ===== Empty State ===== */
    .empty-state {{
        text-align: center;
        padding: 3rem 2rem;
        color: {COLORS['text_muted']};
    }}

    .empty-state-icon {{
        font-size: 3rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }}

    .empty-state-text {{
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        color: {COLORS['text_secondary']};
    }}

    .empty-state-sub {{
        font-size: 0.85rem;
        color: {COLORS['text_muted']};
    }}

    </style>
    """


def inject_global_css():
    """Inject the global CSS into the current Streamlit page."""
    st.markdown(get_global_css(), unsafe_allow_html=True)


def render_page_header(title, subtitle="", icon=""):
    """Render a styled page header with gradient text."""
    st.markdown(f"""
    <div class="page-header">
        <h1>{icon} {title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(icon, value, label, col_class=""):
    """Render a single styled metric card."""
    return f"""
    <div class="metric-card {col_class}">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """


def render_knowledge_card(title, category, tags, date, author, preview=""):
    """Render a styled knowledge item card."""
    tags_html = ""
    if tags:
        for tag in str(tags).split(","):
            tag = tag.strip()
            if tag:
                tags_html += f'<span class="badge badge-tag">{tag}</span> '

    return f"""
    <div class="knowledge-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div class="knowledge-card-title">{title}</div>
            <span class="badge badge-category">{category}</span>
        </div>
        {f'<div style="color: #8899AA; font-size: 0.9rem; margin: 0.5rem 0;">{preview}</div>' if preview else ''}
        <div style="margin: 0.5rem 0;">{tags_html}</div>
        <div class="knowledge-card-meta">
            <span>📅 {date}</span>
            <span>👤 {author}</span>
        </div>
    </div>
    """


def render_badge(text, badge_type="category"):
    """Render a styled badge/pill."""
    return f'<span class="badge badge-{badge_type}">{text}</span>'


def render_empty_state(icon, title, subtitle=""):
    """Render an empty state placeholder."""
    return f"""
    <div class="empty-state">
        <div class="empty-state-icon">{icon}</div>
        <div class="empty-state-text">{title}</div>
        <div class="empty-state-sub">{subtitle}</div>
    </div>
    """


def render_score_bar(score_pct):
    """Render a similarity score bar."""
    return f"""
    <div class="score-bar-container">
        <div class="score-bar" style="width: {score_pct}%;"></div>
    </div>
    """
