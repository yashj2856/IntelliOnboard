"""
Interface Streamlit - POC Onboarding Automatisé.
Lance avec: streamlit run app.py
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import time
import os
from dotenv import load_dotenv

load_dotenv()

from agents.coordinator import Coordinator
from i18n import t, ROLE_NAMES, EXAMPLE_PROMPTS
from llm_client import get_llm_client

# ============================================
# Configuration de la page
# ============================================
st.set_page_config(
    page_title="🚀 Onboarding Agent",
    page_icon="🚀",
    layout="wide",
)

# ============================================
# Styles CSS custom
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --ink: #172126;
        --muted: #667277;
        --paper: #f4f5f0;
        --surface: #ffffff;
        --line: #dce2df;
        --teal: #087f78;
        --teal-dark: #075b57;
        --coral: #ee765e;
        --gold: #d5a33a;
        --shadow: 0 18px 50px rgba(23, 33, 38, 0.08);
    }

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: var(--ink); color-scheme: light; }
    .stApp, .stApp * { color-scheme: light; }
    [data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] p,
    [data-testid="stTextArea"] label, [data-testid="stWidgetLabel"] p,
    [data-testid="stCaptionContainer"] { color: var(--ink); }
    [data-testid="stCaptionContainer"] { color: var(--muted); }
    .stApp {
        background:
            radial-gradient(circle at 8% 4%, rgba(8, 127, 120, 0.10), transparent 25rem),
            radial-gradient(circle at 95% 20%, rgba(238, 118, 94, 0.08), transparent 22rem),
            var(--paper);
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stToolbar"] { right: 1rem; }
    .block-container { max-width: 1420px; padding: 3.2rem 4rem 5rem; }
    h1, h2, h3, h4 { font-family: 'Space Grotesk', sans-serif !important; color: var(--ink); letter-spacing: 0; }
    h1 { font-size: clamp(2.4rem, 4vw, 4.8rem) !important; line-height: 0.98 !important; }
    h2 { font-size: 1.35rem !important; }
    hr { border-color: var(--line); margin: 2rem 0; }

    [data-testid="stSidebar"] {
        background: #172126;
        border-right: 0;
    }
    [data-testid="stSidebar"] * { color: #edf3f0; }
    [data-testid="stSidebar"] hr { border-color: rgba(237, 243, 240, 0.14); }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #b8c8c4; }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #ffffff !important; }
    [data-testid="stSidebar"] .stButton button {
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.13);
        color: #ffffff;
        text-align: left;
    }
    [data-testid="stSidebar"] .stButton button:hover { background: rgba(8, 127, 120, 0.45); border-color: #4ac7bd; }
    [data-testid="stSidebar"] [data-testid="stAlert"] { background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255,255,255,0.13); }

    .main-header {
        text-align: left;
        padding: 1.5rem 0 2.5rem;
        max-width: 860px;
    }
    .main-header h1 { margin: 0.35rem 0 0.8rem; }
    .main-header p { color: var(--muted); font-size: 1.05rem; max-width: 650px; }
    .hero-kicker {
        color: var(--teal);
        font: 700 0.74rem/1 'DM Sans', sans-serif;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }
    .hero-note { color: var(--muted); font-size: 0.84rem; }
    .section-label {
        color: var(--teal);
        font: 700 0.7rem/1 'DM Sans', sans-serif;
        letter-spacing: 0.14em;
        margin-bottom: 0.6rem;
        text-transform: uppercase;
    }
    .launch-panel {
        background: rgba(255,255,255,0.74);
        border: 1px solid var(--line);
        border-radius: 18px;
        box-shadow: var(--shadow);
        padding: 1.25rem 1.35rem 0.35rem;
        margin: 0.5rem 0 1.2rem;
    }
    .launch-panel h3 { margin: 0 0 0.25rem; font-size: 1.15rem; }
    .launch-panel p { color: var(--muted); font-size: 0.88rem; margin: 0 0 0.7rem; }
    .mode-note { color: var(--muted); font-size: 0.78rem; margin-top: 0.2rem; }
    .example-heading { color: var(--muted); font-size: 0.8rem; font-weight: 700; margin: 0.55rem 0 0.35rem; }
    .example-grid [data-testid="stButton"] button {
        background: #f8faf7;
        border: 1px solid var(--line);
        color: var(--ink);
        font-size: 0.82rem;
        min-height: 2.8rem;
        text-align: left;
        white-space: normal;
    }
    .example-grid [data-testid="stButton"] button:hover { background: #eaf6f5; border-color: #8bcac4; color: var(--teal-dark); }

    [data-testid="stTextArea"] textarea {
        min-height: 132px;
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 14px;
        color: var(--ink);
        box-shadow: inset 0 1px 2px rgba(23,33,38,0.03);
        font-size: 1.02rem !important;
        line-height: 1.6;
        padding: 1rem 1.1rem;
    }
    [data-testid="stTextArea"] label p { color: var(--ink) !important; font-weight: 700; }
    [data-testid="stTextArea"] textarea::placeholder { color: #899493; opacity: 1; }
    [data-testid="stTextArea"] textarea:focus { border-color: var(--teal); box-shadow: 0 0 0 3px rgba(8,127,120,0.14); }
    [data-testid="stButton"] button[kind="primary"] {
        background: var(--coral);
        border: 0;
        border-radius: 10px;
        box-shadow: 0 8px 18px rgba(238,118,94,0.24);
        color: #ffffff;
        font-weight: 700;
        min-height: 3rem;
    }
    [data-testid="stButton"] button[kind="primary"]:hover { background: #d95f49; transform: translateY(-1px); }
    [data-testid="stButton"] button { border-radius: 9px; transition: all 160ms ease; }

    [data-testid="metric-container"] {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 14px;
        box-shadow: var(--shadow);
        padding: 1.1rem 1.2rem;
    }
    [data-testid="stMetricLabel"] { color: var(--muted); font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; }
    [data-testid="stMetricValue"] { color: var(--teal-dark); font-family: 'Space Grotesk', sans-serif; }
    [data-testid="stExpander"] {
        background: rgba(255,255,255,0.72);
        border: 1px solid var(--line);
        border-radius: 14px;
        box-shadow: 0 8px 28px rgba(23,33,38,0.04);
        margin: 0.65rem 0;
    }
    [data-testid="stExpander"] summary p { font-weight: 700; color: var(--ink); }
    [data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 10px; overflow: hidden; }
    [data-testid="stAlert"] p { color: var(--ink) !important; }
    .log-entry {
        padding: 0.7rem 0.85rem;
        margin: 0.45rem 0;
        border-radius: 10px;
        border: 1px solid transparent;
        font-family: 'SF Mono', 'Fira Code', monospace;
        font-size: 0.85rem;
        box-shadow: 0 3px 10px rgba(23,33,38,0.04);
    }
    .log-success { background: #eaf7f1; border-color: #b9e5d0; border-left: 4px solid #15916b; }
    .log-pending { background: #fff7e4; border-color: #f1d99b; border-left: 4px solid var(--gold); }
    .log-error { background: #fff0ed; border-color: #f2c1b7; border-left: 4px solid var(--coral); }
    .log-info { background: #eaf6f5; border-color: #b9e1dd; border-left: 4px solid var(--teal); }
    @media (max-width: 900px) {
        .block-container { padding: 2rem 1.2rem 4rem; }
        .main-header { padding-bottom: 1.5rem; }
        [data-testid="metric-container"] { padding: 0.8rem; }
    }
    @media (prefers-color-scheme: dark) {
        .stApp { background: var(--paper); }
        [data-testid="stTextArea"] textarea,
        [data-testid="stSelectbox"] input,
        [data-testid="stChatInput"] textarea { background: #ffffff !important; color: var(--ink) !important; }
        [data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] p,
        [data-testid="stWidgetLabel"] p, [data-testid="stTextArea"] label p,
        [data-testid="stExpander"] summary p { color: var(--ink) !important; }
        [data-testid="stCaptionContainer"] { color: var(--muted) !important; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# Sidebar - Configuration
# ============================================
with st.sidebar:
    st.markdown("<div class='section-label' style='color:#73d1c8'>WORKSPACE</div>", unsafe_allow_html=True)
    st.header("Onboarding OS")
    lang = "en"

    llm_provider = os.getenv("LLM_PROVIDER", "anthropic")
    st.caption("Automated onboarding workspace")
    st.markdown(f"**Provider**  `{llm_provider}`")
    st.markdown(f"**Model**  `{os.getenv('ANTHROPIC_MODEL', os.getenv('OPENAI_MODEL', 'not configured'))}`")

    st.markdown(t("available_roles", lang))
    for role_key, names in ROLE_NAMES.items():
        st.markdown(f"- {names.get(lang, names['fr'])}")


# ============================================
# Header
# ============================================
st.markdown('<div class="main-header"><div class="hero-kicker">Onboarding operations console</div>', unsafe_allow_html=True)
st.title(t("page_title", lang))
st.caption(t("page_subtitle", lang))
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ============================================
# Zone de saisie principale
# ============================================
user_input = st.text_area(
    t("input_label", lang),
    key="user_input_text",
    height=100,
    placeholder=t("input_placeholder", lang),
)

st.markdown('<div class="launch-panel">', unsafe_allow_html=True)
control_col, example_col = st.columns([0.78, 1.22], gap="large")
with control_col:
    st.markdown('<div class="section-label">RUN MODE</div>', unsafe_allow_html=True)
    simulation_mode = st.toggle(t("simulation_toggle", lang), value=True,
                                 help=t("simulation_help", lang))
    st.markdown(
        f'<div class="mode-note">{"Safe preview: no emails or files will be created." if simulation_mode else "Live mode: connected actions will run for real."}</div>',
        unsafe_allow_html=True,
    )
with example_col:
    st.markdown('<div class="section-label">START FROM A BRIEF</div>', unsafe_allow_html=True)
    st.markdown('<div class="example-heading">Choose a ready-made onboarding request</div>', unsafe_allow_html=True)
    examples = EXAMPLE_PROMPTS.get(lang, EXAMPLE_PROMPTS["en"])
    st.markdown('<div class="example-grid">', unsafe_allow_html=True)
    example_cols = st.columns(3, gap="small")
    for i, example in enumerate(examples):
        with example_cols[i % 3]:
            if st.button(f"{t('example_button', lang)} {i + 1}", key=f"ex_{i}", use_container_width=True, help=example):
                st.session_state["user_input_text"] = example
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

col_btn, col_spacer = st.columns([1, 4])
with col_btn:
    launch = st.button(t("launch_button", lang), type="primary", use_container_width=True)

# ============================================
# Helper: translate welcome book via LLM
# ============================================
def translate_welcome_book(text: str) -> str:
    """Translate the French welcome book to English via LLM."""
    cache_key = f"translated_wb_{hash(text)}"
    if cache_key in st.session_state:
        return st.session_state[cache_key]

    llm = get_llm_client()
    response = llm.chat(
        system_prompt="You are a professional translator. Translate the following French markdown document to English. Keep all markdown formatting, emojis, and structure intact. Only translate the text content.",
        user_message=text,
        temperature=0.2,
    )
    translated = response["text"]
    st.session_state[cache_key] = translated
    return translated


# ============================================
# Exécution de l'onboarding
# ============================================
if launch and user_input.strip():

    # Containers pour l'affichage en temps réel
    col_logs, col_results = st.columns([1, 1])

    with col_logs:
        st.subheader(t("live_execution", lang))
        log_container = st.container()

    with col_results:
        st.subheader(t("results_header", lang))
        results_container = st.container()

    # Log callback pour affichage en temps réel
    log_entries = []

    def progress_callback(agent, action, status, details):
        log_entries.append((agent, action, status, details))
        with log_container:
            css_class = "log-success" if status == "✓" else "log-pending" if status == "⏳" else "log-info" if status in ("📅", "📧") else "log-error"
            st.markdown(
                f'<div class="log-entry {css_class}">{status} <strong>[{agent}]</strong> {action}</div>',
                unsafe_allow_html=True,
            )
        time.sleep(0.3)

    # Lancer le coordinator avec la langue
    coordinator = Coordinator(simulation_mode=simulation_mode, lang=lang)

    with st.spinner(t("agents_working", lang)):
        result = coordinator.run(user_input, progress_callback=progress_callback)

    # ============================================
    # Affichage des résultats
    # ============================================
    with results_container:
        if result.status == "completed":
            st.success(t("onboarding_success", lang))

            # Métriques
            m1, m2, m3, m4 = st.columns(4)
            m1.metric(t("folders_metric", lang), len(result.drive_folders))
            m2.metric(t("meetings_metric", lang), len(result.calendar_events))
            m3.metric(t("emails_metric", lang), len(result.emails_sent))
            m4.metric(t("tasks_metric", lang), result.checklist.get("total_tasks", "N/A"))

            # Détails par section
            with st.expander(t("drive_folders", lang), expanded=True):
                for key, folder in result.drive_folders.items():
                    st.markdown(f"- **{folder['name']}** → [{folder.get('webViewLink', '#')}]({folder.get('webViewLink', '#')})")

            with st.expander(t("meetings_planned", lang), expanded=True):
                for event in result.calendar_events:
                    st.markdown(f"- **{event.get('summary', '')}** — {event.get('start', '')} ({event.get('duration', '?')} min)")

            with st.expander(t("emails_sent", lang), expanded=True):
                for email in result.emails_sent:
                    st.markdown(f"- **→ {email.get('to', '')}** : {email.get('subject', '')}")

            # ─── Checklist Table ───
            with st.expander(t("checklist_title", lang), expanded=True):
                if result.checklist_tasks:
                    df = pd.DataFrame(result.checklist_tasks)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.markdown(f"**{result.checklist.get('name', '')}**")
                    st.markdown(f"Link: [{result.checklist.get('link', '#')}]({result.checklist.get('link', '#')})")

            # ─── Welcome Book ───
            if result.welcome_book:
                with st.expander(t("welcome_book_title", lang), expanded=False):
                    if lang == "en":
                        with st.spinner(t("translating", lang)):
                            display_book = translate_welcome_book(result.welcome_book)
                    else:
                        display_book = result.welcome_book

                    st.markdown(display_book)
                    st.download_button(
                        label=t("download_welcome_md", lang),
                        data=display_book,
                        file_name="livret_accueil.md",
                        mime="text/markdown",
                    )

            # ─── HTML Presentation ───
            if result.presentation_html:
                with st.expander(t("presentation_title", lang), expanded=False):
                    components.html(result.presentation_html, height=620, scrolling=True)
                    st.download_button(
                        label=t("download_presentation", lang),
                        data=result.presentation_html,
                        file_name="onboarding_presentation.html",
                        mime="text/html",
                    )

            # Résumé final
            st.divider()
            req = result.request
            st.markdown(t("summary_title", lang))
            st.markdown(f"""
            **{t("employee_label", lang)} :** {req.get('employee_name', 'N/A')}
            **{t("email_label", lang)} :** {req.get('employee_email', 'N/A')}
            **{t("position_label", lang)} :** {req.get('role_title', 'N/A')}
            **{t("team_label", lang)} :** {req.get('team', 'N/A')}
            **{t("start_date_label", lang)} :** {req.get('start_date', 'N/A')}
            """)

        elif result.status == "error":
            st.error(t("onboarding_error", lang))
            for log in result.logs:
                if log["status"] == "❌":
                    st.error(f"**{log['agent']}** : {log['action']} — {log['details']}")

elif launch:
    st.warning(t("empty_input_warning", lang))
