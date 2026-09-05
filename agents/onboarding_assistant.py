"""
Assistant d'Onboarding Personnel.
Chaque employé onboardé a accès à un chatbot dédié qui connaît :
- Sa fiche de poste
- Son planning de première semaine
- Sa checklist et son avancement
- Le livret d'accueil personnalisé
- Les contacts de son équipe
- Les procédures internes

Le contexte est injecté dynamiquement à chaque message (pas de mémoire persistante).
Le state vit dans Google Sheets / Drive, l'assistant le lit à chaque interaction.
"""

import os
import yaml
import json
import logging
from datetime import datetime
from dataclasses import dataclass, field

from llm_client import get_llm_client

logger = logging.getLogger(__name__)


@dataclass
class EmployeeContext:
    """Contexte complet d'un employé onboardé."""
    employee_name: str = ""
    employee_email: str = ""
    role_key: str = ""
    role_title: str = ""
    team: str = ""
    manager_name: str = ""
    manager_email: str = ""
    start_date: str = ""
    # Contenu injecté
    fiche_poste: str = ""
    livret_accueil: str = ""
    checklist_status: list = field(default_factory=list)
    calendar_events: list = field(default_factory=list)
    team_members: list = field(default_factory=list)
    access_list: list = field(default_factory=list)
    formations: list = field(default_factory=list)
    tools_to_install: list = field(default_factory=list)
    company_name: str = ""
    # Métadonnées
    onboarding_day: int = 0  # J+0, J+1, J+2...


ASSISTANT_SYSTEM_PROMPT_FR = """Tu es l'assistant d'onboarding personnel de {employee_name}, qui vient de rejoindre {company_name} en tant que {role_title} dans l'équipe {team}.

Tu es chaleureux, professionnel et proactif. Tu connais TOUT le contexte de son onboarding et tu réponds en français.

Ton rôle :
- Répondre à toutes les questions sur l'entreprise, l'équipe, les outils, les processus
- Guider l'employé dans ses premiers jours (quoi faire, qui contacter, où trouver les infos)
- Vérifier l'avancement de sa checklist et l'encourager
- Donner des conseils pratiques pour bien s'intégrer
- Rediriger vers la bonne personne si tu ne sais pas répondre

Règles :
- Si tu ne connais pas la réponse, dis-le honnêtement et suggère qui contacter
- Ne fabrique jamais d'information — base-toi uniquement sur le contexte fourni
- Sois concis et actionnable dans tes réponses
- Utilise un ton amical mais professionnel (tutoiement OK)

Nous sommes actuellement à J+{onboarding_day} de l'onboarding.

═══════════════════════════════════════
CONTEXTE DE L'ONBOARDING
═══════════════════════════════════════

📋 FICHE DE POSTE :
{fiche_poste}

📅 PLANNING PREMIÈRE SEMAINE :
{calendar_events}

☑️ CHECKLIST ET AVANCEMENT :
{checklist_status}

👥 ÉQUIPE :
Manager : {manager_name} ({manager_email})
Membres :
{team_members}

🔐 ACCÈS À PROVISIONNER :
{access_list}

📚 FORMATIONS OBLIGATOIRES :
{formations}

🛠️ OUTILS À INSTALLER :
{tools_to_install}

📖 LIVRET D'ACCUEIL :
{livret_accueil}
"""

ASSISTANT_SYSTEM_PROMPT_EN = """You are the personal onboarding assistant for {employee_name}, who just joined {company_name} as a {role_title} on the {team} team.

You are warm, professional, and proactive. You know ALL the context of their onboarding and you answer in English.

Your role:
- Answer all questions about the company, team, tools, and processes
- Guide the employee through their first days (what to do, who to contact, where to find info)
- Check checklist progress and encourage them
- Give practical advice for successful integration
- Redirect to the right person if you don't know the answer

Rules:
- If you don't know the answer, say so honestly and suggest who to contact
- Never make up information — only use the provided context
- Be concise and actionable in your answers
- Use a friendly but professional tone

We are currently at Day {onboarding_day} of onboarding.

═══════════════════════════════════════
ONBOARDING CONTEXT
═══════════════════════════════════════

📋 JOB DESCRIPTION:
{fiche_poste}

📅 FIRST WEEK SCHEDULE:
{calendar_events}

☑️ CHECKLIST & PROGRESS:
{checklist_status}

👥 TEAM:
Manager: {manager_name} ({manager_email})
Members:
{team_members}

🔐 ACCESS TO PROVISION:
{access_list}

📚 MANDATORY TRAINING:
{formations}

🛠️ TOOLS TO INSTALL:
{tools_to_install}

📖 WELCOME BOOK:
{livret_accueil}
"""


class OnboardingAssistant:
    """Assistant conversationnel dédié à un employé onboardé."""

    def __init__(self, employee_id: str, simulation_mode: bool = True, lang: str = "en"):
        """
        employee_id: identifiant unique (ex: "sarah_martin_data_engineer")
        lang: "fr" or "en" — controls assistant response language.
        Charge le contexte depuis les fichiers de config + Google Sheets (ou simulation).
        """
        self.llm = get_llm_client()
        self.simulation = simulation_mode
        self.lang = "en"
        self.employee_id = employee_id
        self.conversation_history: list[dict] = []
        self.context = self._load_context(employee_id)

    def _load_config(self, path: str) -> dict:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return {}

    def _load_template(self, path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def _load_context(self, employee_id: str) -> EmployeeContext:
        """
        Charge le contexte complet de l'employé.
        En production : lit depuis Google Sheets/Drive.
        En simulation : charge depuis les fichiers locaux.
        """
        roles_config = self._load_config("config/roles.yaml")
        org_config = self._load_config("config/org_chart.yaml")

        # En simulation, on utilise un contexte par défaut basé sur l'employee_id
        # En production, on lirait depuis un registre (Sheet ou DB)
        employee_registry = self._load_employee_registry()
        employee_data = employee_registry.get(employee_id, {})

        role_key = employee_data.get("role_key", "data_engineer")
        role_config = roles_config.get(role_key, {})
        team_key = employee_data.get("team_key", "data_platform")
        team_config = org_config.get("equipes", {}).get(team_key, {})

        # Charger la fiche de poste
        fiche_path = f"templates/fiches_poste/{role_key}.md"
        fiche_poste = self._load_template(fiche_path)

        # Charger le livret d'accueil
        livret = self._load_template("templates/livret_accueil.md")

        # Calculer le jour d'onboarding
        start_date = employee_data.get("start_date", "2026-03-03")
        try:
            start = datetime.fromisoformat(start_date)
            onboarding_day = (datetime.now() - start).days
        except (ValueError, TypeError):
            onboarding_day = 0

        # Construire la checklist avec statuts
        checklist_status = self._get_checklist_status(employee_id, role_config.get("checklist", {}))

        # Formater les événements calendrier
        calendar_events = self._format_meetings(role_config.get("reunions_premiere_semaine", []), start_date)

        # Membres de l'équipe
        team_members = [
            f"- {m['nom']} ({m['role']}) — {m['email']}"
            for m in team_config.get("membres", [])
        ]

        context = EmployeeContext(
            employee_name=employee_data.get("name", "Nouvel employé"),
            employee_email=employee_data.get("email", ""),
            role_key=role_key,
            role_title=role_config.get("titre", role_key),
            team=role_config.get("departement", ""),
            manager_name=team_config.get("manager", {}).get("nom", ""),
            manager_email=team_config.get("manager", {}).get("email", ""),
            start_date=start_date,
            fiche_poste=fiche_poste or "Non disponible",
            livret_accueil=livret or "Non disponible",
            checklist_status=checklist_status,
            calendar_events=calendar_events,
            team_members=team_members,
            access_list=role_config.get("acces_a_provisionner", []),
            formations=role_config.get("formations_obligatoires", []),
            tools_to_install=role_config.get("outils_a_installer", []),
            company_name=os.getenv("COMPANY_NAME", org_config.get("entreprise", {}).get("nom", "L'entreprise")),
            onboarding_day=max(onboarding_day, 0),
        )

        return context

    def _load_employee_registry(self) -> dict:
        """
        Charge le registre des employés onboardés.
        En production : lit depuis Google Sheets.
        En simulation : retourne des données d'exemple.
        """
        if self.simulation:
            return {
                "sarah_martin_data_engineer": {
                    "name": "Sarah Martin",
                    "email": "sarah.martin@techcorp.com",
                    "role_key": "data_engineer",
                    "team_key": "data_platform",
                    "start_date": "2026-03-03",
                },
                "thomas_legrand_fullstack": {
                    "name": "Thomas Legrand",
                    "email": "thomas.legrand@techcorp.com",
                    "role_key": "developpeur_fullstack",
                    "team_key": "engineering",
                    "start_date": "2026-03-10",
                },
                "claire_rousseau_commercial": {
                    "name": "Claire Rousseau",
                    "email": "claire.rousseau@techcorp.com",
                    "role_key": "commercial",
                    "team_key": "sales",
                    "start_date": "2026-03-17",
                },
            }
        else:
            # Production: lire depuis Google Sheets
            # TODO: Implémenter la lecture du registre
            return {}

    def _get_checklist_status(self, employee_id: str, checklist_config: dict) -> list[dict]:
        """
        Récupère le statut actuel de la checklist.
        En production : lit depuis Google Sheets.
        En simulation : génère un état partiel réaliste.
        """
        items = []
        phase_labels = {
            "avant_arrivee": "Avant l'arrivée",
            "jour_1": "Jour 1",
            "semaine_1": "Semaine 1",
            "mois_1": "Mois 1",
        }

        if self.simulation:
            # Simuler un avancement partiel basé sur le jour d'onboarding
            for phase_key, phase_label in phase_labels.items():
                tasks = checklist_config.get(phase_key, [])
                for i, task in enumerate(tasks):
                    # Avant arrivée: tout fait. Jour 1: partiellement. Le reste: à faire.
                    if phase_key == "avant_arrivee":
                        status = "✅ Fait"
                    elif phase_key == "jour_1" and i < 2:
                        status = "✅ Fait"
                    elif phase_key == "jour_1":
                        status = "🔄 En cours"
                    else:
                        status = "⬜ À faire"
                    items.append({"phase": phase_label, "task": task, "status": status})
        else:
            # Production: lire depuis Google Sheets
            # TODO: Implémenter la lecture du Sheet
            for phase_key, phase_label in phase_labels.items():
                tasks = checklist_config.get(phase_key, [])
                for task in tasks:
                    items.append({"phase": phase_label, "task": task, "status": "⬜ À faire"})

        return items

    def _format_meetings(self, meetings: list[dict], start_date: str) -> list[dict]:
        """Formate les réunions pour le contexte."""
        formatted = []
        for m in meetings:
            formatted.append({
                "jour": f"Jour {m.get('jour', '?')}",
                "type": m.get("type", ""),
                "duree": f"{m.get('duree_minutes', '?')} min",
                "description": m.get("description", ""),
            })
        return formatted

    def _build_system_prompt(self) -> str:
        """Construit le system prompt avec tout le contexte injecté."""
        ctx = self.context

        # Formater la checklist
        checklist_str = "\n".join(
            f"  [{item['status']}] ({item['phase']}) {item['task']}"
            for item in ctx.checklist_status
        )

        # Formater le calendrier
        calendar_str = "\n".join(
            f"  {e['jour']} — {e['type']} ({e['duree']}) : {e['description']}"
            for e in ctx.calendar_events
        )

        # Formater les listes
        team_str = "\n".join(ctx.team_members) if ctx.team_members else "Non disponible"
        access_str = "\n".join(f"  - {a}" for a in ctx.access_list) if ctx.access_list else "Non disponible"
        formations_str = "\n".join(f"  - {f}" for f in ctx.formations) if ctx.formations else "Non disponible"
        tools_str = "\n".join(f"  - {t}" for t in ctx.tools_to_install) if ctx.tools_to_install else "Non disponible"

        template = ASSISTANT_SYSTEM_PROMPT_EN if self.lang == "en" else ASSISTANT_SYSTEM_PROMPT_FR
        return template.format(
            employee_name=ctx.employee_name,
            company_name=ctx.company_name,
            role_title=ctx.role_title,
            team=ctx.team,
            onboarding_day=ctx.onboarding_day,
            fiche_poste=ctx.fiche_poste,
            calendar_events=calendar_str,
            checklist_status=checklist_str,
            manager_name=ctx.manager_name,
            manager_email=ctx.manager_email,
            team_members=team_str,
            access_list=access_str,
            formations=formations_str,
            tools_to_install=tools_str,
            livret_accueil=ctx.livret_accueil[:3000],  # Tronquer si trop long
        )

    def chat(self, user_message: str) -> str:
        """
        Envoie un message et retourne la réponse de l'assistant.
        Maintient l'historique de conversation pour le contexte multi-turn.
        """
        self.conversation_history.append({
            "role": "user",
            "content": user_message,
        })

        system_prompt = self._build_system_prompt()

        # Appeler le LLM avec l'historique complet
        if self.llm.provider == "anthropic":
            response = self.llm._client.messages.create(
                model=self.llm._model,
                max_tokens=2048,
                temperature=0.4,
                system=system_prompt,
                messages=self.conversation_history,
            )
            assistant_message = response.content[0].text
        else:
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(self.conversation_history)
            response = self.llm._client.chat.completions.create(
                model=self.llm._model,
                temperature=0.4,
                messages=messages,
            )
            assistant_message = response.choices[0].message.content

        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message,
        })

        # Garder un historique raisonnable (derniers 20 échanges)
        if len(self.conversation_history) > 40:
            self.conversation_history = self.conversation_history[-40:]

        return assistant_message

    def get_status_summary(self) -> str:
        """Génère un résumé de l'avancement de l'onboarding."""
        ctx = self.context
        total = len(ctx.checklist_status)
        done = sum(1 for item in ctx.checklist_status if "Fait" in item["status"])
        in_progress = sum(1 for item in ctx.checklist_status if "En cours" in item["status"])

        return (
            f"📊 Onboarding de {ctx.employee_name} — J+{ctx.onboarding_day}\n"
            f"   Progression : {done}/{total} tâches complétées, {in_progress} en cours\n"
            f"   Poste : {ctx.role_title} — Équipe : {ctx.team}\n"
            f"   Manager : {ctx.manager_name}"
        )

    def refresh_context(self):
        """
        Rafraîchit le contexte depuis les sources (Google Sheets, etc.).
        Utile si la checklist a été mise à jour manuellement.
        """
        self.context = self._load_context(self.employee_id)
        logger.info(f"Contexte rafraîchi pour {self.employee_id}")
