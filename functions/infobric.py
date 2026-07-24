"""
---------------------------------------------------
Infobric Headcount Retrieval

Uses authenticated requests session.
No browser required.

---------------------------------------------------
"""

from functions.config import (
    INFOBRIC_URL,
    TIMEZONE
)

from functions.exceptions import (
    SessionExpired,
    InfobricError,
    NetworkError
)


def get_headcount(session, site):

    payload = {
        "siteID": site["infobric_site_id"],
        "siteTimeZone": TIMEZONE
    }


    #
    # Contact Infobric
    #

    try:

        response = session.post(
            INFOBRIC_URL,
            json=payload,
            timeout=10
        )


    except Exception as e:

        raise NetworkError(
            f"Unable to contact Infobric.\n{e}"
        )


    #
    # Authentication expired
    #

    if response.status_code in (401, 403):

        raise SessionExpired(
            "Infobric session has expired."
        )


    #
    # Temporary server problems
    #

    if response.status_code >= 500:

        raise NetworkError(
            f"Infobric server unavailable "
            f"(HTTP {response.status_code})"
        )


    #
    # Unexpected response
    #

    if response.status_code != 200:

        raise InfobricError(
            f"Infobric request failed "
            f"(HTTP {response.status_code})"
        )


    #
    # Parse JSON
    #

    try:

        data = response.json()


    except Exception:

        raise InfobricError(
            "Infobric returned invalid JSON."
        )


    #
    # Extract headcount
    #

    try:

        return next(
            item["EmployeesCount"]
            for item in data["d"]
            if item["Presence"] == 0
        )


    except (KeyError, StopIteration):

        raise InfobricError(
            f"Could not determine headcount "
            f"for '{site['name']}'."
        )