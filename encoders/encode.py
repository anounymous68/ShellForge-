"""
Payload encoding helpers for ShellForge.

Supports base64, URL-encoding, and PowerShell -EncodedCommand (UTF-16LE).

Author: Mostafa Tamime
"""

from __future__ import annotations

import base64
import urllib.parse
from typing import Callable


def encode_base64(payload: str) -> str:
    """Return the payload as a UTF-8 base64 string."""
    return base64.b64encode(payload.encode("utf-8")).decode("ascii")


def encode_url(payload: str) -> str:
    """Return a URL-encoded form of the payload."""
    return urllib.parse.quote(payload, safe="")


def encode_ps_encoded(payload: str) -> str:
    """
    Return a PowerShell -EncodedCommand value.

    PowerShell expects UTF-16LE bytes, then base64.
    """
    encoded = base64.b64encode(payload.encode("utf-16-le")).decode("ascii")
    return f"powershell -EncodedCommand {encoded}"


ENCODERS: dict[str, Callable[[str], str]] = {
    "none": lambda p: p,
    "base64": encode_base64,
    "urlencode": encode_url,
    "ps-encoded": encode_ps_encoded,
}


def apply_encoding(payload: str, method: str) -> str:
    """Apply *method* encoding to *payload*."""
    if method not in ENCODERS:
        raise ValueError(f"Unknown encoding method: {method}")
    return ENCODERS[method](payload)
