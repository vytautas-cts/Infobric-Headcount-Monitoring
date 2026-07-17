"""
---------------------------------------------------
Custom exceptions

Author: Vytautas Labanauskas

Purpose:
Defines application exceptions used to
control the flow.

---------------------------------------------------
"""


class SessionExpired(Exception):
    """
    Raised when an authenticated session is no
    longer valid.
    """
    pass


class InfobricError(Exception):
    """
    Raised when Infobric returns an unexpected
    response.
    """
    pass


class SharePointError(Exception):
    """
    Raised when SharePoint returns an unexpected
    response.
    """
    pass

class NetworkError(Exception):
    """Temporary network or connection problem."""
    pass