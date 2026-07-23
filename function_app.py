"""
---------------------------------------------------
Azure Function App

Infobric Live Headcount Monitoring

Purpose:
Runs the Infobric headcount monitor on a schedule
using Azure Functions Timer Trigger.

---------------------------------------------------
"""

import logging
import azure.functions as func

from monitor import run_monitor


app = func.FunctionApp()


@app.timer_trigger(
    schedule="0 */5 * * * *",
    arg_name="timer",
    run_on_startup=True,   # TEMPORARY: run immediately after startup
    use_monitor=True
)
def infobric_headcount_monitor(timer: func.TimerRequest) -> None:
    """
    Azure Timer Trigger.

    Runs every 5 minutes.
    """

    logging.warning(
        "========== INFOBRIC TIMER TRIGGER FIRED =========="
    )

    if timer.past_due:
        logging.warning(
            "Timer is running late."
        )

    try:

        logging.warning(
            "Starting Infobric headcount monitor..."
        )

        run_monitor()

        logging.warning(
            "Infobric headcount monitor completed successfully."
        )

    except Exception:

        logging.exception(
            "Infobric monitor failed."
        )

        raise