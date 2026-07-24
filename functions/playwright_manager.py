"""
---------------------------------------------------
Playwright Manager

Azure Functions compatible async Playwright manager
---------------------------------------------------
"""

import os
from playwright.async_api import async_playwright

from functions.config import HEADLESS


# Tell Playwright where the bundled browsers are
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/home/site/wwwroot/ms-playwright"

_playwright = None
_browser = None


async def start_browser():

    global _playwright
    global _browser

    if _browser:
        return

    _playwright = await async_playwright().start()

    executable = (
        "/home/site/wwwroot/ms-playwright/"
        "chromium_headless_shell-1228/"
        "chrome-headless-shell-linux64/"
        "chrome-headless-shell"
    )

    _browser = await _playwright.chromium.launch(
        executable_path=executable,
        headless=HEADLESS,
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
        ],
    )


async def restart_browser():

    global _playwright
    global _browser

    try:
        if _browser:
            await _browser.close()
    except Exception:
        pass

    try:
        if _playwright:
            await _playwright.stop()
    except Exception:
        pass

    _browser = None
    _playwright = None

    await start_browser()


async def get_browser():

    await start_browser()
    return _browser


async def create_context(storage_state=None):

    browser = await get_browser()

    if storage_state:
        return await browser.new_context(storage_state=storage_state)

    return await browser.new_context()


async def close_browser():

    global _browser
    global _playwright

    try:
        if _browser:
            await _browser.close()
    except Exception:
        pass

    try:
        if _playwright:
            await _playwright.stop()
    except Exception:
        pass

    _browser = None
    _playwright = None