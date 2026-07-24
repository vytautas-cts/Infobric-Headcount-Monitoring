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

async def infobric_session_valid():
    """
    Check if existing Infobric storage state
    is still authenticated.
    """

    if not os.path.exists(INFOBRIC_STATE):
        return False


    context = await create_context(
        storage_state=INFOBRIC_STATE
    )


    try:

        payload = {
            "siteID": SITES[0]["infobric_site_id"],
            "siteTimeZone": TIMEZONE
        }


        response = await context.request.post(
            INFOBRIC_URL,
            data=payload
        )


        return response.status == 200


    except Exception:

        return False


    finally:

        await context.close()



# --------------------------------------------------
# Automatic login
# --------------------------------------------------

async def login_infobric():
    """
    Authenticate to Infobric using service account.
    """

    await get_browser()


    context = await create_context()


    page = await context.new_page()


    await page.goto(
        INFOBRIC_LOGIN
    )


    await page.fill(
        "#txtUserNameLogin",
        INFOBRIC_USERNAME
    )


    await page.fill(
        "#txtPassword_txtPassword",
        INFOBRIC_PASSWORD
    )


    await page.click(
        "#btnLoginWithUserName"
    )


    await page.wait_for_load_state(
        "networkidle"
    )


    await page.wait_for_timeout(
        3000
    )


    await context.storage_state(
        path=INFOBRIC_STATE
    )


    await context.close()


    print("Infobric session saved.")



# --------------------------------------------------
# Public API
# --------------------------------------------------

async def ensure_logins():

    print("Checking Infobric session...")


    if await infobric_session_valid():

        print("Infobric session valid")


    else:

        print("Infobric login required")

        await login_infobric()



async def create_infobric_context():
    """
    Create authenticated Infobric browser context.
    """

    return await create_context(
        storage_state=INFOBRIC_STATE
    )



async def refresh_infobric_context(old_context):
    """
    Refresh Infobric session.
    """

    await old_context.close()


    await login_infobric()


    return await create_infobric_context()