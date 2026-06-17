# =============================================================================
# forge / app / core / encryption
# =============================================================================
# Description : Fernet helpers for encrypting BYOK API keys at rest.
# Layer       : Infra
# Feature     : F002 — BYOK Configuration System
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

import base64
import hashlib

from cryptography.fernet import Fernet

from app.config import get_settings


def _fernet() -> Fernet:
    """
    Build Fernet cipher from BYOK_ENCRYPTION_KEY or derived dev key.

    Returns:
        Fernet: Symmetric cipher for API key encryption.
    """
    settings = get_settings()
    raw = settings.byok_encryption_key or settings.supabase_service_role_key
    digest = hashlib.sha256(raw.encode("utf-8")).digest()
    key = base64.urlsafe_b64encode(digest)
    return Fernet(key)


def encrypt_secret(plaintext: str) -> str:
    """
    Encrypt a provider API key for database storage.

    Args:
        plaintext: Raw API key.

    Returns:
        str: Fernet token string.
    """
    token = _fernet().encrypt(plaintext.encode("utf-8")).decode("utf-8")
    return str(token)


def decrypt_secret(token: str) -> str:
    """
    Decrypt a stored API key token.

    Args:
        token: Fernet ciphertext.

    Returns:
        str: Plaintext API key.
    """
    plaintext = _fernet().decrypt(token.encode("utf-8")).decode("utf-8")
    return str(plaintext)
