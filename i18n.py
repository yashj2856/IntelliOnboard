"""
Internationalisation simple FR/EN pour l'interface Streamlit.
"""

TRANSLATIONS = {
    # app.py - Header & layout
    "page_title": {
        "fr": "🚀 Agent d'Onboarding Automatisé",
        "en": "🚀 Automated Onboarding Agent",
    },
    "page_subtitle": {
        "fr": "Un prompt. 4 agents. 30 secondes. L'onboarding qui prenait 3 jours est prêt.",
        "en": "One prompt. 4 agents. 30 seconds. The onboarding that took 3 days is ready.",
    },
    # Sidebar
    "config_header": {
        "fr": "⚙️ Configuration",
        "en": "⚙️ Settings",
    },
    "language_label": {
        "fr": "🌐 Langue / Language",
        "en": "🌐 Language / Langue",
    },
    "simulation_toggle": {
        "fr": "Mode simulation",
        "en": "Simulation mode",
    },
    "simulation_on": {
        "fr": "🧪 Mode simulation actif. Aucun email ne sera envoyé, aucun fichier ne sera créé.",
        "en": "🧪 Simulation mode active. No emails will be sent, no files will be created.",
    },
    "simulation_off": {
        "fr": "⚡ Mode production. Les actions seront exécutées réellement.",
        "en": "⚡ Production mode. Actions will be executed for real.",
    },
    "simulation_help": {
        "fr": "Active le mode simulation (sans appels Google API réels)",
        "en": "Enable simulation mode (no real Google API calls)",
    },
    "available_roles": {
        "fr": "### 📋 Rôles disponibles",
        "en": "### 📋 Available Roles",
    },
    "example_prompts": {
        "fr": "### 💡 Exemples de prompts",
        "en": "### 💡 Example Prompts",
    },
    "example_button": {
        "fr": "Exemple",
        "en": "Example",
    },
    # Input
    "input_label": {
        "fr": "📝 Décrivez le nouvel employé à onboarder",
        "en": "📝 Describe the new employee to onboard",
    },
    "input_placeholder": {
        "fr": "Ex: Nouvel employé : Sarah Martin, poste Data Engineer, équipe Data Platform, manager Jean Dupont, arrive le 3 mars 2026",
        "en": "E.g.: New employee: Sarah Martin, position Data Engineer, team Data Platform, manager Jean Dupont, starts March 3 2026",
    },
    "launch_button": {
        "fr": "🚀 Lancer l'onboarding",
        "en": "🚀 Launch Onboarding",
    },
    # Execution
    "live_execution": {
        "fr": "📡 Exécution en direct",
        "en": "📡 Live Execution",
    },
    "results_header": {
        "fr": "📊 Résultats",
        "en": "📊 Results",
    },
    "agents_working": {
        "fr": "Les agents travaillent...",
        "en": "Agents are working...",
    },
    # Results
    "onboarding_success": {
        "fr": "✅ Onboarding terminé avec succès !",
        "en": "✅ Onboarding completed successfully!",
    },
    "onboarding_error": {
        "fr": "❌ Une erreur est survenue pendant l'onboarding.",
        "en": "❌ An error occurred during onboarding.",
    },
    "folders_metric": {"fr": "📁 Dossiers", "en": "📁 Folders"},
    "meetings_metric": {"fr": "📅 Réunions", "en": "📅 Meetings"},
    "emails_metric": {"fr": "📧 Emails", "en": "📧 Emails"},
    "tasks_metric": {"fr": "☑️ Tâches", "en": "☑️ Tasks"},
    # Expanders
    "drive_folders": {
        "fr": "📁 Dossiers Google Drive créés",
        "en": "📁 Google Drive Folders Created",
    },
    "meetings_planned": {
        "fr": "📅 Réunions planifiées",
        "en": "📅 Scheduled Meetings",
    },
    "emails_sent": {
        "fr": "📧 Emails envoyés",
        "en": "📧 Emails Sent",
    },
    "checklist_title": {
        "fr": "📋 Checklist de suivi",
        "en": "📋 Onboarding Checklist",
    },
    "welcome_book_title": {
        "fr": "📖 Livret d'Accueil",
        "en": "📖 Welcome Book",
    },
    "presentation_title": {
        "fr": "🎬 Présentation d'Onboarding",
        "en": "🎬 Onboarding Presentation",
    },
    "download_welcome_md": {
        "fr": "📥 Télécharger le Livret (.md)",
        "en": "📥 Download Welcome Book (.md)",
    },
    "download_presentation": {
        "fr": "📥 Télécharger la Présentation (.html)",
        "en": "📥 Download Presentation (.html)",
    },
    # Summary
    "summary_title": {
        "fr": "### 🎯 Récapitulatif",
        "en": "### 🎯 Summary",
    },
    "employee_label": {"fr": "Employé", "en": "Employee"},
    "email_label": {"fr": "Email", "en": "Email"},
    "position_label": {"fr": "Poste", "en": "Position"},
    "team_label": {"fr": "Équipe", "en": "Team"},
    "start_date_label": {"fr": "Date d'arrivée", "en": "Start Date"},
    "empty_input_warning": {
        "fr": "⚠️ Veuillez décrire le nouvel employé à onboarder.",
        "en": "⚠️ Please describe the new employee to onboard.",
    },
    # Assistant page
    "assistant_employee_header": {"fr": "👤 Employé", "en": "👤 Employee"},
    "assistant_select": {
        "fr": "Sélectionner un employé",
        "en": "Select an employee",
    },
    "assistant_refresh": {
        "fr": "🔄 Rafraîchir le contexte",
        "en": "🔄 Refresh Context",
    },
    "assistant_refreshed": {
        "fr": "Contexte rafraîchi !",
        "en": "Context refreshed!",
    },
    "assistant_new_convo": {
        "fr": "🗑️ Nouvelle conversation",
        "en": "🗑️ New Conversation",
    },
    "assistant_greeting": {
        "fr": "Bonjour **{name}** ! Je suis ton assistant d'onboarding. Pose-moi n'importe quelle question sur ton arrivée.",
        "en": "Hello **{name}**! I'm your onboarding assistant. Ask me anything about your first days.",
    },
    "assistant_suggestions_label": {
        "fr": "💡 Exemples de questions :",
        "en": "💡 Example questions:",
    },
    "assistant_thinking": {
        "fr": "Je réfléchis...",
        "en": "Thinking...",
    },
    "assistant_input_placeholder": {
        "fr": "Pose ta question...",
        "en": "Ask your question...",
    },
    "assistant_tasks_label": {
        "fr": "tâches",
        "en": "tasks",
    },
    "translating": {
        "fr": "Traduction en cours...",
        "en": "Translating...",
    },
    # Coordinator log messages
    "log_parsing": {"fr": "Analyse de la demande...", "en": "Parsing request..."},
    "log_insufficient": {"fr": "Informations insuffisantes", "en": "Insufficient information"},
    "log_name_role_required": {"fr": "Nom et rôle requis au minimum", "en": "Name and role required at minimum"},
    "log_parsed": {"fr": "Demande parsée", "en": "Request parsed"},
    "log_unknown_role": {"fr": "Rôle inconnu", "en": "Unknown role"},
    "log_config_loaded": {"fr": "Config chargée pour", "en": "Config loaded for"},
    "log_creating_drive": {"fr": "Création de l'arborescence Drive...", "en": "Creating Drive folder structure..."},
    "log_folders_created": {"fr": "dossiers créés dans Drive", "en": "folders created in Drive"},
    "log_scheduling": {"fr": "Planification de {} réunions...", "en": "Scheduling {} meetings..."},
    "log_meetings_scheduled": {"fr": "réunions planifiées", "en": "meetings scheduled"},
    "log_sending_emails": {"fr": "Envoi des emails...", "en": "Sending emails..."},
    "log_emails_sent": {"fr": "emails envoyés", "en": "emails sent"},
    "log_creating_checklist": {"fr": "Création de la checklist de suivi...", "en": "Creating tracking checklist..."},
    "log_checklist_created": {"fr": "Checklist créée: {} tâches", "en": "Checklist created: {} tasks"},
    "log_generating_book": {"fr": "Génération du Livret d'Accueil...", "en": "Generating Welcome Book..."},
    "log_book_generated": {"fr": "Livret d'Accueil généré", "en": "Welcome Book generated"},
    "log_book_error": {"fr": "Erreur livret", "en": "Welcome Book error"},
    "log_generating_pres": {"fr": "Génération de la présentation d'onboarding...", "en": "Generating onboarding presentation..."},
    "log_pres_generated": {"fr": "Présentation HTML générée", "en": "HTML presentation generated"},
    "log_pres_error": {"fr": "Erreur présentation", "en": "Presentation error"},
    "log_complete": {"fr": "Onboarding complet !", "en": "Onboarding complete!"},
    # Email subjects
    "email_welcome_subject": {"fr": "Bienvenue {name} !", "en": "Welcome {name}!"},
    "email_manager_subject": {"fr": "[Onboarding] {name} arrive", "en": "[Onboarding] {name} is joining"},
    "email_team_subject": {"fr": "{name} rejoint l'équipe", "en": "{name} is joining the team"},
    "email_it_subject": {"fr": "[Onboarding] Accès - {name}", "en": "[Onboarding] Access - {name}"},
}

# Suggestions for assistant page
ASSISTANT_SUGGESTIONS = {
    "fr": [
        "Quel est mon planning pour cette semaine ?",
        "Quels outils dois-je installer ?",
        "Qui sont les membres de mon équipe ?",
        "Où en est ma checklist d'onboarding ?",
        "Comment configurer mon accès GCP ?",
        "Quelles formations dois-je suivre ?",
        "Comment poser des congés ?",
        "Qui contacter si j'ai un problème technique ?",
    ],
    "en": [
        "What's my schedule for this week?",
        "What tools do I need to install?",
        "Who are my team members?",
        "Where is my onboarding checklist?",
        "How do I set up my GCP access?",
        "What training do I need to complete?",
        "How do I request time off?",
        "Who should I contact for technical issues?",
    ],
}

# Role display names for sidebar
ROLE_NAMES = {
    "data_engineer": {"fr": "🔧 Data Engineer", "en": "🔧 Data Engineer"},
    "developpeur_fullstack": {"fr": "💻 Développeur Fullstack", "en": "💻 Fullstack Developer"},
    "chef_de_projet": {"fr": "📊 Chef de Projet", "en": "📊 Project Manager"},
    "commercial": {"fr": "🤝 Commercial", "en": "🤝 Sales Executive"},
}

# Example prompts for sidebar
EXAMPLE_PROMPTS = {
    "fr": [
        "Nouvel employé : Sarah Martin, Data Engineer dans l'équipe Data Platform, manager Jean Dupont, arrive le 3 mars 2026",
        "On recrute Thomas Legrand comme développeur fullstack dans l'équipe Engineering, il commence le 10 mars",
        "Prépare l'onboarding de Claire Rousseau, elle arrive comme commerciale le 17 mars, équipe Sales",
    ],
    "en": [
        "New employee: Sarah Martin, Data Engineer on the Data Platform team, manager Jean Dupont, starts March 3 2026",
        "We're hiring Thomas Legrand as a fullstack developer on the Engineering team, he starts March 10",
        "Prepare onboarding for Claire Rousseau, joining as Sales Executive on March 17, Sales team",
    ],
}

# Checklist phase labels
PHASE_LABELS = {
    "avant_arrivee": {"fr": "Avant l'arrivée", "en": "Pre-arrival"},
    "jour_1": {"fr": "Jour 1", "en": "Day 1"},
    "semaine_1": {"fr": "Semaine 1", "en": "Week 1"},
    "mois_1": {"fr": "Mois 1", "en": "Month 1"},
}

# Checklist column headers
CHECKLIST_COLUMNS = {
    "Phase": {"fr": "Phase", "en": "Phase"},
    "Tâche": {"fr": "Tâche", "en": "Task"},
    "Statut": {"fr": "Statut", "en": "Status"},
}

CHECKLIST_STATUS_TODO = {"fr": "⬜ À faire", "en": "⬜ To do"}

# Meeting type translations (from roles.yaml French to English)
MEETING_TYPES = {
    "1:1 Manager": "1:1 Manager",
    "Déjeuner d'équipe": "Team Lunch",
    "Setup technique": "Technical Setup",
    "Architecture walkthrough": "Architecture Walkthrough",
    "Pair programming": "Pair Programming",
    "1:1 RH": "1:1 HR",
    "Point d'étape": "Week-end Checkpoint",
    "Codebase walkthrough": "Codebase Walkthrough",
    "Product overview": "Product Overview",
    "Tour des projets": "Project Tour",
    "Rencontre stakeholders": "Stakeholder Meetings",
    "Shadow commercial": "Sales Shadow",
    "Product deep dive": "Product Deep Dive",
    "Jeu de rôle pitch": "Pitch Role Play",
}

# Checklist task translations (from roles.yaml French to English)
TASK_TRANSLATIONS = {
    # data_engineer
    "Commander le matériel (laptop, écran, etc.)": "Order equipment (laptop, monitor, etc.)",
    "Créer le compte Google Workspace": "Create Google Workspace account",
    "Préparer les accès GCP": "Provision GCP access",
    "Créer le compte GitHub et ajouter aux repos": "Create GitHub account and add to repos",
    "Préparer le badge d'accès": "Prepare access badge",
    "Accueil physique par le manager": "In-person welcome by manager",
    "Tour des locaux": "Office tour",
    "Installation du poste de travail": "Workstation setup",
    "Vérification de tous les accès": "Verify all access credentials",
    "Compléter toutes les formations obligatoires": "Complete all mandatory training",
    "Premier commit sur un repo": "First commit on a repo",
    "Comprendre le pipeline de données principal": "Understand the main data pipeline",
    "Livrer un premier ticket en autonomie": "Deliver a first ticket independently",
    "Documenter un processus existant": "Document an existing process",
    "Feedback 360 informel": "Informal 360 feedback",
    # developpeur_fullstack
    "Commander le matériel": "Order equipment",
    "Créer les comptes (Google, GitHub, Slack)": "Create accounts (Google, GitHub, Slack)",
    "Préparer un premier ticket 'good first issue'": "Prepare a first 'good first issue' ticket",
    "Accueil et tour des locaux": "Welcome and office tour",
    "Setup complet de l'environnement": "Complete environment setup",
    "Premier `git clone` et `npm run dev`": "First `git clone` and `npm run dev`",
    "Compléter les formations obligatoires": "Complete mandatory training",
    "Merger une première PR": "Merge a first PR",
    "Livrer une feature en autonomie": "Deliver a feature independently",
    "Participer à une code review": "Participate in a code review",
    # chef_de_projet
    "Créer les comptes outils": "Create tool accounts",
    "Préparer l'accès aux dossiers projets": "Prepare access to project folders",
    "Identifier le premier projet à confier": "Identify first project to assign",
    "Accueil et présentation de l'équipe": "Welcome and team introduction",
    "Accès à tous les outils validé": "All tool access verified",
    "Comprendre le portefeuille projets": "Understand the project portfolio",
    "Shadow sur un comité de pilotage": "Shadow a steering committee",
    "Piloter un projet en autonomie": "Lead a project independently",
    "Animer un premier comité de pilotage": "Run a first steering committee",
    # commercial
    "Créer le compte CRM": "Create CRM account",
    "Préparer le territoire commercial": "Prepare sales territory",
    "Commander cartes de visite": "Order business cards",
    "Accès CRM validé": "CRM access verified",
    "Présentation de l'offre": "Product offering presentation",
    "Compléter toutes les formations": "Complete all training",
    "Premier appel de prospection supervisé": "First supervised prospecting call",
    "10 premiers RDV en autonomie": "First 10 meetings independently",
    "Première proposition commerciale envoyée": "First commercial proposal sent",
}


def t(key: str, lang: str = "fr") -> str:
    """Get translated string for key and language."""
    entry = TRANSLATIONS.get(key, {})
    return entry.get(lang, entry.get("fr", key))


def translate_task(task_fr: str, lang: str = "fr") -> str:
    """Translate a checklist task from French to the target language."""
    if lang == "fr":
        return task_fr
    return TASK_TRANSLATIONS.get(task_fr, task_fr)


def translate_meeting_type(meeting_type_fr: str, lang: str = "fr") -> str:
    """Translate a meeting type from French to the target language."""
    if lang == "fr":
        return meeting_type_fr
    return MEETING_TYPES.get(meeting_type_fr, meeting_type_fr)
