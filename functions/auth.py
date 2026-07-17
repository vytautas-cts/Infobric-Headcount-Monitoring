"""
---------------------------------------------------
Authentication

Author: Vytautas Labanauskas

Purpose:
Manages authentication for Infobric.

Responsibilities

- Validate saved Infobric session.
- Authenticate when required.
- Create authenticated browser contexts.
- Refresh sessions automatically.

SharePoint authentication is handled separately
by Microsoft Entra in sharepoint_auth.py.

---------------------------------------------------
"""

import os

from functions.playwright_manager import (
    get_browser,
    create_context
)

from functions.config import (
    INFOBRIC_LOGIN,
    INFOBRIC_URL,
    INFOBRIC_STATE,
    TIMEZONE,
    SITES,
    INFOBRIC_USERNAME,
    INFOBRIC_PASSWORD
)


# --------------------------------------------------
# Session validation
# --------------------------------------------------

def infobric_session_valid():

    if not os.path.exists(INFOBRIC_STATE):
        return False

    context = create_context(
        storage_state=INFOBRIC_STATE
    )

    try:

        payload = {
            "siteID": SITES[0]["infobric_site_id"],
            "siteTimeZone": TIMEZONE
        }

        response = context.request.post(
            INFOBRIC_URL,
            data=payload
        )

        return response.status == 200

    except Exception:

        return False

    finally:

        context.close()


# --------------------------------------------------
# Automatic login
# --------------------------------------------------

def login_infobric():
    """
    Authenticate to Infobric using the service
    account stored in the .env file.

    NOTE:
    The selectors below must match the Infobric
    login page.
    """

    browser = get_browser()

    context = create_context()

    page = context.new_page()

    page.goto(INFOBRIC_LOGIN)


    page.fill(
    "#txtUserNameLogin",
    INFOBRIC_USERNAME
    )

    page.fill(
    "#txtPassword_txtPassword",
    INFOBRIC_PASSWORD
    )

    page.click(
        "#btnLoginWithUserName"
    )

    page.wait_for_load_state("networkidle")

    page.wait_for_timeout(3000)

    context.storage_state(
        path=INFOBRIC_STATE
    )

    context.close()

    print("✓ Infobric session saved.")


# --------------------------------------------------
# Public API
# --------------------------------------------------

def ensure_logins():

    print("Checking Infobric session...")

    if infobric_session_valid():

        print("✓ Infobric session valid")

    else:

        print("✗ Infobric login required")

        login_infobric()


def create_infobric_context():
    """
    Create an authenticated Infobric browser
    context.
    """

    return create_context(
        storage_state=INFOBRIC_STATE
    )


def refresh_infobric_context(old_context):
    """
    Refresh the Infobric session.
    """

    old_context.close()

    login_infobric()

    return create_infobric_context()