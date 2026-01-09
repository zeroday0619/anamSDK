"""
Korea University Anam Hospital internal API for Python SDK
"""
__version__ = "0.1.1"

import httpx
from fake_useragent import UserAgent
from .client import AnamClient


def KUMCClient(username: str | None = None, password: str | None = None) -> AnamClient:
    session = httpx.AsyncClient(
        headers={
            "User-Agent": UserAgent().random
        }
    )
    client = AnamClient(session=session, username=username, password=password)
    return client


__all__ = ["KUMCClient"]