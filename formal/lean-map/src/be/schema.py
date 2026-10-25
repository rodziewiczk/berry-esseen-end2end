"""Closed JSON Schema validation from an offline repository registry."""
from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from .errors import ProtocolError

ROOT = Path(__file__).resolve().parents[2]
_NAME = re.compile(r"[a-z][a-z0-9-]*\.schema\.json\Z", re.ASCII)


@lru_cache(maxsize=1)
def _schemas():
    all_schemas = {}
    by_name = {}
    for folder in (ROOT / "schemas/architecture", ROOT / "schemas/local-pilot"):
        for path in sorted(folder.glob("*.schema.json")):
            value = json.loads(path.read_text(encoding="utf-8-sig"))
            Draft202012Validator.check_schema(value)
            identifier = value["$id"]
            if identifier in all_schemas:
                raise ProtocolError("duplicate_schema_id", "Schema identity is duplicated")
            all_schemas[identifier] = value
            if folder.name == "local-pilot":
                by_name[path.name] = value
    if not by_name:
        raise ProtocolError("missing_schema_bundle", "The public local-pilot schema bundle is required")
    registry = Registry().with_resources(
        (key, Resource.from_contents(value)) for key, value in all_schemas.items())
    return by_name, registry


def validate_document(value, schema_name: str) -> None:
    if not isinstance(schema_name, str) or not _NAME.fullmatch(schema_name):
        raise ProtocolError("unsupported_schema", "Unknown local-pilot schema")
    schemas, registry = _schemas()
    if schema_name not in schemas:
        raise ProtocolError("unsupported_schema", "Unknown local-pilot schema")
    try:
        error = next(Draft202012Validator(schemas[schema_name], registry=registry).iter_errors(value), None)
    except Exception as exc:
        raise ProtocolError("invalid_schema_bundle", "Cannot resolve the local schema bundle") from exc
    if error is not None:
        pointer = "/" + "/".join(str(v) for v in error.absolute_path)
        # Do not echo arbitrary attacker-controlled input or large error reprs.
        raise ProtocolError("schema_validation_failed", "Schema rejected field " + pointer[:256])
