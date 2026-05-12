"""
Auth0 JWT Middleware
─────────────────────
Validates Auth0-issued access tokens (RS256) on protected routes.

Configuration (from .env):
  AUTH0_DOMAIN         — e.g. dev-xxx.us.auth0.com
  AUTH0_API_IDENTIFIER — audience, e.g. https://dev-xxx.us.auth0.com/api/v2/
  AUTH0_ALGORITHMS     — RS256 (Auth0 default for SPAs)

Usage:
  # Protect a single route
  @router.get("/protected", dependencies=[Depends(require_auth)])
  async def protected():
      ...

  # Get full token payload
  @router.get("/me")
  async def me(token: dict = Depends(get_current_token)):
      return {"sub": token["sub"], "scopes": token.get("scope", "").split()}
"""
import os
import json
import httpx
from typing import Optional
from functools import lru_cache

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError, ExpiredSignatureError

# ─── Config ───────────────────────────────────────────────────────────────────

AUTH0_DOMAIN     = os.getenv("AUTH0_DOMAIN", "")
API_IDENTIFIER   = os.getenv("AUTH0_API_IDENTIFIER", "")
ALGORITHMS       = os.getenv("AUTH0_ALGORITHMS", "RS256").split(",")
JWKS_URI         = os.getenv(
    "AUTH0_JWKS_URI",
    f"https://{AUTH0_DOMAIN}/.well-known/jwks.json" if AUTH0_DOMAIN else ""
)

_bearer = HTTPBearer(auto_error=False)


# ─── JWKS Cache ───────────────────────────────────────────────────────────────

@lru_cache(maxsize=1)
def _cached_jwks() -> dict:
    """Fetch and cache JWKS (public keys) from Auth0."""
    if not JWKS_URI:
        return {"keys": []}
    response = httpx.get(JWKS_URI, timeout=10)
    response.raise_for_status()
    return response.json()


def _get_signing_key(kid: str) -> Optional[str]:
    """Extract the RSA public key matching the token's kid header."""
    jwks = _cached_jwks()
    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            # Convert JWK → PEM using python-jose
            from jose.backends import RSAKey
            return RSAKey(key, algorithm="RS256").public_key().export_key("PEM").decode("utf-8")
    return None


# ─── Token Validation ─────────────────────────────────────────────────────────

def _validate_token(token: str) -> dict:
    """
    Validate an Auth0 JWT access token.
    Checks: signature, expiry, audience, issuer, algorithm.
    Returns the decoded payload dict.
    Raises HTTPException on any validation failure.
    """
    if not AUTH0_DOMAIN:
        # Auth0 not configured — bypass for local dev (log warning)
        import logging
        logging.warning("AUTH0_DOMAIN not set — token validation bypassed")
        return {"sub": "local_dev", "scope": ""}

    # Decode header to get kid (key ID)
    try:
        unverified_header = jwt.get_unverified_header(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Malformed JWT — cannot decode header",
            headers={"WWW-Authenticate": "Bearer"}
        )

    kid = unverified_header.get("kid")
    alg = unverified_header.get("alg", "")

    # T1: Reject alg:none and HS* — our threat detection in middleware form
    if alg.lower() in ("none", "hs256", "hs384", "hs512", ""):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"JWT algorithm '{alg}' not allowed — RS256/ES256 required",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if alg not in ALGORITHMS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"JWT algorithm '{alg}' not in allowlist {ALGORITHMS}",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Fetch matching public key
    signing_key = _get_signing_key(kid) if kid else None
    if not signing_key:
        # Refresh cache once in case of key rotation
        _cached_jwks.cache_clear()
        signing_key = _get_signing_key(kid) if kid else None

    if not signing_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"No matching public key for kid='{kid}'",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Verify signature + claims
    try:
        payload = jwt.decode(
            token,
            signing_key,
            algorithms=ALGORITHMS,
            audience=API_IDENTIFIER or None,
            issuer=f"https://{AUTH0_DOMAIN}/" if AUTH0_DOMAIN else None,
            options={"verify_at_hash": False}
        )
        return payload

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )


# ─── FastAPI Dependencies ─────────────────────────────────────────────────────

async def get_current_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer)
) -> dict:
    """
    FastAPI dependency — extracts and validates the Bearer token.
    Returns decoded token payload.
    Use with: token: dict = Depends(get_current_token)
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return _validate_token(credentials.credentials)


async def require_auth(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer)
) -> None:
    """
    FastAPI dependency — validates the Bearer token and discards payload.
    Use with: dependencies=[Depends(require_auth)]
    """
    await get_current_token(credentials)


def require_scope(required_scope: str):
    """
    Scope-gated dependency factory.
    Usage: dependencies=[Depends(require_scope("read:financials"))]
    """
    async def _check(token: dict = Depends(get_current_token)):
        scopes = token.get("scope", "").split()
        if required_scope not in scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient scope. Required: '{required_scope}'"
            )
    return _check
