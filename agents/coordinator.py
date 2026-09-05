"""
Agent Coordinateur - Orchestre le processus d'onboarding complet.
Parse la demande, charge la config du rôle, et délègue aux agents spécialisés.
"""

import os
import yaml
import json
import logging
from datetime import datetime
from dataclasses import dataclass, field, asdict

import jinja2
from llm_client import get_llm_client
from i18n import t, PHASE_LABELS, CHECKLIST_STATUS_TODO, CHECKLIST_COLUMNS, translate_task, translate_meeting_type

logger = logging.getLogger(__name__)


@dataclass
class OnboardingRequest:
    """Données structurées de la demande d'onboarding."""
    employee_name: str = ""
    employee_email: str = ""
    role_key: str = ""
    role_title: str = ""
    team: str = ""
    manager_name: str = ""
    start_date: str = ""
    extra_info: str = ""


@dataclass
class OnboardingResult:
    """Résultats de l'onboarding complet."""
    request: dict = field(default_factory=dict)
    drive_folders: dict = field(default_factory=dict)
    calendar_events: list = field(default_factory=list)
    emails_sent: list = field(default_factory=list)
    checklist: dict = field(default_factory=dict)
    checklist_tasks: list = field(default_factory=list)
    welcome_book: str = ""
    presentation_html: str = ""
    logs: list = field(default_factory=list)
    status: str = "pending"

    def add_log(self, agent: str, action: str, status: str = "✓", details: str = ""):
        self.logs.append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "action": action,
            "status": status,
            "details": details,
        })


PARSE_SYSTEM_PROMPT = """Tu es un assistant qui extrait les informations d'onboarding depuis un message en langage naturel.
Extrais les informations suivantes et retourne-les en JSON strict (pas de markdown, pas de commentaires) :
{
    "employee_name": "nom complet",
    "employee_email": "email si mentionné, sinon chaîne vide",
    "role_key": "clé du rôle parmi: data_engineer, developpeur_fullstack, chef_de_projet, commercial",
    "role_title": "titre du poste tel que mentionné",
    "team": "nom de l'équipe si mentionné",
    "manager_name": "nom du manager si mentionné",
    "start_date": "date au format YYYY-MM-DD",
    "extra_info": "toute info supplémentaire"
}
Si une info n'est pas mentionnée, laisse une chaîne vide.
Pour role_key, déduis le plus proche parmi les clés disponibles."""


class Coordinator:
    """Agent coordinateur principal."""

    def __init__(self, simulation_mode: bool = True, lang: str = "en"):
        self.llm = get_llm_client()
        self.simulation = simulation_mode
        self.lang = "en"
        self.roles_config = self._load_config("config/roles.yaml")
        self.org_config = self._load_config("config/org_chart.yaml")

    def _load_config(self, path: str) -> dict:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config non trouvée: {path}")
            return {}

    def parse_request(self, user_input: str) -> OnboardingRequest:
        """Utilise le LLM pour parser la demande en langage naturel."""
        available_roles = list(self.roles_config.keys())
        prompt = f"""Message de l'utilisateur: {user_input}

Rôles disponibles: {available_roles}

Extrais les informations et retourne uniquement du JSON valide."""

        response = self.llm.chat(
            system_prompt=PARSE_SYSTEM_PROMPT,
            user_message=prompt,
            temperature=0.1,
        )

        try:
            # Nettoyer la réponse
            text = response["text"].strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0]
            data = json.loads(text)
            return OnboardingRequest(**{k: v for k, v in data.items() if k in OnboardingRequest.__dataclass_fields__})
        except (json.JSONDecodeError, TypeError) as e:
            logger.error(f"Erreur parsing LLM: {e}")
            return OnboardingRequest()

    def _resolve_team_emails(self, request: OnboardingRequest, role_config: dict) -> dict:
        """Résout les emails de l'équipe depuis org_chart.yaml."""
        equipes = self.org_config.get("equipes", {})

        # Trouver l'équipe correspondante
        team_key = request.team.lower().replace(" ", "_") if request.team else role_config.get("departement", "").lower().replace(" ", "_")
        team_data = equipes.get(team_key, {})

        return {
            "manager_email": team_data.get("manager", {}).get("email", "manager@company.com"),
            "team_emails": [m["email"] for m in team_data.get("membres", [])],
            "rh_email": self.org_config.get("rh", {}).get("contact_principal", {}).get("email", "rh@company.com"),
            "it_email": self.org_config.get("it_support", {}).get("contact_principal", {}).get("email", "it@company.com"),
        }

    def _generate_employee_email(self, request: OnboardingRequest) -> str:
        """Génère l'email si non fourni."""
        if request.employee_email:
            return request.employee_email
        domain = os.getenv("COMPANY_DOMAIN", "company.com")
        parts = request.employee_name.lower().split()
        if len(parts) >= 2:
            return f"{parts[0]}.{parts[-1]}@{domain}"
        return f"{parts[0]}@{domain}"

    def run(self, user_input: str, progress_callback=None) -> OnboardingResult:
        """
        Exécute le processus d'onboarding complet.
        progress_callback: fonction appelée à chaque étape (pour le UI)
        """
        result = OnboardingResult()
        lang = self.lang

        def log(agent, action, status="✓", details=""):
            result.add_log(agent, action, status, details)
            if progress_callback:
                progress_callback(agent, action, status, details)

        # ─── Step 1: Parse the request ───
        log("Coordinator", t("log_parsing", lang), "⏳")
        request = self.parse_request(user_input)

        if not request.employee_name or not request.role_key:
            result.status = "error"
            log("Coordinator", t("log_insufficient", lang), "❌",
                t("log_name_role_required", lang))
            return result

        request.employee_email = self._generate_employee_email(request)
        result.request = asdict(request)
        log("Coordinator", f"{t('log_parsed', lang)}: {request.employee_name} - {request.role_key}", "✓")

        # ─── Load role config ───
        role_config = self.roles_config.get(request.role_key, {})
        if not role_config:
            result.status = "error"
            log("Coordinator", f"{t('log_unknown_role', lang)}: {request.role_key}", "❌")
            return result

        team_emails = self._resolve_team_emails(request, role_config)
        log("Coordinator", f"{t('log_config_loaded', lang)}: {role_config.get('titre', request.role_key)}", "✓")

        # ─── Step 2: Create Drive folders ───
        log("Document Generator", t("log_creating_drive", lang), "⏳")
        if self.simulation:
            from mcp_tools.google_drive import simulate_create_onboarding_structure
            folders = simulate_create_onboarding_structure(request.employee_name, request.role_key)
        else:
            from mcp_tools.google_drive import create_onboarding_folder_structure
            folders = create_onboarding_folder_structure(request.employee_name, request.role_key)

        result.drive_folders = folders
        log("Document Generator", f"5 {t('log_folders_created', lang)}", "✓",
            folders.get("root", {}).get("webViewLink", ""))

        # ─── Step 3: Schedule meetings ───
        meetings = role_config.get("reunions_premiere_semaine", [])
        log("Calendar Planner", t("log_scheduling", lang).format(len(meetings)), "⏳")

        if self.simulation:
            from mcp_tools.google_calendar import simulate_schedule_week
            events = simulate_schedule_week(request.employee_name, request.start_date or "2026-03-03", meetings)
        else:
            from mcp_tools.google_calendar import schedule_onboarding_week
            start = datetime.fromisoformat(request.start_date) if request.start_date else datetime.now()
            events = schedule_onboarding_week(request.employee_email, start, meetings, team_emails)

        # Translate meeting summaries for display
        if lang == "en":
            for event in events:
                summary = event.get("summary", "")
                if summary.startswith("[Onboarding] "):
                    meeting_type = summary.replace("[Onboarding] ", "")
                    event["summary"] = f"[Onboarding] {translate_meeting_type(meeting_type, lang)}"

        result.calendar_events = events
        log("Calendar Planner", f"{len(events)} {t('log_meetings_scheduled', lang)}", "✓")

        for event in events:
            summary = event.get("summary", "Meeting")
            log("Calendar Planner", f"  → {summary}", "📅")

        # ─── Step 4: Send emails ───
        log("Communication Manager", t("log_sending_emails", lang), "⏳")
        emails_sent = []

        drive_link = folders.get("root", {}).get("webViewLink", "#")
        checklist_link = "#"

        if self.simulation:
            from mcp_tools.gmail import simulate_send_email
            emails_sent.append(simulate_send_email(
                request.employee_email,
                t("email_welcome_subject", lang).format(name=request.employee_name)))
            emails_sent.append(simulate_send_email(
                team_emails["manager_email"],
                t("email_manager_subject", lang).format(name=request.employee_name)))
            if team_emails["team_emails"]:
                emails_sent.append(simulate_send_email(
                    team_emails["team_emails"][0],
                    t("email_team_subject", lang).format(name=request.employee_name)))
            emails_sent.append(simulate_send_email(
                team_emails["it_email"],
                t("email_it_subject", lang).format(name=request.employee_name)))
        else:
            from mcp_tools.gmail import (send_welcome_email, send_manager_notification,
                                          send_team_announcement, send_it_access_request)
            manager_name = request.manager_name or team_emails.get("manager_email", "").split("@")[0]

            emails_sent.append(send_welcome_email(
                request.employee_name, request.employee_email, manager_name,
                role_config["titre"], request.start_date, drive_link
            ))
            emails_sent.append(send_manager_notification(
                team_emails["manager_email"], manager_name,
                request.employee_name, role_config["titre"], request.start_date, checklist_link
            ))
            if team_emails["team_emails"]:
                emails_sent.append(send_team_announcement(
                    team_emails["team_emails"], request.employee_name,
                    role_config["titre"], request.start_date
                ))
            emails_sent.append(send_it_access_request(
                request.employee_name, role_config["titre"],
                role_config.get("acces_a_provisionner", [])
            ))

        result.emails_sent = emails_sent
        log("Communication Manager", f"{len(emails_sent)} {t('log_emails_sent', lang)}", "✓")
        for email in emails_sent:
            log("Communication Manager", f"  → {email.get('to', '???')}: {email.get('subject', '')}", "📧")

        # ─── Step 5: Create tracking checklist ───
        checklist_data = role_config.get("checklist", {})
        log("Checklist Tracker", t("log_creating_checklist", lang), "⏳")

        if self.simulation:
            from mcp_tools.google_sheets import simulate_create_checklist
            checklist = simulate_create_checklist(request.employee_name, request.role_key, checklist_data)
        else:
            from mcp_tools.google_sheets import create_checklist_sheet
            checklist = create_checklist_sheet(
                request.employee_name, request.role_key,
                checklist_data, folders["suivi"]["id"]
            )

        result.checklist = checklist
        total = checklist.get("total_tasks", sum(len(v) for v in checklist_data.values()))
        log("Checklist Tracker", t("log_checklist_created", lang).format(total), "✓", checklist.get("link", ""))

        # ─── Step 5b: Build structured task list ───
        checklist_tasks = []
        for phase_key, phase_names in PHASE_LABELS.items():
            phase_label = phase_names.get(lang, phase_names["fr"])
            for task_fr in checklist_data.get(phase_key, []):
                checklist_tasks.append({
                    CHECKLIST_COLUMNS["Phase"][lang]: phase_label,
                    CHECKLIST_COLUMNS["Tâche"][lang]: translate_task(task_fr, lang),
                    CHECKLIST_COLUMNS["Statut"][lang]: CHECKLIST_STATUS_TODO[lang],
                })
        result.checklist_tasks = checklist_tasks

        # ─── Step 6: Generate Welcome Book ───
        log("Document Generator", t("log_generating_book", lang), "⏳")
        try:
            jinja_env = jinja2.Environment(
                loader=jinja2.FileSystemLoader("templates"),
                undefined=jinja2.Undefined,
            )
            livret_tpl = jinja_env.get_template("livret_accueil.md")

            equipes = self.org_config.get("equipes", {})
            team_key = request.team.lower().replace(" ", "_") if request.team else role_config.get("departement", "").lower().replace(" ", "_")
            team_data = equipes.get(team_key, {})

            result.welcome_book = livret_tpl.render(
                company_name=self.org_config.get("entreprise", {}).get("nom", "TechCorp"),
                employee_name=request.employee_name,
                role_title=role_config.get("titre", request.role_key),
                team=role_config.get("departement", request.team),
                manager_name=request.manager_name or team_data.get("manager", {}).get("nom", ""),
                manager_email=team_emails["manager_email"],
                start_date=request.start_date,
                access_list=role_config.get("acces_a_provisionner", []),
                meetings=role_config.get("reunions_premiere_semaine", []),
                rh_email=team_emails["rh_email"],
                it_email=team_emails["it_email"],
                generated_date=datetime.now().strftime("%Y-%m-%d %H:%M"),
            )
            log("Document Generator", t("log_book_generated", lang), "✓")
        except Exception as e:
            logger.error(f"Erreur génération livret: {e}")
            result.welcome_book = ""
            log("Document Generator", f"{t('log_book_error', lang)}: {e}", "❌")

        # ─── Step 7: Generate HTML Presentation ───
        log("Document Generator", t("log_generating_pres", lang), "⏳")
        try:
            pres_tpl = jinja_env.get_template("presentation.html")

            team_members = [
                {"nom": m["nom"], "role": m["role"], "email": m["email"]}
                for m in team_data.get("membres", [])
            ]

            result.presentation_html = pres_tpl.render(
                company_name=self.org_config.get("entreprise", {}).get("nom", "TechCorp"),
                employee_name=request.employee_name,
                role_title=role_config.get("titre", request.role_key),
                team=role_config.get("departement", request.team),
                manager_name=request.manager_name or team_data.get("manager", {}).get("nom", ""),
                manager_email=team_emails["manager_email"],
                start_date=request.start_date,
                meetings=role_config.get("reunions_premiere_semaine", []),
                access_list=role_config.get("acces_a_provisionner", []),
                checklist_tasks=checklist_tasks,
                team_members=team_members,
                rh_email=team_emails["rh_email"],
                it_email=team_emails["it_email"],
                generated_date=datetime.now().strftime("%Y-%m-%d %H:%M"),
            )
            log("Document Generator", t("log_pres_generated", lang), "✓")
        except Exception as e:
            logger.error(f"Erreur génération présentation: {e}")
            result.presentation_html = ""
            log("Document Generator", f"{t('log_pres_error', lang)}: {e}", "❌")

        # ─── Done ───
        result.status = "completed"
        log("Coordinator", f"✅ {t('log_complete', lang)}", "🎉")

        return result
