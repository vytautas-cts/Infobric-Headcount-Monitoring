"""
---------------------------------------------------
Playwright Manager

Author: Vytautas Labanauskas

Purpose:
Creates and manages a shared Playwright Chromium
instance used throughout the application.

The browser can be restarted automatically after
network interruptions or system sleep.

---------------------------------------------------
"""

from playwright.sync_api import sync_playwright

from functions.config import HEADLESS


_playwright = None
_browser = None


def start_browser():
    """
    Start Playwright and Chromium if not already
    running.
    """

    global _playwright
    global _browser

    if _browser is not None:
        return

    _playwright = sync_playwright().start()

    _browser = _playwright.chromium.launch(
        headless=HEADLESS,
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
    )


def restart_browser():
    """
    Completely restart Chromium.
    """

    global _playwright
    global _browser

    try:
        if _browser:
            _browser.close()
    except Exception:
        pass

    try:
        if _playwright:
            _playwright.stop()
    except Exception:
        pass

    _browser = None
    _playwright = None

    start_browser()


def get_browser():

    start_browser()

    return _browser


def create_context(storage_state=None):

    browser = get_browser()

    if storage_state:

        return browser.new_context(
            storage_state=storage_state
        )

    return browser.new_context()


def close_browser():

    global _browser
    global _playwright

    try:
        if _browser:
            _browser.close()
    except Exception:
        pass

    try:
        if _playwright:
            _playwright.stop()
    except Exception:
        pass

    _browser = None
    _playwright = None