"""
---------------------------------------------------
Microsoft Entra Authentication

Author: Vytautas Labanauskas

Purpose:
Authenticate with Microsoft Entra and cache a
SharePoint access token for later use.

Run this file once whenever a new authentication
is required.

---------------------------------------------------
"""

import os
import msal

from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("ENTRA_CLIENT_ID")
TENANT_ID = os.getenv("ENTRA_TENANT_ID")

CACHE_FILE = "states/sharepoint_token.bin"

SCOPES = [
    "https://ctsnordics365.sharepoint.com/AllSites.Manage"
]


def main():

    cache = msal.SerializableTokenCache()

    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache.deserialize(f.read())

    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        token_cache=cache
    )

    print("Starting Microsoft Entra authentication...\n")

    flow = app.initiate_device_flow(
        scopes=SCOPES
    )

    if "user_code" not in flow:
        raise RuntimeError(
            "Failed to create device authentication flow."
        )

    print(flow["message"])
    print()

    result = app.acquire_token_by_device_flow(flow)

    if "access_token" not in result:
        print(result)
        raise RuntimeError(
            "Authentication failed."
        )

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        f.write(cache.serialize())

    print("✓ Authentication successful.")
    print(f"✓ Token cache saved to {CACHE_FILE}")


if __name__ == "__main__":
    main()