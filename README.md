# Infobric Live Headcount Monitor

A Python application that monitors live employee headcount on one or more Infobric construction sites and updates corresponding SharePoint Online lists.

The application continuously checks Infobric for the current number of people on site and only updates SharePoint when the value changes.

---

# Features

- Live headcount monitoring from Infobric
- Supports multiple construction sites
- Automatic SharePoint Online updates
- Updates only when headcount changes
- Automatic Infobric session refresh
- Microsoft Entra authentication for SharePoint

---

# Architecture Overview

The application has two authentication systems:

## Infobric

Authentication is handled through Playwright.

Flow:

```
Infobric username/password
          |
          ▼
     Playwright login
          |
          ▼
 state_infobric.json
          |
          ▼
  Monitor Infobric data
```

A dedicated Infobric account is used.

The browser session is saved so the application does not need to log in every time.

---

## SharePoint

SharePoint authentication uses Microsoft Entra delegated authentication.

Flow:

```
Microsoft Entra login
          |
          ▼
 MSAL token cache
          |
          ▼
 SharePoint REST API
          |
          ▼
 Update SharePoint list
```

SharePoint does not use Playwright authentication.

---

# Project Structure

```
.
├── main.py
├── entra.py
│
├── functions/
│   ├── auth.py
│   ├── config.py
│   ├── exceptions.py
│   ├── infobric.py
│   ├── logger.py
│   ├── playwright_manager.py
│   ├── sharepoint.py
│   └── sharepoint_auth.py
│
├── states/
│   └── state_infobric.json
│
├── .env
│
├── requirements.txt
│
└── README.md
```

---

# Requirements

## Software

- Python 3.11+
- Microsoft account with SharePoint permissions
- Infobric account with access to required sites

## Python packages

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright browser:

```bash
playwright install chromium
```

---

# Configuration

All application settings are stored in:

```
functions/config.py
```

Main settings:

## Infobric

Configure:

- Infobric login URL
- Infobric API endpoint
- Infobric site IDs
- Time zone

Example:

```python
SITES = [
    {
        "name": "Kvandal",
        "infobric_site_id": "XXXXXXXX",

        "sharepoint_site":
        "https://company.sharepoint.com/sites/example",

        "sharepoint_list":
        "On Site Headcount",

        "sharepoint_title":
        "Kvandal"
    }
]
```

Additional sites can be added to the `SITES` list.

---

# Environment Variables

Sensitive information should not be stored in code.

Create a `.env` file:

```
INFOBRIC_USERNAME=username
INFOBRIC_PASSWORD=password

ENTRA_CLIENT_ID=xxxxxxxx
ENTRA_TENANT_ID=xxxxxxxx
```

---

# Authentication Setup

## First Infobric login

If this file does not exist:

```
states/state_infobric.json
```

the application will open Infobric login.

The application will:

1. Open Chromium.
2. Enter username and password.
3. Complete login.
4. Save browser session.

After this, future runs use the saved session.

---

## If Infobric session expires

The application automatically:

1. Detects invalid session.
2. Performs login again.
3. Creates a new state file.
4. Continues monitoring.

---

# Microsoft Entra Authentication

SharePoint authentication uses delegated Microsoft Entra authentication through the Microsoft Authentication Library (MSAL).

Before running the application for the first time, authenticate with Microsoft Entra by running:

```bash
python entra.py
```

The script will prompt you to sign in using your Microsoft account and complete multi-factor authentication (MFA) if required.

After successful authentication, a token cache is created:

```
states/sharepoint_token.bin
```

The application automatically uses this token to authenticate with SharePoint. If the access token expires, MSAL will automatically refresh it using the cached refresh token.

If the token cache is deleted, revoked, or can no longer be refreshed, simply run:

```bash
python entra.py
```

again to create a new token cache.

The SharePoint authentication process does not use Playwright or browser automation.

# Running the Application

Start monitoring:

```bash
python main.py
```

Example output:

```
[12:00:01] Starting Live Monitoring...

Checking Infobric session...

✓ Infobric session valid

Monitoring started.

[13:21:02] 👷 People on the site: 313 
[13:21:03] ✓ Site headcount updated in SharePoint
```

---

# Monitoring Logic

The application does not update SharePoint continuously.

Example:

```
Infobric:

10 people
     |
     ▼
SharePoint update


10 people
     |
     ▼
No update


15 people
     |
     ▼
SharePoint update
```

This reduces unnecessary SharePoint requests.

---

# Application Workflow

```
Start
 |
 ▼
Check Infobric session
 |
 ▼
Create browser context
 |
 ▼
Read headcount
 |
 ▼
Has value changed?
 |
 +---- No
 |       |
 |       ▼
 |   Wait and check again
 |
 +---- Yes
         |
         ▼
 Update SharePoint
         |
         ▼
 Wait for next check
```

---

# Playwright Browser Settings

Chromium is managed in:

```
functions/playwright_manager.py
```

Local development:

```python
HEADLESS = False
```

allows seeing the browser.

Production environments such as Azure:

```python
HEADLESS = True
```

should be used.

Chromium runs with:

```python
args=[
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
```

because container environments have restricted permissions and limited shared memory.

---

# Troubleshooting

## "No cached SharePoint account found"

The MSAL token cache is missing.

Run the authentication process again.

---

## "Infobric login required"

Delete:

```
states/state_infobric.json
```

and restart.

The application will create a new session.

---

## SharePoint update errors

Check:

1. SharePoint list name
2. Column internal names
3. User permissions
4. Microsoft Entra application permissions

---

## Playwright cannot find login fields

Infobric may have changed the login page.

Update selectors in:

```
functions/auth.py
```

---

# Adding a New Construction Site

Add a new entry:

```python
SITES = [
    {
        "name": "New Site",
        "infobric_site_id": "SITE_ID",
        "sharepoint_site": "...",
        "sharepoint_list": "...",
        "sharepoint_title": "..."
    }
]
```

No code changes are required.

---

# Deployment

The application is designed to run as a background service.

Possible deployment options:

- Azure Container Apps
- Azure Virtual Machine
- Docker container

Azure deployment requires:

- Python runtime
- Chromium support
- Environment variables/secrets
- Persistent storage for Infobric session state

---

## License

This project is proprietary software owned by CTS Nordics.
The source code is for authorized internal company use only.

---

## Author

Developed for **CTS Nordics** by **Vytautas Labanauskas** to automate subcontractor activity reporting and Power BI dashboard generation from Infobric workforce data. 

huh