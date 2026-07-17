"""
---------------------------------------------------
SharePoint Authentication

Uses Microsoft Entra ID / MSAL.

No browser required.
---------------------------------------------------
"""

import os
import msal

from dotenv import load_dotenv


load_dotenv()


CLIENT_ID = os.getenv(
    "ENTRA_CLIENT_ID"
)

TENANT_ID = os.getenv(
    "ENTRA_TENANT_ID"
)


CACHE_FILE = "states/sharepoint_token.bin"


SCOPES = [
    "https://ctsnordics365.sharepoint.com/AllSites.Manage"
]


def get_sharepoint_token():

    cache = msal.SerializableTokenCache()


    if os.path.exists(CACHE_FILE):

        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            cache.deserialize(
                f.read()
            )


    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=(
            f"https://login.microsoftonline.com/"
            f"{TENANT_ID}"
        ),
        token_cache=cache
    )


    accounts = app.get_accounts()


    if not accounts:

        raise Exception(
            "No SharePoint account in cache"
        )


    result = app.acquire_token_silent(
        SCOPES,
        accounts[0]
    )


    if not result:

        raise Exception(
            "Could not refresh SharePoint token"
        )


    return result["access_token"]