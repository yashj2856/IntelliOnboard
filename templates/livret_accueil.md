# Welcome Book — {{ company_name }}

Welcome **{{ employee_name }}**! 🎉

## 🏢 About the company

{{ company_name }} is a technology company specializing in cloud and data solutions.
We currently have 250 employees across three locations (Paris, Lyon, Nantes).

**Our mission:** Help companies turn data into decisions through reliable, high-performance platforms.

**Our values:**
- Technical excellence
- Collaboration and transparency
- Impact and innovation
- Kindness

## 👤 Your role

- **Title:** {{ role_title }}
- **Team:** {{ team }}
- **Manager:** {{ manager_name }}
- **Start date:** {{ start_date }}

## 📍 Practical information

### Working hours and attendance
- Flexible hours: start between 8:30 and 10:00
- Hybrid policy: three days in the office, two remote days
- Required office days: Tuesday and Thursday

### Office access
- Address: 42 avenue de la Grande Armée, 75017 Paris
- Badge: collect it at reception on your first day
- Wi-Fi: network `{{ company_name }}-Corp` / password provided by IT

### Tools and access
Your access will be configured before your arrival:
{% for access in access_list %}
- {{ access }}
{% endfor %}

## 📅 Your first week

{% for meeting in meetings %}
### Day {{ meeting.jour }} — {{ meeting.type }}
- **Duration:** {{ meeting.duree_minutes }} minutes
- **Description:** {{ meeting.description }}
{% endfor %}

## 📋 Your first goals

### By day 30
- Understand the organization and processes
- Meet key stakeholders
- Deliver a first contribution

### By day 60
- Work independently on your main responsibilities
- Identify areas for improvement

### By day 90
- Be fully operational
- Actively contribute to team goals

## 📞 Useful contacts

| Qui | Email |
|-----|-------|
| Your manager | {{ manager_email }} |
| HR | {{ rh_email }} |
| IT Support | {{ it_email }} |

## ❓ FAQ

**How do I request time off?**
Use Lucca (Timmi Absences). Requests must be approved by your manager.

**How do I request remote work?**
Use Lucca (Timmi Absences) at least 24 hours in advance.

**Who should I contact about a technical issue?**
Slack: #it-support or email: {{ it_email }}

---

*This document was generated automatically by the Onboarding Agent.*
*Last updated: {{ generated_date }}*
