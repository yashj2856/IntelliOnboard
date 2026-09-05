"""
Tool Google Drive - Création de dossiers et fichiers pour l'onboarding.
"""

import os
import logging
from googleapiclient.http import MediaFileUpload
from .google_auth import get_drive_service

logger = logging.getLogger(__name__)

ROOT_FOLDER_ID = os.getenv("GOOGLE_DRIVE_ROOT_FOLDER_ID")


def create_folder(name: str, parent_id: str | None = None) -> dict:
    """Crée un dossier dans Google Drive."""
    service = get_drive_service()
    metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_id:
        metadata["parents"] = [parent_id]
    elif ROOT_FOLDER_ID:
        metadata["parents"] = [ROOT_FOLDER_ID]

    folder = service.files().create(body=metadata, fields="id, name, webViewLink").execute()
    logger.info(f"Dossier créé: {folder['name']} ({folder['id']})")
    return folder


def create_doc_from_template(template_id: str, name: str, folder_id: str) -> dict:
    """Duplique un Google Doc template et le place dans le bon dossier."""
    service = get_drive_service()
    copy = service.files().copy(
        fileId=template_id,
        body={"name": name, "parents": [folder_id]},
        fields="id, name, webViewLink"
    ).execute()
    logger.info(f"Document créé depuis template: {copy['name']}")
    return copy


def upload_file(filepath: str, name: str, folder_id: str, mime_type: str = "application/pdf") -> dict:
    """Upload un fichier dans Google Drive."""
    service = get_drive_service()
    metadata = {"name": name, "parents": [folder_id]}
    media = MediaFileUpload(filepath, mimetype=mime_type)
    file = service.files().create(
        body=metadata, media_body=media, fields="id, name, webViewLink"
    ).execute()
    logger.info(f"Fichier uploadé: {file['name']}")
    return file


def create_onboarding_folder_structure(employee_name: str, role: str) -> dict:
    """
    Crée la structure de dossiers complète pour un nouvel employé.
    Retourne les IDs de tous les dossiers créés.
    """
    safe_name = employee_name.replace(" ", "_")
    root = create_folder(f"Onboarding_{safe_name}_{role}")

    folders = {
        "root": root,
        "admin": create_folder("01_Administratif", root["id"]),
        "technique": create_folder("02_Ressources_Techniques", root["id"]),
        "formations": create_folder("03_Formations", root["id"]),
        "suivi": create_folder("04_Suivi", root["id"]),
    }

    logger.info(f"Structure onboarding créée pour {employee_name}: {root['webViewLink']}")
    return folders


# ============================================
# Mode simulation (sans Google API)
# ============================================

def simulate_create_onboarding_structure(employee_name: str, role: str) -> dict:
    """Simule la création de dossiers (pour démo sans Google API)."""
    safe_name = employee_name.replace(" ", "_")
    base_url = "https://drive.google.com/drive/folders"
    
    return {
        "root": {"id": "sim_root", "name": f"Onboarding_{safe_name}_{role}", "webViewLink": f"{base_url}/simulated_root"},
        "admin": {"id": "sim_admin", "name": "01_Administratif", "webViewLink": f"{base_url}/simulated_admin"},
        "technique": {"id": "sim_tech", "name": "02_Ressources_Techniques", "webViewLink": f"{base_url}/simulated_tech"},
        "formations": {"id": "sim_form", "name": "03_Formations", "webViewLink": f"{base_url}/simulated_formations"},
        "suivi": {"id": "sim_suivi", "name": "04_Suivi", "webViewLink": f"{base_url}/simulated_suivi"},
    }
