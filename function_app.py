"""
---------------------------------------------------
Azure Function App

Infobric Live Headcount Monitoring

Purpose:
Runs the Infobric headcount monitor on a schedule
using Azure Functions Timer Trigger.

---------------------------------------------------
"""

import azure.functions as func

from monitor import run_monitor

import logging


app = func.FunctionApp()


@app.timer_trigger(
    schedule="0 */5 * * * *",
    arg_name="timer",
    run_on_startup=False,
    use_monitor=True
)
def infobric_headcount_monitor(timer: func.TimerRequest) -> None:
    """
    Azure Timer Trigger.

    Runs every 5 minutes.
    """

    logging.info(
        "Infobric headcount monitor started."
    )

    try:

        run_monitor()

        logging.info(
            "Infobric headcount monitor completed successfully."
        )

    except Exception as e:

        logging.exception(
            f"Infobric monitor failed: {e}"
        )