"""
Tool Google Sheets - Création et suivi de la checklist d'onboarding.
"""

import logging
from .google_auth import get_sheets_service, get_drive_service

logger = logging.getLogger(__name__)


def create_checklist_sheet(employee_name: str, role: str, checklist: dict, folder_id: str) -> dict:
    """
    Crée un Google Sheet de suivi dans le dossier onboarding.
    checklist: dict avec clés avant_arrivee, jour_1, semaine_1, mois_1
    """
    sheets_service = get_sheets_service()
    drive_service = get_drive_service()

    # Créer le spreadsheet
    spreadsheet = sheets_service.spreadsheets().create(
        body={
            "properties": {"title": f"Checklist Onboarding - {employee_name}"},
            "sheets": [{"properties": {"title": "Suivi"}}],
        }
    ).execute()

    spreadsheet_id = spreadsheet["spreadsheetId"]
    sheet_id = spreadsheet["sheets"][0]["properties"]["sheetId"]

    # Déplacer dans le bon dossier
    file = drive_service.files().get(fileId=spreadsheet_id, fields="parents").execute()
    previous_parents = ",".join(file.get("parents", []))
    drive_service.files().update(
        fileId=spreadsheet_id,
        addParents=folder_id,
        removeParents=previous_parents,
    ).execute()

    # Remplir la checklist
    rows = [["Phase", "Tâche", "Responsable", "Deadline", "Statut", "Notes"]]

    phase_labels = {
        "avant_arrivee": "Avant l'arrivée",
        "jour_1": "Jour 1",
        "semaine_1": "Semaine 1",
        "mois_1": "Mois 1",
    }

    for phase_key, phase_label in phase_labels.items():
        tasks = checklist.get(phase_key, [])
        for task in tasks:
            rows.append([phase_label, task, "", "", "⬜ À faire", ""])

    sheets_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range="Suivi!A1",
        valueInputOption="RAW",
        body={"values": rows},
    ).execute()

    # Formatage basique
    _format_checklist(sheets_service, spreadsheet_id, sheet_id)

    link = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
    logger.info(f"Checklist créée: {link}")

    return {"id": spreadsheet_id, "link": link, "name": f"Checklist Onboarding - {employee_name}"}


def _format_checklist(service, spreadsheet_id: str, sheet_id: int = 0):
    """Applique un formatage basique à la checklist."""
    requests = [
        # Header en gras + fond bleu
        {
            "repeatCell": {
                "range": {"sheetId": sheet_id, "startRowIndex": 0, "endRowIndex": 1},
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
                        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat)",
            }
        },
        # Auto-resize colonnes
        {"autoResizeDimensions": {"dimensions": {"sheetId": sheet_id, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 6}}},
    ]

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id, body={"requests": requests}
    ).execute()


# ============================================
# Mode simulation
# ============================================

def simulate_create_checklist(employee_name: str, role: str, checklist: dict) -> dict:
    """Simule la création d'une checklist Google Sheets."""
    total_tasks = sum(len(tasks) for tasks in checklist.values())
    logger.info(f"[SIMULATION] Checklist créée pour {employee_name}: {total_tasks} tâches")
    return {
        "id": "sim_sheet_001",
        "link": "https://docs.google.com/spreadsheets/d/simulated_checklist",
        "name": f"Checklist Onboarding - {employee_name}",
        "total_tasks": total_tasks,
    }