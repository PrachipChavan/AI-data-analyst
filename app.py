"""
AI Data Analyst — Agentic AI powered by Groq + LLaMA 3.3
Main Streamlit application
"""

# ── Force UTF-8 on Windows (must be before all other imports) ───────────────────────────
import sys
import os
os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"
import io as _io
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import streamlit as st
import pandas as pd
import plotly.io as pio
import json
import io
from dotenv import load_dotenv

from agent.controller import AgentController
from utils.report import generate_report, get_quick_stats

load_dotenv()

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg-primary: #0a0a14;
    --bg-secondary: #0f0f1e;
    --bg-card: #12122a;
    --bg-glass: rgba(255,255,255,0.04);
    --border: rgba(139,92,246,0.2);
    --border-subtle: rgba(255,255,255,0.06);
    --purple: #8b5cf6;
    --purple-light: #a78bfa;
    --purple-glow: rgba(139,92,246,0.15);
    --cyan: #06b6d4;
    --green: #10b981;
    --red: #ef4444;
    --orange: #f59e0b;
    --text-primary: #ffffff;
    --text-secondary: #e2e8f0;
    --text-muted: #cbd5e1;
}

/* ── Global white text reset ── */
html, body { color: #ffffff !important; }

/* All Streamlit text elements — exclude icon spans */
.stApp p, .stApp div, .stApp label,
.stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown h1,
.stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] em,
.stText, .element-container p {
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
}

/* Sidebar: target specific text nodes, NOT icon spans */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stButton > button {
    color: #ffffff !important;
}

/* Widget labels */
.stTextInput label, .stTextArea label, .stSelectbox label,
.stFileUploader label, .stSlider label, .stRadio label,
.stCheckbox label, .stNumberInput label, .stDateInput label,
[data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p {
    color: #ffffff !important;
    font-weight: 500 !important;
}

/* Expander — only target text, NOT the icon glyph span */
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary div,
.streamlit-expanderHeader p {
    color: #ffffff !important;
}
/* Preserve Material Icons rendering in expander */
[data-testid="stExpander"] summary .material-icons,
[data-testid="stExpander"] summary [data-testid="stExpanderToggleIcon"] {
    font-family: 'Material Icons' !important;
    color: #a78bfa !important;
}

/* Alert / notification text */
.stSuccess, .stSuccess p, .stSuccess div,
.stInfo, .stInfo p, .stInfo div,
.stWarning, .stWarning p, .stWarning div,
.stError, .stError p, .stError div {
    color: #ffffff !important;
}

/* Dataframe text */
[data-testid="stDataFrame"] * { color: #ffffff !important; }

/* Button text */
.stButton > button, .stButton > button span,
.stDownloadButton > button, .stDownloadButton > button span {
    color: #ffffff !important;
}

/* Caption / helper text */
.stCaption, .stCaption p { color: #cbd5e1 !important; }

/* Tooltip */
.stTooltipIcon { color: #a78bfa !important; }

/* App background */
.stApp {
    background: linear-gradient(135deg, #0a0a14 0%, #0d0d22 50%, #0a0a14 100%) !important;
}

/* Hide default header */
header[data-testid="stHeader"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border-subtle);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c0c1e 0%, #0a0a18 100%) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] > div {
    padding: 1.5rem 1rem;
}

/* Stat cards */
.stat-card {
    background: var(--bg-glass);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}
.stat-card:hover {
    border-color: var(--purple);
    box-shadow: 0 0 20px var(--purple-glow);
    transform: translateY(-2px);
}
.stat-number {
    font-size: 1.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--purple-light), var(--cyan));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.stat-label {
    font-size: 0.72rem;
    color: #cbd5e1 !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.2rem;
}

/* Chat messages */
.chat-msg-user {
    background: linear-gradient(135deg, rgba(139,92,246,0.15), rgba(139,92,246,0.08));
    border: 1px solid rgba(139,92,246,0.3);
    border-radius: 14px 14px 4px 14px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
    color: var(--text-primary);
    font-size: 0.95rem;
}
.chat-msg-assistant {
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    border-radius: 14px 14px 14px 4px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
    color: var(--text-primary);
    font-size: 0.95rem;
    line-height: 1.7;
}

/* Agent trace steps */
.trace-step {
    font-size: 0.82rem;
    padding: 0.5rem 0.8rem;
    border-radius: 8px;
    margin: 0.25rem 0;
    border-left: 3px solid;
    font-family: 'Inter', monospace;
}
.trace-thought {
    background: rgba(139,92,246,0.08);
    border-left-color: var(--purple);
    color: var(--purple-light);
}
.trace-tool {
    background: rgba(6,182,212,0.08);
    border-left-color: var(--cyan);
    color: var(--cyan);
}
.trace-obs {
    background: rgba(16,185,129,0.06);
    border-left-color: var(--green);
    color: #6ee7b7;
}
.trace-error {
    background: rgba(239,68,68,0.08);
    border-left-color: var(--red);
    color: #fca5a5;
}

/* Section headers */
.section-header {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #cbd5e1 !important;
    margin: 1.2rem 0 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border-subtle);
}

/* Hero title */
.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa 0%, #06b6d4 50%, #10b981 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.3rem;
    letter-spacing: -0.02em;
}
.hero-subtitle {
    color: #cbd5e1 !important;
    font-size: 1rem;
    margin-bottom: 1.5rem;
}

/* Upload zone */
.upload-zone {
    border: 2px dashed var(--border);
    border-radius: 16px;
    padding: 2.5rem;
    text-align: center;
    background: var(--bg-glass);
    transition: all 0.3s;
}
.upload-zone:hover {
    border-color: var(--purple);
    background: var(--purple-glow);
}

/* Quick question pills */
.pill-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin: 0.6rem 0;
}
.pill {
    background: rgba(139,92,246,0.1);
    border: 1px solid rgba(139,92,246,0.3);
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
    font-size: 0.8rem;
    color: var(--purple-light);
    cursor: pointer;
    transition: all 0.2s;
    display: inline-block;
}
.pill:hover {
    background: rgba(139,92,246,0.25);
    border-color: var(--purple);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #6d28d9) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.5rem 1.2rem !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(124,58,237,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(124,58,237,0.5) !important;
}

/* ── Input fields: dark background + white text ── */
.stTextInput input,
.stTextInput input[type="text"],
.stTextInput input[type="password"],
.stTextArea textarea,
.stNumberInput input,
.stDateInput input,
[data-testid="stTextInput"] input,
[data-testid="stTextInputRootElement"] input,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea,
input, textarea {
    background: #1a1a2e !important;
    background-color: #1a1a2e !important;
    border: 1px solid rgba(139,92,246,0.4) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    font-size: 0.95rem !important;
    caret-color: #a78bfa !important;
}

/* Input wrapper containers */
[data-baseweb="input"],
[data-baseweb="base-input"],
[data-testid="stTextInputRootElement"],
.stTextInput > div,
.stTextInput > div > div {
    background: #1a1a2e !important;
    background-color: #1a1a2e !important;
    border-radius: 10px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
[data-baseweb="input"]:focus-within {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 2px rgba(139,92,246,0.25) !important;
    outline: none !important;
}

/* ── File Uploader: dark background + white text ── */
[data-testid="stFileUploader"],
[data-testid="stFileUploader"] > div,
[data-testid="stFileUploaderDropzone"],
[data-testid="stFileUploaderDropzone"] > div,
[data-baseweb="file-uploader"] {
    background: #1a1a2e !important;
    background-color: #1a1a2e !important;
    border: 2px dashed rgba(139,92,246,0.4) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
}

/* File uploader inner text */
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] p,
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] button,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] small {
    color: #ffffff !important;
}

/* Expander */
.streamlit-expanderHeader,
[data-testid="stExpander"] details summary {
    background: var(--bg-glass) !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    font-size: 0.85rem !important;
}

/* Divider */
hr {
    border: none !important;
    border-top: 1px solid var(--border-subtle) !important;
    margin: 1.5rem 0 !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--purple); border-radius: 2px; }

/* Spinner */
.stSpinner > div { border-top-color: var(--purple) !important; }

/* Success / Info */
.stSuccess { background: rgba(16,185,129,0.1) !important; border-color: var(--green) !important; color: #ffffff !important; }
.stInfo { background: rgba(6,182,212,0.1) !important; border-color: var(--cyan) !important; color: #ffffff !important; }
.stWarning { background: rgba(245,158,11,0.1) !important; border-color: var(--orange) !important; color: #ffffff !important; }
.stError { background: rgba(239,68,68,0.1) !important; border-color: var(--red) !important; color: #ffffff !important; }

/* Sidebar info text override */
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #ffffff !important; }

/* Input placeholder text */
::placeholder { color: #94a3b8 !important; opacity: 1 !important; }
:-ms-input-placeholder { color: #94a3b8 !important; }
::-ms-input-placeholder { color: #94a3b8 !important; }
</style>
""", unsafe_allow_html=True)


# ── Session State Init ─────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "agent": None,
        "df": None,
        "df_name": "",
        "messages": [],   # [{role, content, traces, charts}]
        "api_key_set": False,
        "trace_log": [],
        "pending_question": None,
        "last_api_key": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ── Helper: Load DataFrame ─────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_df(file_bytes: bytes, filename: str) -> pd.DataFrame:
    if filename.endswith(".csv"):
        return pd.read_csv(io.BytesIO(file_bytes))
    elif filename.endswith((".xlsx", ".xls")):
        return pd.read_excel(io.BytesIO(file_bytes))
    elif filename.endswith(".json"):
        return pd.read_json(io.BytesIO(file_bytes))
    else:
        raise ValueError(f"Unsupported format: {filename}")


# ── Helper: Render Chart ───────────────────────────────────────────────────────
def render_chart(chart_json: str):
    try:
        fig = pio.from_json(chart_json)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True})
    except Exception as e:
        st.warning(f"Could not render chart: {e}")


# ── Helper: Stat Cards ─────────────────────────────────────────────────────────
def render_stat_cards(stats: dict):
    cols = st.columns(5)
    items = [
        (stats["rows"], "Rows"),
        (stats["columns"], "Columns"),
        (stats["numeric_cols"], "Numeric"),
        (stats["categorical_cols"], "Categorical"),
        (f"{stats['missing_pct']}%", "Missing"),
    ]
    for col, (val, label) in zip(cols, items):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{val:,}" if isinstance(val, int) else "{val}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)


def render_stat_cards_fixed(stats: dict):
    cols = st.columns(5)
    items = [
        (f"{stats['rows']:,}", "Rows"),
        (str(stats["columns"]), "Columns"),
        (str(stats["numeric_cols"]), "Numeric"),
        (str(stats["categorical_cols"]), "Categorical"),
        (f"{stats['missing_pct']}%", "Missing Data"),
    ]
    for col, (val, label) in zip(cols, items):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{val}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)


# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 0.5rem 0 1.5rem;">
        <div style="font-size:2.5rem; margin-bottom:0.3rem;">🤖</div>
        <div style="font-size:1.1rem; font-weight:700; color:#a78bfa;">AI Data Analyst</div>
        <div style="font-size:0.72rem; color:#64748b; margin-top:0.2rem;">Powered by Groq · LLaMA 3.3</div>
    </div>
    """, unsafe_allow_html=True)

    # ── API Key ──────────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">⚡ Configuration</div>', unsafe_allow_html=True)
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        value=os.getenv("GROQ_API_KEY", ""),
        placeholder="gsk_...",
        help="Get your free API key at console.groq.com",
    )

    if api_key and api_key.strip():
        # Recreate agent whenever the key changes
        if api_key.strip() != st.session_state.last_api_key:
            st.session_state.agent = AgentController(api_key=api_key.strip())
            st.session_state.api_key_set = True
            st.session_state.last_api_key = api_key.strip()
        st.markdown('<p style="color:#10b981; font-size:0.8rem; margin:0.3rem 0;">✅ API Key set</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:#f59e0b; font-size:0.8rem; margin:0.3rem 0;">⚠️ Enter your Groq API key above</p>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.75rem; margin:0;"><a href="https://console.groq.com" target="_blank" style="color:#a78bfa;">Get free key → console.groq.com</a></p>', unsafe_allow_html=True)

    # ── File Upload ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">📂 Dataset</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Upload Dataset",
        type=["csv", "xlsx", "xls", "json"],
        help="Supports CSV, Excel, JSON",
        label_visibility="collapsed",
    )

    if uploaded:
        try:
            df = load_df(uploaded.read(), uploaded.name)
            if st.session_state.df is None or st.session_state.df_name != uploaded.name:
                st.session_state.df = df
                st.session_state.df_name = uploaded.name
                st.session_state.messages = []
                st.session_state.trace_log = []
                if st.session_state.agent:
                    st.session_state.agent.set_dataframe(df, uploaded.name)
            st.success(f"✅ {uploaded.name} loaded")
        except Exception as e:
            st.error(f"Error: {e}")

    # ── Sample Datasets ──────────────────────────────────────────────────────
    st.markdown('<div class="section-header">🗂️ Sample Datasets</div>', unsafe_allow_html=True)

    SAMPLE_DATASETS = {
        "🚢 Titanic": "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv",
        "🌸 Iris": "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv",
        "💰 Tips": "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv",
        "🏠 Housing": "https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv",
    }

    for name, url in SAMPLE_DATASETS.items():
        if st.button(name, key=f"sample_{name}", use_container_width=True):
            with st.spinner(f"Loading {name}..."):
                try:
                    df = pd.read_csv(url)
                    st.session_state.df = df
                    st.session_state.df_name = name.split(" ", 1)[1]
                    st.session_state.messages = []
                    st.session_state.trace_log = []
                    if st.session_state.agent:
                        st.session_state.agent.set_dataframe(df, name)
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to load: {e}")

    # ── Controls ─────────────────────────────────────────────────────────────
    if st.session_state.df is not None:
        st.markdown('<div class="section-header">🎛️ Controls</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.session_state.trace_log = []
                if st.session_state.agent:
                    st.session_state.agent.clear_history()
                st.rerun()
        with col2:
            if st.session_state.messages and st.session_state.agent:
                report_md = generate_report(
                    st.session_state.df_name,
                    st.session_state.agent.conversation_history,
                    st.session_state.agent.get_tool_log(),
                    st.session_state.agent.get_charts(),
                )
                st.download_button(
                    "📥 Report",
                    data=report_md,
                    file_name=f"analysis_{st.session_state.df_name.replace(' ', '_')}.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

    # ── Agent Info ───────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.72rem; color:#64748b; line-height:1.6;">
    <b style="color:#8b5cf6;">🔧 19 Analysis Tools</b><br>
    Data profiling · SQL queries<br>
    Charts & visualizations<br>
    ML clustering · Forecasting<br>
    Outlier detection · Stats<br><br>
    <b style="color:#8b5cf6;">⚡ Model</b><br>
    llama-3.3-70b-versatile<br>
    Sub-second inference
    </div>
    """, unsafe_allow_html=True)


# ── MAIN CONTENT ───────────────────────────────────────────────────────────────
# Header
st.markdown("""
<div style="padding: 1.5rem 0 0.5rem;">
    <div class="hero-title">🤖 AI Data Analyst</div>
    <div class="hero-subtitle">Agentic AI that autonomously explores, visualizes & interprets your data</div>
</div>
""", unsafe_allow_html=True)

# ── Dataset Stats ──────────────────────────────────────────────────────────────
if st.session_state.df is not None:
    stats = get_quick_stats(st.session_state.df)
    render_stat_cards_fixed(stats)
    st.markdown("<br>", unsafe_allow_html=True)

    # Data preview expander
    with st.expander(f"📋 Preview: {st.session_state.df_name} ({stats['rows']:,} rows × {stats['columns']} cols)", expanded=False):
        st.dataframe(st.session_state.df.head(20), use_container_width=True)

else:
    # Welcome screen
    st.markdown("""
    <div class="upload-zone">
        <div style="font-size:3rem; margin-bottom:1rem;">📂</div>
        <div style="font-size:1.1rem; font-weight:600; color:#a78bfa; margin-bottom:0.5rem;">Upload Your Dataset to Begin</div>
        <div style="color:#64748b; font-size:0.9rem;">Supports CSV, Excel (.xlsx), and JSON files<br>Or load a sample dataset from the sidebar</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Feature cards
    c1, c2, c3 = st.columns(3)
    features = [
        ("🔍", "Auto EDA", "Automatically explores your data: statistics, distributions, correlations"),
        ("📊", "Smart Charts", "Generates beautiful Plotly visualizations tailored to your questions"),
        ("🧠", "Agentic Analysis", "Plans multi-step analysis — calls 19 tools autonomously via ReAct loop"),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3], features):
        with col:
            st.markdown(f"""
            <div class="stat-card" style="text-align:left; padding:1.2rem;">
                <div style="font-size:1.5rem; margin-bottom:0.5rem;">{icon}</div>
                <div style="font-weight:600; color:#a78bfa; margin-bottom:0.4rem;">{title}</div>
                <div style="font-size:0.83rem; color:#64748b; line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ── Chat Interface ─────────────────────────────────────────────────────────────
if st.session_state.df is not None:
    st.markdown("---")

    # Quick question suggestions
    QUICK_QUESTIONS = [
        "Give me a full EDA of this dataset",
        "What are the top correlations?",
        "Show distribution of all numeric columns",
        "Find outliers in the data",
        "What are the key trends?",
        "Cluster the data and explain patterns",
        "Show missing data analysis",
        "What insights can you derive?",
    ]

    st.markdown('<p style="font-size:0.85rem; color:#64748b; margin-bottom:0.4rem;">💡 Quick Questions:</p>', unsafe_allow_html=True)
    pills_html = '<div class="pill-container">'
    for q in QUICK_QUESTIONS:
        pills_html += f'<span class="pill" onclick="void(0)">{q}</span>'
    pills_html += '</div>'
    st.markdown(pills_html, unsafe_allow_html=True)

    # Quick question buttons (functional)
    cols = st.columns(4)
    for i, q in enumerate(QUICK_QUESTIONS[:4]):
        with cols[i % 4]:
            if st.button(q, key=f"quick_{i}", use_container_width=True):
                st.session_state.pending_question = q

    # ── Display Chat History ───────────────────────────────────────────────────
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-msg-user">👤 {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                # Render agent traces
                if msg.get("traces"):
                    with st.expander("🔍 Agent Trace", expanded=False):
                        for trace in msg["traces"]:
                            cls = {
                                "thought": "trace-thought",
                                "tool_call": "trace-tool",
                                "observation": "trace-obs",
                                "error": "trace-error",
                            }.get(trace["type"], "trace-obs")
                            icon = {"thought": "💭", "tool_call": "🔧", "observation": "👁️", "error": "❌"}.get(trace["type"], "•")
                            content = trace["content"]
                            if trace["type"] == "observation" and len(content) > 300:
                                content = content[:300] + "..."
                            st.markdown(
                                f'<div class="trace-step {cls}">{icon} {content}</div>',
                                unsafe_allow_html=True,
                            )

                st.markdown(f'<div class="chat-msg-assistant">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

                # Render charts
                if msg.get("charts"):
                    chart_cols = st.columns(min(2, len(msg["charts"])))
                    for i, chart_data in enumerate(msg["charts"]):
                        with chart_cols[i % 2]:
                            render_chart(chart_data["chart"])

    # ── Chat Input ─────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    input_col, btn_col = st.columns([5, 1])
    with input_col:
        user_input = st.text_input(
            "Ask anything about your data...",
            key="chat_input",
            placeholder="e.g. What factors most influence survival? Show me trends over time.",
            label_visibility="collapsed",
        )
    with btn_col:
        send_btn = st.button("Analyze ➜", key="send_btn", use_container_width=True)

    # ── Process Input ──────────────────────────────────────────────────────────
    question = st.session_state.pending_question or (user_input if send_btn else None)
    if st.session_state.pending_question:
        st.session_state.pending_question = None

    if question:
        if not st.session_state.agent:
            st.error("⚠️ Please enter your Groq API key in the sidebar.")
        else:
            # Ensure agent has current df
            if st.session_state.agent.df is None:
                st.session_state.agent.set_dataframe(st.session_state.df, st.session_state.df_name)

            # Add user message
            st.session_state.messages.append({"role": "user", "content": question})

            # Run agent and collect output
            traces = []
            charts_before = len(st.session_state.agent.get_charts())

            with st.spinner("🤖 Analyzing..."):
                final_answer = ""
                for step in st.session_state.agent.run(question):
                    traces.append(step)
                    if step["type"] == "answer":
                        final_answer = step["content"]

            # Collect new charts generated during this turn
            all_charts = st.session_state.agent.get_charts()
            new_charts = all_charts[charts_before:]

            # Add assistant message
            st.session_state.messages.append({
                "role": "assistant",
                "content": final_answer,
                "traces": traces,
                "charts": new_charts,
            })

            st.rerun()
