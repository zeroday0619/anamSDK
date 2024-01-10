"""
Korea University Anam Hospital internal API for Python SDK
"""
__version__ = "0.1.0"

import httpx
from fake_useragent import UserAgent
from .client import AnamClient


def KUMCClient() -> AnamClient:
    session = httpx.AsyncClient(
        headers={
            "User-Agent": UserAgent().random
        }
    )
    client = AnamClient(session=session)
    return client


__all__ = ["KUMCClient"]