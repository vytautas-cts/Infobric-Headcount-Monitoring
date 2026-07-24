from functions.config import INFOBRIC_URL, TIMEZONE

from functions.exceptions import (
    SessionExpired,
    InfobricError,
    NetworkError
)


async def get_headcount(context, site):

    payload = {
        "siteID": site["infobric_site_id"],
        "siteTimeZone": TIMEZONE
    }


    #
    # Contact Infobric
    #

    try:

        response = await context.request.post(
            INFOBRIC_URL,
            data=payload,
            timeout=10000
        )


    except Exception as e:

        raise NetworkError(
            f"Unable to contact Infobric.\n{e}"
        )



    #
    # Authentication expired
    #

    if response.status in (401, 403):

        raise SessionExpired(
            "Infobric session has expired."
        )



    #
    # Temporary server problems
    #

    if response.status >= 500:

        raise NetworkError(
            f"Infobric server unavailable "
            f"(HTTP {response.status})"
        )



    #
    # Unexpected response
    #

    if response.status != 200:

        raise InfobricError(
            f"Infobric request failed "
            f"(HTTP {response.status})"
        )



    #
    # Parse JSON
    #

    try:

        data = await response.json()


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