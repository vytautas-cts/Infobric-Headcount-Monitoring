"""
---------------------------------------------------
Infobric Live Headcount Monitoring

Author: Vytautas Labanauskas

Purpose:
Monitor one or more construction sites in Infobric
and update the corresponding SharePoint lists.

---------------------------------------------------
"""

import time


from functions.auth import (
    get_session
)


from functions.config import (
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



def run_monitor():

    info("Starting monitoring cycle...")


    #
    # Get authenticated Infobric session
    #

    session = get_session()


    network_lost = False


    try:

        for site in SITES:

            name = site["name"]

            retries = 3
            count = None


            while retries > 0:


                try:

                    count = get_headcount(
                        session,
                        site
                    )


                    if network_lost:

                        info(
                            "Connection restored."
                        )

                        network_lost = False


                    break



                except SessionExpired as e:

                    error(e)

                    info(
                        "Infobric session expired. Re-authenticating..."
                    )


                    session = get_session()


                    retries -= 1



                except NetworkError as e:


                    error(e)


                    if not network_lost:

                        info(
                            "Network unavailable. Waiting..."
                        )

                        network_lost = True


                    time.sleep(30)



                except InfobricError as e:


                    error(e)


                    retries -= 1



                if retries:

                    info(
                        f"Retrying Infobric ({retries} retries left)..."
                    )

                    time.sleep(10)



            #
            # Could not obtain count
            #

            if count is None:

                error(
                    f"Skipping '{name}'."
                )

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


                    break



                except NetworkError as e:


                    error(e)

                    time.sleep(30)



                except SharePointError as e:


                    error(e)

                    sharepoint_retries -= 1



                if sharepoint_retries:

                    info(
                        f"Retrying SharePoint update "
                        f"({sharepoint_retries} retries left)..."
                    )

                    time.sleep(10)



            if sharepoint_retries == 0:

                continue



            sharepoint_updated(
                name
            )



    finally:

        pass



    info(
        "Monitoring completed."
    )