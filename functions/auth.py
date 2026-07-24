"""
---------------------------------------------------
Infobric Authentication (requests based)

No browser required.
Uses ASP.NET authentication cookies.
---------------------------------------------------
"""

import os
import json
import requests
from bs4 import BeautifulSoup

from functions.config import (
    INFOBRIC_LOGIN,
    INFOBRIC_STATE,
    INFOBRIC_USERNAME,
    INFOBRIC_PASSWORD
)


_session = None


def save_session(session):

    cookies = {}

    for cookie in session.cookies:
        cookies[cookie.name] = cookie.value

    os.makedirs(
        os.path.dirname(INFOBRIC_STATE),
        exist_ok=True
    )

    with open(INFOBRIC_STATE, "w") as f:
        json.dump(cookies, f)


def load_session():

    if not os.path.exists(INFOBRIC_STATE):
        return None

    with open(INFOBRIC_STATE) as f:
        cookies = json.load(f)

    session = requests.Session()

    for name, value in cookies.items():
        session.cookies.set(
            name,
            value,
            domain="site.infobric.com"
        )

    return session


def login_infobric():

    print("Logging into Infobric...")

    session = requests.Session()

    login_url = (
        "https://site.infobric.com/"
        "Login.aspx?ReturnUrl=%2fSettings%2f"
    )


    # Get login page first

    response = session.get(login_url)

    if response.status_code != 200:
        raise Exception(
            "Could not open Infobric login page"
        )


    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    payload = {}


    # ASP.NET hidden fields

    for field in soup.find_all(
        "input",
        type="hidden"
    ):

        if field.get("name"):
            payload[field["name"]] = field.get(
                "value",
                ""
            )


    # Your selectors revealed these names

    payload.update(
        {
            "txtUserNameLogin": INFOBRIC_USERNAME,
            "txtPassword_txtPassword": INFOBRIC_PASSWORD,
            "btnLoginWithUserName": "Login"
        }
    )


    response = session.post(
        login_url,
        data=payload,
        allow_redirects=False
    )


    if response.status_code != 302:

        raise Exception(
            "Infobric login failed"
        )


    if ".ASPXAUTH" not in session.cookies:

        raise Exception(
            "Authentication cookie not received"
        )


    save_session(session)


    print(
        "Infobric login successful."
    )


    return session



def ensure_logins():

    global _session


    if _session:
        return


    _session = load_session()


    if _session:

        print(
            "Testing saved Infobric session..."
        )

        return


    _session = login_infobric()



def get_session():

    global _session

    ensure_logins()

    return _session