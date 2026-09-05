"""
Tool Google Calendar - Planification des réunions d'onboarding.
"""

import logging
from datetime import datetime, timedelta
from .google_auth import get_calendar_service

logger = logging.getLogger(__name__)


def create_event(
    summary: str,
    description: str,
    start_time: datetime,
    duration_minutes: int,
    attendees: list[str],
    calendar_id: str = "primary",
) -> dict:
    """Crée un événement dans Google Calendar."""
    service = get_calendar_service()

    end_time = start_time + timedelta(minutes=duration_minutes)

    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_time.isoformat(), "timeZone": "Europe/Paris"},
        "end": {"dateTime": end_time.isoformat(), "timeZone": "Europe/Paris"},
        "attendees": [{"email": email} for email in attendees],
        "reminders": {"useDefault": True},
    }

    result = service.events().insert(
        calendarId=calendar_id, body=event, sendUpdates="all"
    ).execute()

    logger.info(f"Événement créé: {summary} ({result.get('htmlLink', '')})")
    return result


def get_free_busy(email: str, start: datetime, end: datetime) -> list[dict]:
    """Vérifie les disponibilités d'une personne."""
    service = get_calendar_service()

    body = {
        "timeMin": start.isoformat() + "Z",
        "timeMax": end.isoformat() + "Z",
        "items": [{"id": email}],
    }

    result = service.freebusy().query(body=body).execute()
    return result.get("calendars", {}).get(email, {}).get("busy", [])


def find_free_slot(
    attendees: list[str],
    target_date: datetime,
    duration_minutes: int,
    start_hour: int = 9,
    end_hour: int = 18,
) -> datetime | None:
    """
    Trouve le premier créneau libre commun entre les participants.
    Cherche entre start_hour et end_hour.
    """
    service = get_calendar_service()

    day_start = target_date.replace(hour=start_hour, minute=0, second=0)
    day_end = target_date.replace(hour=end_hour, minute=0, second=0)

    body = {
        "timeMin": day_start.isoformat() + "Z",
        "timeMax": day_end.isoformat() + "Z",
        "items": [{"id": email} for email in attendees],
    }

    result = service.freebusy().query(body=body).execute()

    # Collecter tous les créneaux occupés
    busy_slots = []
    for email in attendees:
        slots = result.get("calendars", {}).get(email, {}).get("busy", [])
        busy_slots.extend(slots)

    # Chercher le premier créneau libre
    current = day_start
    while current + timedelta(minutes=duration_minutes) <= day_end:
        slot_end = current + timedelta(minutes=duration_minutes)
        is_free = True
        for busy in busy_slots:
            busy_start = datetime.fromisoformat(busy["start"].replace("Z", ""))
            busy_end = datetime.fromisoformat(busy["end"].replace("Z", ""))
            if current < busy_end and slot_end > busy_start:
                is_free = False
                current = busy_end
                break
        if is_free:
            return current
        current += timedelta(minutes=30)

    return None


def schedule_onboarding_week(
    employee_email: str,
    start_date: datetime,
    meetings: list[dict],
    team_emails: dict,
) -> list[dict]:
    """
    Planifie toute la première semaine d'onboarding.
    meetings: liste de dicts avec type, duree_minutes, jour, description
    team_emails: dict avec manager_email, team_emails, rh_email, it_email
    """
    created_events = []

    for meeting in meetings:
        day_offset = meeting["jour"] - 1
        meeting_date = start_date + timedelta(days=day_offset)

        # Déterminer les participants selon le type de réunion
        attendees = [employee_email]
        if "manager" in meeting["type"].lower() or "1:1" in meeting["type"].lower():
            attendees.append(team_emails.get("manager_email", ""))
        elif "équipe" in meeting["type"].lower() or "déjeuner" in meeting["type"].lower():
            attendees.extend(team_emails.get("team_emails", []))
        elif "rh" in meeting["type"].lower():
            attendees.append(team_emails.get("rh_email", ""))
        elif "setup" in meeting["type"].lower() or "technique" in meeting["type"].lower():
            attendees.append(team_emails.get("it_email", ""))
        else:
            attendees.append(team_emails.get("manager_email", ""))

        # Trouver un créneau libre
        slot = find_free_slot(attendees, meeting_date, meeting["duree_minutes"])

        if slot:
            event = create_event(
                summary=f"[Onboarding] {meeting['type']}",
                description=meeting.get("description", ""),
                start_time=slot,
                duration_minutes=meeting["duree_minutes"],
                attendees=attendees,
            )
            created_events.append(event)
        else:
            # Fallback: placer à 10h par défaut
            fallback_time = meeting_date.replace(hour=10, minute=0)
            event = create_event(
                summary=f"[Onboarding] {meeting['type']}",
                description=meeting.get("description", ""),
                start_time=fallback_time,
                duration_minutes=meeting["duree_minutes"],
                attendees=attendees,
            )
            created_events.append(event)

    return created_events


# ============================================
# Mode simulation
# ============================================

def simulate_schedule_week(employee_name: str, start_date: str, meetings: list[dict]) -> list[dict]:
    """Simule la planification d'une semaine d'onboarding."""
    events = []
    base = datetime.fromisoformat(start_date) if isinstance(start_date, str) else start_date
    hour = 9

    for meeting in meetings:
        day_offset = meeting.get("jour", 1) - 1
        event_date = base + timedelta(days=day_offset)
        events.append({
            "id": f"sim_event_{len(events)}",
            "summary": f"[Onboarding] {meeting['type']}",
            "start": event_date.replace(hour=hour).isoformat(),
            "duration": meeting["duree_minutes"],
            "description": meeting.get("description", ""),
            "status": "simulated",
        })
        hour += 2
        if hour > 17:
            hour = 9

    logger.info(f"[SIMULATION] {len(events)} événements planifiés pour {employee_name}")
    return events
