# 🔐 Codveda Identity — Django Authentication Platform

> **Level 3 · Task 1 — Python Development Internship**

A polished Django web application demonstrating registration, login/logout, protected pages, role-aware access, profile management, and password reset using Django's authentication framework.

## ✨ Features
- 👤 User registration with validation
- 🔑 Login and logout
- 🛡️ Login-protected dashboard and profile
- 🧩 Staff, superuser and group-aware role display
- 🔄 Complete password reset flow
- 🎨 Responsive custom UI
- 🗄️ SQLite local development
- ⚙️ Environment-based email/security settings

## 🎯 Codveda requirements

| Requirement | Implementation |
|---|---|
| Registration | Custom registration form |
| Login / Logout | Django authentication views |
| Authentication | Session-based Django authentication |
| Roles / Permissions | Staff, superuser and groups |
| Password reset | Complete Django reset workflow |
| Web app | Protected dashboard + profile |

## 🏗️ Flow
~~~text
Browser
  ↓
Django URLs
  ├── accounts/ → Register · Login · Logout · Profile · Password Reset
  └── dashboard/ → Protected workspace
  ↓
Django Authentication
  ↓
SQLite
~~~

## 🚀 Setup
~~~bash
git clone https://github.com/Bandhan-lab/codveda-python-level3-django.git
cd codveda-python-level3-django
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
~~~

Open http://127.0.0.1:8000/.

## 🧪 Tests
~~~bash
python manage.py check
python manage.py test
~~~

## 📁 Structure
~~~text
accounts/       # authentication and account flows
config/         # Django configuration
dashboard/      # protected dashboard
templates/      # authentication and dashboard UI
static/css/     # responsive styling
tests/          # authentication tests
manage.py
requirements.txt
.env.example
~~~

## 📧 Password reset
Local development uses Django's console email backend, so reset messages appear in the terminal. SMTP variables are provided in .env.example for real email delivery.

## 🛡️ Security
Do not commit production secrets. Use environment variables and set DEBUG=0 with restricted hosts when deploying.

## 🧠 Skills
**Python · Django · Authentication · Sessions · Permissions · Forms · Templates · HTML · CSS · SQLite · Testing · Git/GitHub**

## 📌 Status
**Level 3 Task 1 — Core implementation complete.**

Built for the **Codveda Technology Python Development Internship**.

### Author
**Bandhan Kumar Sahoo**  
CSE (AI & ML) · GITA Autonomous College, Bhubaneswar
