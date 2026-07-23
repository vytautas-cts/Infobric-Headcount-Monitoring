"""
---------------------------------------------------
Logger

Author: Vytautas Labanauskas

Purpose:
Provides consistent console output for the
application.

All console messages should be routed through this
module.

---------------------------------------------------
"""

from datetime import datetime


def timestamp():
    """Current time for log messages."""

    return datetime.now().strftime("%H:%M:%S")


def info(message):
    """General information."""

    print(f"[{timestamp()}] {message}")


def headcount_changed(site, count):
    """
    Called whenever a site's headcount changes.
    """

    print(
        f"[{timestamp()}] "
        f"People on the {site} site: {count} "
    )


def sharepoint_updated(site):
    """
    Called after a successful SharePoint update.
    """

    print(
        f"[{timestamp()}] "
        f"{site} headcount updated in SharePoint"
    )


def warning(message):
    """
    Non-critical warning.
    """

    print(
        f"[{timestamp()}] "
        f"{message}"
    )


def error(message):
    """
    Critical error message.
    """

    print(
        f"[{timestamp()}] "
        f"ERROR: {message}"
    )