"""
Worker Celery pour l'exécution asynchrone des agents.
Utile en mode production pour ne pas bloquer l'interface.
"""

import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    "onboarding",
    broker=os.getenv("REDIS_URL", "redis://redis:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://redis:6379/0"),
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Paris",
    task_track_started=True,
    result_expires=3600,
)


@celery_app.task(bind=True, name="run_onboarding")
def run_onboarding_task(self, user_input: str, simulation: bool = True):
    """Tâche Celery pour exécuter l'onboarding en arrière-plan."""
    from agents.coordinator import Coordinator

    logs = []

    def callback(agent, action, status, details):
        logs.append({"agent": agent, "action": action, "status": status, "details": details})
        self.update_state(state="PROGRESS", meta={"logs": logs})

    coordinator = Coordinator(simulation_mode=simulation)
    result = coordinator.run(user_input, progress_callback=callback)

    return {
        "status": result.status,
        "request": result.request,
        "drive_folders": result.drive_folders,
        "calendar_events": result.calendar_events,
        "emails_sent": result.emails_sent,
        "checklist": result.checklist,
        "logs": result.logs,
    }
