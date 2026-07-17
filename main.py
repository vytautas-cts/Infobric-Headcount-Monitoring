"""
---------------------------------------------------
Infobric Live Headcount Monitoring

Author: Vytautas Labanauskas

Purpose:
Monitor one or more construction sites in Infobric
and update the corresponding SharePoint lists.

Workflow

1. Ensure Infobric login.
2. Create authenticated Infobric browser context.
3. Monitor configured sites.
4. Update SharePoint through Microsoft Entra token.

---------------------------------------------------
"""

import time

from functions.auth import (
    ensure_logins,
    create_infobric_context,
    refresh_infobric_context
)

from functions.playwright_manager import (
    close_browser,
    restart_browser
)

from functions.config import (
    POLL_INTERVAL,
    SITES
)

from functions.exceptions import (
    SessionExpired,
    InfobricError,
    SharePointError,
    NetworkError
)

from functions.infobric import (
    get_headcount
)

from functions.sharepoint import (
    update_sharepoint
)

from functions.logger import (
    info,
    headcount_changed,
    sharepoint_updated,
    error
)

def main():

    info("Starting Live Monitoring...")

    #
    # Ensure Infobric login
    #

    ensure_logins()

    #
    # Create browser context
    #

    infobric_context = create_infobric_context()

    previous = {}

    network_lost = False
    network_failures = 0

    info("Monitoring started.")

    try:

        while True:

            for site in SITES:

                name = site["name"]

                #
                # Get headcount
                #

                retries = 3
                count = None

                while retries > 0:

                    try:

                        count = get_headcount(
                            infobric_context,
                            site
                        )

                        if network_lost:

                            info(
                                "Connection restored."
                            )

                            network_lost = False

                        network_failures = 0

                        break

                    #
                    # Session expired
                    #

                    except SessionExpired:

                        info(
                            "Refreshing Infobric session..."
                        )

                        infobric_context = (
                            refresh_infobric_context(
                                infobric_context
                            )
                        )

                        retries -= 1

                    #
                    # Internet unavailable
                    #

                    except NetworkError:

                        if not network_lost:

                            info(
                                "Network unavailable. Waiting for connection..."
                            )

                            network_lost = True

                        network_failures += 1

                        time.sleep(30)

                        #
                        # Restart Playwright after repeated
                        # network failures.
                        #

                        if network_failures >= 3:

                            info(
                                "Restarting Playwright browser..."
                            )

                            restart_browser()

                            try:
                                infobric_context.close()
                            except Exception:
                                pass

                            try:

                                infobric_context = create_infobric_context()

                            except Exception:

                                info(
                                    "Creating a new Infobric session..."
                                )

                                infobric_context = refresh_infobric_context(
                                    infobric_context
                                )

                            network_failures = 0

                        continue

                    #
                    # Other Infobric error
                    #

                    except InfobricError as e:

                        error(e)

                        info(
                            "Recreating browser context..."
                        )

                        try:

                            infobric_context.close()

                        except Exception:
                            pass

                        infobric_context = (
                            create_infobric_context()
                        )

                        retries -= 1

                    if retries:

                        info(
                            f"Retrying in 10 seconds ({retries} retries left)..."
                        )

                        time.sleep(10)

                #
                # Could not obtain headcount
                #

                if count is None:

                    error(
                        f"Skipping '{name}' this polling cycle."
                    )

                    continue

                #
                # Only update if changed
                #

                if previous.get(name) == count:

                    continue

                headcount_changed(
                    name,
                    count
                )

                #
                # Update SharePoint
                #

                sharepoint_retries = 3

                while sharepoint_retries > 0:

                    try:

                        update_sharepoint(
                            site,
                            count
                        )

                        if network_lost:

                            info(
                                "Connection restored."
                            )

                            network_lost = False

                        break

                    except NetworkError:

                        if not network_lost:

                            info(
                                "SharePoint unavailable. Waiting for connection..."
                            )

                            network_lost = True

                        time.sleep(30)

                        continue

                    except SessionExpired as e:

                        error(e)

                        sharepoint_retries -= 1

                    except SharePointError as e:

                        error(e)

                        sharepoint_retries -= 1


                    if sharepoint_retries:

                        info(
                            f"Retrying SharePoint update ({sharepoint_retries} retries left)..."
                        )

                        time.sleep(10)

                if sharepoint_retries == 0:

                    continue

                sharepoint_updated(
                    name
                )

                previous[name] = count

            time.sleep(
                POLL_INTERVAL
            )

    finally:

        try:

            infobric_context.close()

        except Exception:
            pass

        close_browser()


if __name__ == "__main__":

    main()