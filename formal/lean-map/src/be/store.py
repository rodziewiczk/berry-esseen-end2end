"""Immutable local bytes. A digest path never gives a file mathematical trust."""
from __future__ import annotations

import os
from pathlib import Path
import re
import stat
import tempfile

from .codec import bytes_digest, canonical_bytes, loads
from .errors import ProtocolError

_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z", re.ASCII)
_NAT = re.compile(r"(?:0|[1-9][0-9]*)\Z", re.ASCII)


def ordinary_directory(path: Path) -> Path:
    """Create only ordinary directory components; never follow a link/junction."""
    path = Path(os.path.abspath(path))
    if os.name == "nt" and len(str(path)) >= 248:
        raise ProtocolError("path_too_long", "This pilot Windows profile requires a shorter --state-dir")
    for part in [*reversed(path.parents), path]:
        if part.is_symlink() or getattr(part, "is_junction", lambda: False)():
            raise ProtocolError("linked_state_path", "State paths must not contain links")
        if part.exists():
            if not part.is_dir():
                raise ProtocolError("invalid_state_path", "Expected an ordinary directory")
        else:
            try:
                part.mkdir()
            except FileExistsError:
                if not part.is_dir() or part.is_symlink():
                    raise ProtocolError("invalid_state_path", "Directory creation raced a non-directory")
    return path


def _sync_directory(path: Path) -> None:
    # Windows does not expose a POSIX directory fsync through this interface.
    if os.name == "posix":
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def validate_ref(ref: dict, maximum: int = 16 * 1024 * 1024) -> int:
    if type(ref) is not dict or set(ref) != {"bytes_digest", "size_bytes", "media_type", "format_id"}:
        raise ProtocolError("invalid_artifact_ref", "Expected the complete closed artifact reference")
    if not isinstance(ref["bytes_digest"], str) or not _DIGEST.fullmatch(ref["bytes_digest"]):
        raise ProtocolError("invalid_artifact_ref", "Invalid byte digest")
    size = ref["size_bytes"]
    if not isinstance(size, str) or len(size) > 12 or not _NAT.fullmatch(size):
        raise ProtocolError("invalid_artifact_ref", "Invalid artifact size")
    for key in ("media_type", "format_id"):
        if not isinstance(ref[key], str) or not 0 < len(ref[key]) <= 128 or any(
                ord(c) < 32 or ord(c) > 126 for c in ref[key]):
            raise ProtocolError("invalid_artifact_ref", "Invalid artifact type")
    count = int(size)
    if count > maximum:
        raise ProtocolError("artifact_size_limit", "Artifact exceeds the local profile")
    return count


class LocalCAS:
    def __init__(self, root: Path | str, *, max_blob_bytes: int = 16 * 1024 * 1024):
        self.root = ordinary_directory(Path(root))
        self.objects = ordinary_directory(self.root / "objects" / "sha256")
        self.pending = ordinary_directory(self.root / "pending")
        self.max_blob_bytes = max_blob_bytes

    def _path(self, ref: dict) -> Path:
        validate_ref(ref, self.max_blob_bytes)
        hex_digest = ref["bytes_digest"][7:]
        parent = self.objects / hex_digest[:2]
        if parent.is_symlink() or getattr(parent, "is_junction", lambda: False)():
            raise ProtocolError("linked_artifact", "Artifact directory is linked")
        path = parent / hex_digest
        if os.name == "nt" and len(str(path)) >= 260:
            raise ProtocolError("path_too_long", "This pilot Windows profile requires a shorter --state-dir")
        return path

    def read_bytes(self, ref: dict) -> bytes:
        expected = validate_ref(ref, self.max_blob_bytes)
        path = self._path(ref)
        if path.is_symlink():
            raise ProtocolError("linked_artifact", "Artifact is linked")
        try:
            fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
            with os.fdopen(fd, "rb") as stream:
                info = os.fstat(stream.fileno())
                if not stat.S_ISREG(info.st_mode) or info.st_size != expected:
                    raise ProtocolError("artifact_size_mismatch", "Artifact is not the declared ordinary file")
                raw = stream.read(expected + 1)
        except FileNotFoundError as exc:
            raise ProtocolError("artifact_missing", "A required immutable artifact is absent") from exc
        if len(raw) != expected or bytes_digest(raw) != ref["bytes_digest"]:
            raise ProtocolError("artifact_digest_mismatch", "Immutable artifact bytes changed")
        return raw

    def read_json(self, ref: dict):
        return loads(self.read_bytes(ref), require_canonical=True)

    def put_bytes(self, raw: bytes, *, media_type: str = "application/json",
                  format_id: str = "be.local-pilot/1") -> dict:
        if not isinstance(raw, bytes):
            raise ProtocolError("invalid_artifact", "Artifact input must be bytes")
        if len(raw) > self.max_blob_bytes:
            raise ProtocolError("artifact_size_limit", "Artifact exceeds the local profile")
        ref = dict(bytes_digest=bytes_digest(raw), size_bytes=str(len(raw)),
                   media_type=media_type, format_id=format_id)
        validate_ref(ref, self.max_blob_bytes)
        target = self._path(ref)
        ordinary_directory(target.parent)
        fd, temporary = tempfile.mkstemp(prefix="upload-", dir=self.pending)
        temporary = Path(temporary)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
            try:
                # Same-volume hard-link installation is create-only: no overwrite race.
                if os.name == "nt":
                    # Windows rename is create-only (unlike POSIX rename).
                    os.rename(temporary, target)
                else:
                    os.link(temporary, target)
                _sync_directory(target.parent)
            except FileExistsError:
                pass
            except OSError as exc:
                raise ProtocolError("cas_install_unsupported", "Atomic create-only installation failed") from exc
            self.read_bytes(ref)
            return ref
        finally:
            temporary.unlink(missing_ok=True)

    def put_json(self, value, *, format_id: str = "be.local-pilot/1") -> dict:
        return self.put_bytes(canonical_bytes(value), format_id=format_id)

    def put_file(self, path: Path | str, *, format_id: str = "be.local-pilot/1",
                 maximum: int | None = None) -> dict:
        path = Path(path)
        if path.is_symlink() or not path.is_file():
            raise ProtocolError("invalid_output_file", "Expected an ordinary output file")
        limit = min(maximum or self.max_blob_bytes, self.max_blob_bytes)
        with path.open("rb") as stream:
            raw = stream.read(limit + 1)
        if len(raw) > limit:
            raise ProtocolError("artifact_size_limit", "Output exceeds its declared bound")
        return self.put_bytes(raw, format_id=format_id)


ArtifactStore = LocalCAS
