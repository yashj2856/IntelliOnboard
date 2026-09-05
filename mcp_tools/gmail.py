"""
Tool Gmail - Envoi d'emails pour l'onboarding.
"""

import base64
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .google_auth import get_gmail_service

logger = logging.getLogger(__name__)


def send_email(to: str, subject: str, body_html: str, cc: list[str] | None = None) -> dict:
    """Envoie un email via Gmail API."""
    service = get_gmail_service()

    message = MIMEMultipart("alternative")
    message["to"] = to
    message["subject"] = subject
    if cc:
        message["cc"] = ", ".join(cc)

    message.attach(MIMEText(body_html, "html"))

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    result = service.users().messages().send(
        userId="me", body={"raw": raw}
    ).execute()

    logger.info(f"Email envoyé à {to}: {subject} (id: {result['id']})")
    return result


def send_welcome_email(employee_name: str, employee_email: str, manager_name: str, 
                        role: str, start_date: str, drive_link: str) -> dict:
    """Send the welcome email to the new employee."""
    subject = f"Welcome to the team, {employee_name}! 🎉"
    body = f"""
    <html><body style="font-family: Arial, sans-serif; line-height: 1.6;">
    <h2>Welcome, {employee_name}!</h2>
    <p>We are delighted to welcome you as <strong>{role}</strong>, 
    starting on <strong>{start_date}</strong>.</p>
    
    <p>Your manager, <strong>{manager_name}</strong>, is looking forward to your first day. 
    Here is what you need to know:</p>
    
    <h3>📁 Your onboarding workspace</h3>
    <p>All your documents are available here: <a href="{drive_link}">{drive_link}</a></p>
    
    <h3>📅 Your first week</h3>
    <p>Your detailed schedule is available in your Google Calendar. 
    The invitations have already been sent.</p>
    
    <h3>✅ Before your arrival</h3>
    <ul>
        <li>Verify that you can access your Google Workspace account</li>
        <li>Read the welcome book in your Drive folder</li>
        <li>Contact {manager_name} if you have any questions</li>
    </ul>
    
    <p>See you soon!<br>The HR team</p>
    </body></html>
    """
    return send_email(employee_email, subject, body)


def send_manager_notification(manager_email: str, manager_name: str, employee_name: str,
                               role: str, start_date: str, checklist_link: str) -> dict:
    """Notify the manager about the new employee's arrival."""
    subject = f"[Onboarding] {employee_name} is joining on {start_date}"
    body = f"""
    <html><body style="font-family: Arial, sans-serif; line-height: 1.6;">
    <h2>New team member</h2>
    <p>Hello {manager_name},</p>
    <p><strong>{employee_name}</strong> is joining your team as <strong>{role}</strong> 
    on <strong>{start_date}</strong>.</p>
    
    <h3>📋 Your manager checklist</h3>
    <p>Track everything here: <a href="{checklist_link}">{checklist_link}</a></p>
    
    <h3>Actions required before {start_date}:</h3>
    <ul>
        <li>Prepare the workstation</li>
        <li>Identify a buddy</li>
        <li>Prepare 30/60/90-day goals</li>
        <li>Block time for the first week</li>
    </ul>
    
    <p>The first-week meetings have been automatically scheduled in your calendar.</p>
    </body></html>
    """
    return send_email(manager_email, subject, body)


def send_team_announcement(team_emails: list[str], employee_name: str, role: str,
                            start_date: str, fun_fact: str = "") -> dict:
    """Announce the new employee to the team."""
    subject = f"🎉 New team member: {employee_name} is joining the team!"
    body = f"""
    <html><body style="font-family: Arial, sans-serif; line-height: 1.6;">
    <h2>New team member!</h2>
    <p><strong>{employee_name}</strong> is joining us as <strong>{role}</strong> 
    starting on <strong>{start_date}</strong>.</p>
    {f'<p>Fun fact: {fun_fact}</p>' if fun_fact else ''}
    <p>A team lunch is planned to welcome them. 
    The invitation is in your calendars.</p>
    <p>Stop by and say hello! 👋</p>
    </body></html>
    """
    return send_email(team_emails[0], subject, body, cc=team_emails[1:])


def send_it_access_request(employee_name: str, role: str, access_list: list[str]) -> dict:
    """Send the IT access request."""
    import os
    it_email = os.getenv("IT_SUPPORT_EMAIL", "it-support@company.com")
    
    access_html = "".join(f"<li>{access}</li>" for access in access_list)
    subject = f"[Onboarding] Access request - {employee_name} ({role})"
    body = f"""
    <html><body style="font-family: Arial, sans-serif; line-height: 1.6;">
    <h2>Access provisioning request</h2>
    <p><strong>Employee:</strong> {employee_name}<br>
    <strong>Role:</strong> {role}</p>
    
    <h3>Access to provision:</h3>
    <ul>{access_html}</ul>
    
    <p>Please provision these accesses before the start date.</p>
    </body></html>
    """
    return send_email(it_email, subject, body)


# ============================================
# Mode simulation
# ============================================

def simulate_send_email(to: str, subject: str, body_html: str = "", cc: list[str] | None = None) -> dict:
    """Simule l'envoi d'un email."""
    logger.info(f"[SIMULATION] Email → {to} | Sujet: {subject}")
    return {"id": "sim_msg_001", "to": to, "subject": subject, "status": "simulated"}
