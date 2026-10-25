"""Local coordinator authentication for expensive, source-checked receipts.

The key is private operational state, never a certificate or mathematical
premise. Third parties rerun the checker; the seal is not a Lean proof.
"""
from __future__ import annotations

import hashlib
import hmac
import os
from pathlib import Path
import re
import secrets
import stat

from .codec import canonical_bytes, bytes_digest
from .errors import ProtocolError
from .store import ordinary_directory

_HEX = re.compile(r"[0-9a-f]{64}\Z", re.ASCII)


class LocalAuthority:
    def __init__(self, directory: Path | str):
        root = ordinary_directory(Path(directory))
        path = root / "authority.key"
        if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
            raise ProtocolError("linked_authority_key", "Authority key must be an ordinary private file")
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            pass
        else:
            with os.fdopen(fd, "wb") as stream:
                stream.write(secrets.token_bytes(32))
                stream.flush()
                os.fsync(stream.fileno())
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        with os.fdopen(fd, "rb") as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_size != 32:
                raise ProtocolError("authority_key_invalid", "Incomplete local authority key; do not reuse prior acceptance")
            if os.name == "posix" and info.st_mode & 0o077:
                raise ProtocolError("authority_key_permissions", "Authority key must be private to its owner")
            key = stream.read(33)
        if len(key) != 32:
            raise ProtocolError("authority_key_invalid", "Invalid local authority key")
        self._key = key
        self.authority_id = bytes_digest(key)

    def sign(self, payload: dict) -> dict[str, str]:
        raw = canonical_bytes(payload)
        return {"scheme": "be.local-authority/hmac-sha256/1", "authority_id": self.authority_id,
                "payload_digest": bytes_digest(raw),
                "signature": hmac.new(self._key, b"BELOCALAUTH/1\n" + raw, hashlib.sha256).hexdigest()}

    def verify(self, payload: dict, seal: dict) -> None:
        if type(seal) is not dict or set(seal) != {"scheme", "authority_id", "payload_digest", "signature"}:
            raise ProtocolError("unauthorized_cache_receipt", "Missing closed local authority seal")
        signature = seal["signature"]
        if not isinstance(signature, str) or not _HEX.fullmatch(signature):
            raise ProtocolError("unauthorized_cache_receipt", "Malformed local authority seal")
        expected = self.sign(payload)
        if any(seal[k] != expected[k] for k in ("scheme", "authority_id", "payload_digest")) \
                or not hmac.compare_digest(signature, expected["signature"]):
            raise ProtocolError("unauthorized_cache_receipt", "Receipt is not authenticated for this exact payload")
