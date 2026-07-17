"""
---------------------------------------------------
Configuration

Author: Vytautas Labanauskas

Purpose:
Contains all configurable application settings.

Sensitive values are loaded from the project's
.env file.

To monitor additional construction sites, simply
add another entry to the SITES list.

---------------------------------------------------
"""

import os

from dotenv import load_dotenv


# ==================================================
# LOAD ENVIRONMENT VARIABLES
# ==================================================

load_dotenv()


# ==================================================
# APPLICATION
# ==================================================

# Run Playwright in headless mode.
# Set to False only for local debugging.
HEADLESS = True

# Polling interval (seconds)
POLL_INTERVAL = 5


# ==================================================
# MICROSOFT ENTRA
# ==================================================

# Microsoft Entra Application (Client) ID
ENTRA_CLIENT_ID = os.getenv("ENTRA_CLIENT_ID")

# Microsoft Entra Directory (Tenant) ID
ENTRA_TENANT_ID = os.getenv("ENTRA_TENANT_ID")

# OAuth Authority
ENTRA_AUTHORITY = (
    f"https://login.microsoftonline.com/"
    f"{ENTRA_TENANT_ID}"
)

# Delegated SharePoint permission
ENTRA_SCOPE = [
    "https://ctsnordics365.sharepoint.com/AllSites.Manage"
]


# ==================================================
# INFOBRIC
# ==================================================

INFOBRIC_LOGIN = "https://site.infobric.com"

INFOBRIC_URL = (
    "https://site.infobric.com/"
    "Site/Panels/Persons/Parts/"
    "EmployeeLeftPanel.aspx/"
    "GetEmployeePresenceCountInfoOnSite"
)

# Saved authenticated browser session
INFOBRIC_STATE = "states/state_infobric.json"

# Windows time zone expected by Infobric
TIMEZONE = "W. Europe Standard Time"

# Dedicated Infobric service account
INFOBRIC_USERNAME = os.getenv("INFOBRIC_USERNAME")
INFOBRIC_PASSWORD = os.getenv("INFOBRIC_PASSWORD")


# ==================================================
# SHAREPOINT
# ==================================================

# SharePoint tenant root
SHAREPOINT_LOGIN = "https://ctsnordics365.sharepoint.com"

# -----------------------------------------------------------------
# Temporary
#
# Used only while migrating away from Playwright authentication.
# Will be removed after Microsoft Entra authentication
# is fully implemented.
# -----------------------------------------------------------------

SHAREPOINT_STATE = "states/state_sharepoint.json"

# SharePoint internal column names
HEADCOUNT_FIELD = "PeopleonSite"

LAST_UPDATE_FIELD = "Lastmodified"


# ==================================================
# CONSTRUCTION SITES
# ==================================================

SITES = [

    {
        "name": "Kvandal",

        # --------------------------------------------------
        # INFOBRIC
        # --------------------------------------------------

        "infobric_site_id":
            "d5c24017-fb45-47fb-a647-4955872c3ec3",

        # --------------------------------------------------
        # SHAREPOINT
        # --------------------------------------------------

        "sharepoint_site":
            "https://ctsnordics365.sharepoint.com/sites/PRO1047-Sunlight",

        "sharepoint_list":
            "On Site Headcount",

        # Value stored in the SharePoint Title column
        "sharepoint_title":
            "Kvandal"
    }

]