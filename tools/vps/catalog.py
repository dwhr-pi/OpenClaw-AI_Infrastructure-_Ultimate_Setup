"""Read-only, offline import of Free-VPS source claims, not usage approvals.

Dimension keys retain the source vocabulary. Each value is unverified, even
when the source text claims permission. Missing dimensions have value None.
Only the caller writes snapshots; no provider or source scripts are invoked.
"""

from copy import deepcopy
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat


MAX_JSON_BYTES = 4 * 1024 * 1024
SOURCE_REPOSITORY = "https://github.com/dwhr-pi/Free-VPS"
DIMENSION_FIELDS = (
    "gruppe", "url", "art", "pruefstatus", "ressourcen", "regionen",
    "kreditkarte", "kosten", "erneuerung", "kubernetes", "registrierung",
    "agent_registrierung", "mehrfachkonten", "automatisierung", "mining",
    "ki", "krypto_tools", "trading", "oeffentliche_tradingplattform",
    "traffic", "bandbreite", "netz", "backup_sla", "erlaubt_verboten",
    "erfahrungen", "erfahrungsquellen", "quellen", "validatoren",
    "betriebssysteme", "gpu", "commercial", "pruefumfang",
    "landesberechtigung", "cpu_anteil", "architektur", "ram", "disk", "iops",
    "root", "kernel", "cgroups", "tun", "ipv4", "ipv6", "nat", "ports", "udp",
    "traffic_zaehlrichtung", "fair_use", "drosselung", "einrichtungsgebuehr",
    "steuer", "mindestlaufzeit", "egress", "kaution", "telefon", "kyc", "mfa",
    "captcha", "api", "ssh", "ki_client", "ki_inferenz", "ki_training",
    "private_trading_bots", "gewerbliche_nutzung",
)


class CatalogError(ValueError):
    """Invalid or unsafe source JSON or snapshot."""


def _fail(message):
    raise CatalogError(message)


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            _fail("duplicate JSON key: " + key)
        result[key] = value
    return result


def _float(value):
    number = float(value)
    if not math.isfinite(number):
        _fail("non-finite JSON number")
    return number


def _read_json(path):
    # A byte-limited read, not read_bytes() followed by a size check.
    path = Path(path)
    if not path.is_file():
        _fail("JSON input must be a regular file")
    with path.open("rb") as handle:
        if not stat.S_ISREG(os.fstat(handle.fileno()).st_mode):
            _fail("JSON input must be a regular file")
        raw = handle.read(MAX_JSON_BYTES + 1)
    if len(raw) > MAX_JSON_BYTES:
        _fail("JSON exceeds 4 MiB")
    try:
        value = json.loads(
            raw.decode("utf-8"), object_pairs_hook=_object,
            parse_constant=lambda value: _fail("non-finite JSON number: " + value),
            parse_float=_float,
        )
        _check_depth(value)
    except (UnicodeError, RecursionError, ValueError) as exc:
        raise CatalogError("invalid JSON: " + str(exc)) from exc
    if not isinstance(value, dict):
        _fail("JSON root must be an object")
    return raw, value


def _check_depth(value, depth=0):
    if depth > 64:
        _fail("JSON nesting exceeds 64 levels")
    if isinstance(value, dict):
        for child in value.values():
            _check_depth(child, depth + 1)
    elif isinstance(value, list):
        for child in value:
            _check_depth(child, depth + 1)


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        _fail(label + " must be non-empty text")
    return value


def _claimed_date(value, reference):
    if value is None:
        return None
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        _fail("claimed review date must be YYYY-MM-DD or null")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise CatalogError("invalid claimed review date") from exc
    # One calendar day tolerates source timezone differences, not future reviews.
    if parsed > reference.date() + timedelta(days=1):
        _fail("claimed review date is in the future")
    return value


def _retrieval(value, now):
    if value is None:
        parsed = now
    elif isinstance(value, datetime):
        parsed = value
    elif isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise CatalogError("invalid retrieved_at") from exc
    else:
        _fail("retrieved_at must be an aware datetime or ISO timestamp")
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        _fail("retrieved_at requires an explicit timezone")
    parsed = parsed.astimezone(timezone.utc)
    if parsed > now + timedelta(minutes=5):
        _fail("retrieved_at is in the future")
    return parsed


def _head(value):
    if value is not None:
        _text(value, "source head")
        if len(value) > 200 or any(ord(char) < 32 for char in value):
            _fail("invalid source head")
    return value


def _kind(record):
    group = record.get("gruppe")
    if not isinstance(group, str):
        return "unverified"
    family = {
        "historisch": "historical", "trial": "trial",
        "rueckerstattung": "refund", "zweckgebunden": "broker_funded",
    }.get(group)
    if family:
        return family
    # Candidate/redirect claims must not become confirmed VM classifications.
    if group in {"kandidat", "ausgeschlossen"}:
        return "unverified"
    art = record.get("art", "")
    if not isinstance(art, str):
        return "unverified"
    art = art.casefold()
    if "ci-runner" in art:
        return "ci_runner"
    if "app-/shared-hosting" in art:
        return "app_hosting"
    if "systemcontainer" in art or "system-container" in art:
        return "system_container"
    if re.search(r"\b(vm|kvm)\b", art):
        return "vm"
    return "unverified"


def _offer(record, reference):
    if not isinstance(record, dict):
        _fail("offer source_fields must be an object")
    identifier = _text(record.get("id"), "offer id")
    name = _text(record.get("name"), "offer name")
    reviewed = _claimed_date(record.get("geprueft_am"), reference)
    kind = _kind(record)
    if kind == "historical" or record.get("gruppe") == "ausgeschlossen":
        registration = "unsupported"
    elif kind == "unverified" or not record.get("registrierung"):
        registration = "terms_unclear"
    else:
        registration = "human_action_required"
    fields = dict.fromkeys(DIMENSION_FIELDS)
    fields.update({key: None for key in record if key not in {"id", "name", "geprueft_am"}})
    return {
        "id": identifier, "name": name, "kind": kind,
        "source_claimed_reviewed_on": reviewed,
        "content_reviewed_at": None,
        "source_fields": deepcopy(record),
        "registration": {"state": registration},
        "dimensions": {
            key: {"state": "unverified", "value": deepcopy(record.get(key))}
            for key in fields
        },
    }


def _unique(offers):
    ids = set()
    for offer in offers:
        if offer["id"] in ids:
            _fail("duplicate offer id: " + offer["id"])
        ids.add(offer["id"])


def _schema(value):
    if type(value) is not int or value != 1:
        _fail("unsupported schema_version")


def import_catalog(path, *, retrieved_at=None, source_head=None):
    """Import a local source file without network, script execution or writes.

    retrieved_at denotes local ingestion only. Missing source review dates stay
    null. source_head is caller-supplied provenance, not independently verified.
    """
    raw, source = _read_json(path)
    _schema(source.get("schema_version"))
    reference = _retrieval(retrieved_at, datetime.now(timezone.utc))
    records = source.get("angebote")
    if not isinstance(records, list):
        _fail("angebote must be a list")
    offers = [_offer(record, reference) for record in records]
    _unique(offers)
    return {
        "schema_version": 1,
        "source": {
            "repository": SOURCE_REPOSITORY,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "head": _head(source_head),
            "source_claimed_reviewed_on": _claimed_date(source.get("recherchiert_am"), reference),
        },
        "retrieved_at": reference.isoformat().replace("+00:00", "Z"),
        "offers": offers,
    }


def load_catalog(path):
    """Validate an offline import snapshot; its hash is provenance, not a signature."""
    _, catalog = _read_json(path)
    _schema(catalog.get("schema_version"))
    reference = _retrieval(catalog.get("retrieved_at"), datetime.now(timezone.utc))
    if not isinstance(catalog.get("retrieved_at"), str):
        _fail("snapshot requires retrieved_at")
    if not catalog["retrieved_at"].endswith(("Z", "+00:00")):
        _fail("snapshot retrieved_at must be UTC")
    source = catalog.get("source")
    required = {"repository", "sha256", "head", "source_claimed_reviewed_on"}
    if not isinstance(source, dict) or not required.issubset(source):
        _fail("incomplete snapshot provenance")
    if source["repository"] != SOURCE_REPOSITORY:
        _fail("unexpected source repository")
    if not isinstance(source["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", source["sha256"]):
        _fail("invalid source sha256")
    _head(source["head"])
    _claimed_date(source["source_claimed_reviewed_on"], reference)
    offers = catalog.get("offers")
    if not isinstance(offers, list):
        _fail("snapshot offers must be a list")
    for offer in offers:
        if not isinstance(offer, dict) or "source_fields" not in offer:
            _fail("invalid snapshot offer")
        # Rebuild conservative metadata so altered permissions cannot sneak in.
        if offer != _offer(offer["source_fields"], reference):
            _fail("snapshot offer contradicts offline source normalization")
    _unique(offers)
    return catalog


def get_offer(catalog, id):
    """Return the unique matching row; raise KeyError when it is absent."""
    matches = [offer for offer in catalog["offers"] if offer["id"] == id]
    if not matches:
        raise KeyError(id)
    if len(matches) != 1:
        _fail("duplicate offer id: " + str(id))
    return matches[0]
