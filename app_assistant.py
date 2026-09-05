"""
Interface Chat - Assistant d'onboarding personnel.
Page séparée accessible via URL avec l'ID employé.
Lance avec: streamlit run app_assistant.py
"""

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

from agents.onboarding_assistant import OnboardingAssistant
from i18n import t, ASSISTANT_SUGGESTIONS

# ============================================
# Configuration de la page
# ============================================
st.set_page_config(
    page_title="💬 Assistant Onboarding",
    page_icon="💬",
    layout="centered",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --ink: #172126;
        --muted: #68777a;
        --paper: #f4f5f0;
        --surface: #ffffff;
        --line: #dce2df;
        --teal: #087f78;
        --teal-dark: #075b57;
        --coral: #ee765e;
    }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: var(--ink); color-scheme: light; }
    .stApp, .stApp * { color-scheme: light; }
    [data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] p,
    [data-testid="stWidgetLabel"] p, [data-testid="stCaptionContainer"] { color: var(--ink); }
    [data-testid="stCaptionContainer"] { color: var(--muted); }
    .stApp {
        background:
            radial-gradient(circle at 90% 0%, rgba(8, 127, 120, 0.11), transparent 24rem),
            radial-gradient(circle at 5% 55%, rgba(238, 118, 94, 0.07), transparent 20rem),
            var(--paper);
    }
    [data-testid="stHeader"] { background: transparent; }
    .block-container { max-width: 980px; padding: 3rem 2.5rem 6rem; }
    h1, h2, h3, h4 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: 0; }
    [data-testid="stSidebar"] { background: #172126; border-right: 0; }
    [data-testid="stSidebar"] * { color: #edf3f0; }
    [data-testid="stSidebar"] hr { border-color: rgba(237, 243, 240, 0.14); }
    [data-testid="stSidebar"] .stButton button {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.13);
        color: #ffffff;
        border-radius: 9px;
    }
    [data-testid="stSidebar"] .stButton button:hover { background: rgba(8,127,120,0.45); border-color: #4ac7bd; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #b8c8c4; }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #ffffff !important; }

    .status-card {
        background: #172126;
        color: #ffffff;
        padding: 1.45rem 1.6rem;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        margin: 0.5rem 0 1.4rem;
        box-shadow: 0 18px 45px rgba(23,33,38,0.14);
        position: relative;
        overflow: hidden;
    }
    .status-card::after {
        content: '';
        width: 7rem;
        height: 7rem;
        border: 1px solid rgba(74,199,189,0.35);
        border-radius: 50%;
        position: absolute;
        right: -2rem;
        top: -3rem;
    }
    .status-card h3 { margin: 0; color: white !important; font-size: 1.35rem; }
    .status-card p { margin: 0.45rem 0 0; color: #b8c8c4; }
    [data-testid="stChatMessage"] {
        border: 1px solid var(--line);
        border-radius: 15px;
        margin: 0.7rem 0;
        padding: 0.9rem 1rem;
        background: rgba(255,255,255,0.76);
    }
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p { line-height: 1.65; }
    [data-testid="stChatInput"] textarea {
        border: 1px solid var(--line);
        border-radius: 13px;
        background: var(--surface);
        color: var(--ink);
        box-shadow: 0 10px 30px rgba(23,33,38,0.08);
    }
    [data-testid="stChatInput"] textarea:focus { border-color: var(--teal); box-shadow: 0 0 0 3px rgba(8,127,120,0.14); }
    [data-testid="stButton"] button {
        border-radius: 10px;
        border-color: var(--line);
        transition: all 160ms ease;
    }
    [data-testid="stButton"] button:hover { border-color: var(--teal); color: var(--teal-dark); transform: translateY(-1px); }
    [data-testid="stProgressBar"] > div > div { background: var(--teal); }
    [data-testid="stAlert"] p { color: var(--ink) !important; }
    hr { border-color: var(--line); margin: 1.8rem 0; }
    @media (max-width: 700px) {
        .block-container { padding: 1.5rem 1rem 5rem; }
        .status-card { padding: 1.15rem; }
    }
    @media (prefers-color-scheme: dark) {
        .stApp { background: var(--paper); }
        [data-testid="stChatInput"] textarea { background: #ffffff !important; color: var(--ink) !important; }
        [data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] p,
        [data-testid="stWidgetLabel"] p { color: var(--ink) !important; }
        [data-testid="stCaptionContainer"] { color: var(--muted) !important; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# Sidebar - Sélection de l'employé
# ============================================
with st.sidebar:
    lang = "en"

    st.header(t("assistant_employee_header", lang))

    st.divider()

    # En production: l'employé serait identifié par son login
    # En simulation: on choisit dans une liste
    available_employees = {
        "sarah_martin_data_engineer": "Sarah Martin — Data Engineer",
        "thomas_legrand_fullstack": "Thomas Legrand — Fullstack Dev",
        "claire_rousseau_commercial": "Claire Rousseau — Commercial",
    }

    selected_id = st.selectbox(
        t("assistant_select", lang),
        options=list(available_employees.keys()),
        format_func=lambda x: available_employees[x],
    )

    simulation_mode = st.toggle(t("simulation_toggle", lang), value=True)

    st.divider()

    if st.button(t("assistant_refresh", lang), use_container_width=True):
        if "assistant" in st.session_state:
            st.session_state.assistant.refresh_context()
            st.success(t("assistant_refreshed", lang))

    if st.button(t("assistant_new_convo", lang), use_container_width=True):
        st.session_state.pop("messages", None)
        st.session_state.pop("assistant", None)
        st.rerun()

# ============================================
# Initialisation de l'assistant
# ============================================
needs_reinit = (
    "assistant" not in st.session_state
    or st.session_state.get("current_employee") != selected_id
    or st.session_state.get("current_lang") != lang
)

if needs_reinit:
    st.session_state.assistant = OnboardingAssistant(selected_id, simulation_mode=simulation_mode, lang=lang)
    st.session_state.current_employee = selected_id
    st.session_state.current_lang = lang
    st.session_state.messages = []

assistant: OnboardingAssistant = st.session_state.assistant

# ============================================
# Header avec statut
# ============================================
ctx = assistant.context

st.markdown(f"""
<div class="status-card">
    <h3>💬 Assistant Onboarding — {ctx.employee_name}</h3>
    <p>{ctx.role_title} · {t("team_label", lang)} {ctx.team} · J+{ctx.onboarding_day}</p>
</div>
""", unsafe_allow_html=True)

# Barre de progression
total_tasks = len(ctx.checklist_status)
done_tasks = sum(1 for item in ctx.checklist_status if "Fait" in item["status"])
if total_tasks > 0:
    progress = done_tasks / total_tasks
    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress(progress)
    with col2:
        st.caption(f"{done_tasks}/{total_tasks} {t('assistant_tasks_label', lang)}")

st.divider()

# ============================================
# Suggestions de questions (pour la démo)
# ============================================
if not st.session_state.messages:
    st.markdown(t("assistant_greeting", lang).format(name=ctx.employee_name))
    st.caption(t("assistant_suggestions_label", lang))

    suggestions = ASSISTANT_SUGGESTIONS.get(lang, ASSISTANT_SUGGESTIONS["fr"])

    # Afficher les suggestions comme des boutons
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(suggestion, key=f"sug_{i}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": suggestion})
                with st.spinner(""):
                    response = assistant.chat(suggestion)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

# ============================================
# Historique de la conversation
# ============================================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ============================================
# Input utilisateur
# ============================================
if prompt := st.chat_input(t("assistant_input_placeholder", lang)):
    # Afficher le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Obtenir et afficher la réponse
    with st.chat_message("assistant"):
        with st.spinner(t("assistant_thinking", lang)):
            response = assistant.chat(prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
