"""
Issue #10 -- FastAPI Scaffold -- app/services/auth_service.py

Given in full -- this is a standard FastAPI auth-dependency pattern,
not a judgment call about your data. Read it, particularly the
secrets.compare_digest note below, since it's worth understanding why
it's there rather than just accepting it.
"""

import logging
import os
import secrets

from fastapi import Header, HTTPException, status

logger = logging.getLogger(__name__)


def verify_api_key(x_api_key: str | None = Header(None)) -> None:
    """
    FastAPI dependency: validates the X-API-Key request header against
    the API_KEY environment variable. Raises HTTP 401 if missing or
    invalid. Returns nothing on success -- its job is just to raise
    (or not).

    Uses secrets.compare_digest instead of `==` for the comparison.
    A plain `==` on strings exits as soon as it hits the first
    mismatched character, so how long the comparison takes can, in
    principle, leak information about how many leading characters of a
    guess were correct (a timing side-channel). compare_digest always
    takes the same amount of time regardless of where the mismatch is,
    which is why it's the standard choice for comparing secrets.
    """
    expected_key = os.environ.get("API_KEY")

    if not expected_key:
        logger.error("API_KEY is not set in the environment.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Server misconfigured: API_KEY not set",
        )

    if not x_api_key or not secrets.compare_digest(x_api_key, expected_key):
        logger.warning("Rejected request with missing or invalid API key.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key",
        )