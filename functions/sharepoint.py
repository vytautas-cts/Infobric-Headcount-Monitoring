"""
---------------------------------------------------
SharePoint

Author: Vytautas Labanauskas

Purpose:
Updates the SharePoint list with the latest
employee headcount using Microsoft Entra ID.

---------------------------------------------------
"""

from datetime import datetime

import requests

from functions.config import (
    HEADCOUNT_FIELD,
    LAST_UPDATE_FIELD
)

from functions.exceptions import (
    SessionExpired,
    SharePointError
)

from functions.sharepoint_auth import (
    get_sharepoint_token
)


def get_headers():

    token = get_sharepoint_token()

    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json;odata=nometadata",
        "Content-Type": "application/json;odata=nometadata"
    }



def get_item_id(site):
    """
    Find SharePoint item ID using Title.
    """

    url = (
        f"{site['sharepoint_site']}"
        f"/_api/web/lists/GetByTitle('{site['sharepoint_list']}')"
        f"/items"
        f"?$filter=Title eq '{site['sharepoint_title']}'"
    )

    try:

        response = requests.get(
            url,
            headers=get_headers()
        )

    except Exception as e:

        raise SharePointError(
            f"Unable to contact SharePoint.\n{e}"
        )


    if response.status_code in (401, 403):

        raise SessionExpired(
            "SharePoint token expired."
        )


    if response.status_code != 200:

        raise SharePointError(
            f"Unable to query SharePoint "
            f"(HTTP {response.status_code})\n"
            f"{response.text}"
        )


    try:

        items = response.json()["value"]

    except Exception:

        raise SharePointError(
            "Invalid SharePoint response."
        )


    if not items:

        raise SharePointError(
            f"No SharePoint item found with "
            f"title '{site['sharepoint_title']}'."
        )


    return items[0]["ID"]



def update_sharepoint(site, count):
    """
    Update SharePoint headcount.
    """


    item_id = get_item_id(
        site
    )


    url = (
        f"{site['sharepoint_site']}"
        f"/_api/web/lists/GetByTitle('{site['sharepoint_list']}')"
        f"/items({item_id})"
    )


    payload = {

        HEADCOUNT_FIELD:
            count,

        LAST_UPDATE_FIELD:
            datetime.now().astimezone().isoformat()

    }


    headers = get_headers()

    headers.update(
        {
            "IF-MATCH": "*",
            "X-HTTP-Method": "MERGE"
        }
    )


    try:

        response = requests.post(
            url,
            headers=headers,
            json=payload
        )


    except Exception as e:

        raise SharePointError(
            f"Unable to contact SharePoint.\n{e}"
        )


    if response.status_code in (401,403):

        raise SessionExpired(
            "SharePoint token expired."
        )


    if response.status_code != 204:

        raise SharePointError(
            f"SharePoint update failed "
            f"(HTTP {response.status_code})\n"
            f"{response.text}"
        )


    return response.status_code