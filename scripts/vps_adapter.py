#!/usr/bin/env python3
"""CLI fuer Offline-Kataloge und explizit autorisierte VPS-Adapteraktionen."""

import argparse
import json
import os
from pathlib import Path
import stat
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.vps import adapter  # noqa: E402
from tools.vps.catalog import get_offer, import_catalog, load_catalog  # noqa: E402


ARGUMENT_ERROR = "Fehler: Ungueltige Argumente.\n"
ACTION_ERROR = "Fehler: VPS-Aktion fehlgeschlagen.\n"
ACTIONS = ("plan", "validate", "provision", "status", "configure", "verify", "teardown")


class ArgumentError(ValueError):
    """Parser failure without user-controlled diagnostic text."""


class Parser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("allow_abbrev", False)
        super().__init__(*args, **kwargs)

    def error(self, message):
        raise ArgumentError()


def parser():
    result = Parser(prog="vps_adapter.py", description=__doc__)
    commands = result.add_subparsers(dest="action", required=True)
    catalog = commands.add_parser("catalog", help="Lokale Quelle als Snapshot importieren")
    catalog.add_argument("--source", required=True)
    catalog.add_argument("--source-head")
    catalog.add_argument("--output", required=True)
    for action in ACTIONS:
        command = commands.add_parser(action)
        command.add_argument("--plan", required=True)
        command.add_argument("--catalog", required=True)
        command.add_argument("--apply", action="store_true")
        command.add_argument("--authorization")
        command.add_argument("--state-dir")
    return result


def _private_authorization(info):
    if not stat.S_ISREG(info.st_mode):
        raise adapter.Guard("authorization_regular_file_required")
    if os.name == "posix":
        if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o600:
            raise adapter.Guard("authorization_private_owner_permissions_required")


def _read_authorization(value):
    path = adapter.protected(value, outside_repo=True)
    _private_authorization(path.lstat())
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    descriptor = os.open(path, flags)
    try:
        info = os.fstat(descriptor)
        _private_authorization(info)
        if info.st_size > adapter.MAX_BYTES:
            raise adapter.Guard("authorization_too_large")
        # Check the opened descriptor before reading, not just the path metadata.
        with os.fdopen(descriptor, "rb", closefd=False) as stream:
            raw = stream.read(adapter.MAX_BYTES + 1)
        if len(raw) > adapter.MAX_BYTES:
            raise adapter.Guard("authorization_too_large")
        authorization = adapter.strict_json(raw)
        if not isinstance(authorization, dict):
            raise adapter.Guard("authorization_object_required")
        return authorization
    finally:
        os.close(descriptor)


def _run(args):
    if args.action == "catalog":
        catalog = import_catalog(args.source, source_head=args.source_head)
        payload = json.dumps(catalog, ensure_ascii=True, allow_nan=False, indent=2) + "\n"
        output = adapter.protected(Path(args.output).absolute())
        # Guard parent links before exclusive creation of the final file.
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(payload)
        return {"catalog_written": True, "offers": len(catalog["offers"])}
    plan = adapter.read_json(args.plan)
    catalog = load_catalog(args.catalog)
    offer = get_offer(catalog, plan["offer_id"])
    authorization = None
    if args.apply:
        if args.authorization is None:
            raise adapter.Guard("operator_authorization_required")
        authorization = _read_authorization(args.authorization)
    return adapter.execute(args.action, plan, offer, authorization,
                           apply=args.apply, state_root=args.state_dir)


def main(argv=None):
    try:
        args = parser().parse_args(argv)
        result = _run(args)
        output = json.dumps(result, ensure_ascii=True, allow_nan=False, sort_keys=True)
        sys.stdout.write(output + "\n")
        return 0
    except ArgumentError:
        sys.stderr.write(ARGUMENT_ERROR)
        return 2
    except (Exception, KeyboardInterrupt):
        # CatalogError and OS/parser/provider exceptions may include input values.
        sys.stderr.write(ACTION_ERROR)
        return 1


if __name__ == "__main__":
    sys.exit(main())
