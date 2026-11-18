"""Fixture-only CLI checks; no provider, SSH, environment credentials or network."""

from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tools.vps.catalog import CatalogError, import_catalog, load_catalog


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("vps_cli", ROOT / "scripts/vps_adapter.py")
cli = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cli)


class CliTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name).resolve()
        self.source = self.write("source.json", {
            "schema_version": 1, "recherchiert_am": "2020-02-19",
            "angebote": [{"id": "fixture", "name": "Synthetic offer", "gruppe": "gratis",
                          "art": "VM", "registrierung": ["Human contract acceptance"],
                          "geprueft_am": "2020-02-19"}],
        })
        self.catalog = self.write("catalog.json", import_catalog(self.source))
        self.plan = self.write("plan.json", {"offer_id": "fixture"})
        self.authorization = self.write("authorization.json", {"version": 1})
        self.authorization.chmod(0o600)
        self.addCleanup(patch.stopall)
        patch("socket.socket", side_effect=AssertionError("network forbidden")).start()
        patch.object(cli.adapter, "GcpAdapter", side_effect=AssertionError("provider forbidden")).start()
        patch.object(cli.adapter, "verify_ssh", side_effect=AssertionError("SSH forbidden")).start()

    def write(self, name, value):
        path = self.directory / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def invoke(self, argv):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = cli.main([str(value) for value in argv])
        return code, stdout.getvalue(), stderr.getvalue()

    def arguments(self, action):
        return [action, "--plan", self.plan, "--catalog", self.catalog]

    def test_catalog_exclusive_output_and_optional_head(self):
        for head in [None, "a" * 40]:
            output = self.directory / ("output-" + str(head) + ".json")
            args = ["catalog", "--source", self.source, "--output", output]
            if head is not None:
                args += ["--source-head", head]
            code, stdout, stderr = self.invoke(args)
            self.assertEqual((0, ""), (code, stderr))
            self.assertEqual({"catalog_written": True, "offers": 1}, json.loads(stdout))
            self.assertEqual(head, load_catalog(output)["source"]["head"])
            original = output.read_bytes()
            self.assertEqual((1, "", cli.ACTION_ERROR), self.invoke(args))
            self.assertEqual(original, output.read_bytes())

    def test_catalog_existing_symlink_never_overwrites_target(self):
        output = self.directory / "linked.json"
        try:
            output.symlink_to(self.source)
        except OSError:
            self.skipTest("symlink creation unavailable")
        original = self.source.read_bytes()
        self.assertEqual((1, "", cli.ACTION_ERROR), self.invoke(
            ["catalog", "--source", self.source, "--output", output]))
        self.assertEqual(original, self.source.read_bytes())

    def test_catalog_protects_absolute_output_before_exclusive_creation(self):
        output = self.directory / "protected-output.json"
        relative = Path("relative-output.json")
        with patch.object(cli.adapter, "protected", return_value=output) as protected:
            result = self.invoke(["catalog", "--source", self.source, "--output", relative])
        self.assertEqual(0, result[0])
        protected.assert_called_once_with(relative.absolute())
        self.assertEqual(1, len(load_catalog(output)["offers"]))

    def test_catalog_parent_link_metadata_rejected_before_create(self):
        parent = self.directory / "parent"
        parent.mkdir()
        output = parent / "must-not-exist.json"
        real_lstat = Path.lstat

        def linked_parent(path, *args, **kwargs):
            if path == parent:
                return SimpleNamespace(st_mode=stat.S_IFLNK | 0o777)
            return real_lstat(path, *args, **kwargs)

        with patch.object(Path, "lstat", linked_parent):
            self.assertEqual((1, "", cli.ACTION_ERROR), self.invoke(
                ["catalog", "--source", self.source, "--output", output]))
        self.assertFalse(output.exists())

    def test_catalog_parent_traversal_rejected_before_create(self):
        parent = self.directory / "parent"
        parent.mkdir()
        output = parent / ".." / "must-not-exist.json"
        self.assertEqual((1, "", cli.ACTION_ERROR), self.invoke(
            ["catalog", "--source", self.source, "--output", output]))
        self.assertFalse((self.directory / "must-not-exist.json").exists())

    def test_catalog_real_symlink_parent_never_creates_in_target(self):
        target = self.directory / "target"
        target.mkdir()
        link = self.directory / "linked-parent"
        try:
            link.symlink_to(target, target_is_directory=True)
        except OSError:
            self.skipTest("directory symlink creation unavailable")
        self.assertEqual((1, "", cli.ACTION_ERROR), self.invoke(
            ["catalog", "--source", self.source, "--output", link / "must-not-exist.json"]))
        self.assertEqual([], list(target.iterdir()))

    def test_all_actions_forward_imported_offer_and_dry_run(self):
        for action in cli.ACTIONS:
            with self.subTest(action=action), patch.object(cli.adapter, "execute", return_value={"executed": False}) as execute:
                with patch.object(cli, "_read_authorization", side_effect=AssertionError("must not read")):
                    result = self.invoke(self.arguments(action) + [
                        "--authorization", "DO-NOT-READ", "--state-dir", self.directory / "state"])
                self.assertEqual((0, '{"executed": false}\n', ""), result)
                args, kwargs = execute.call_args
                self.assertEqual(action, args[0])
                self.assertEqual({"offer_id": "fixture"}, args[1])
                self.assertEqual("fixture", args[2]["id"])
                self.assertIn("source_fields", args[2])
                self.assertIsNone(args[3])
                self.assertEqual({"apply": False, "state_root": str(self.directory / "state")}, kwargs)

    def test_apply_reads_protected_external_authorization(self):
        real_protected = cli.adapter.protected
        for action in cli.ACTIONS:
            with self.subTest(action=action), \
                    patch.object(cli.adapter, "protected", wraps=real_protected) as protected, \
                    patch.object(cli.adapter, "execute", return_value={"mocked": True}) as execute:
                result = self.invoke(self.arguments(action) + [
                    "--apply", "--authorization", self.authorization])
                self.assertEqual(0, result[0])
                protected.assert_called_once_with(str(self.authorization), outside_repo=True)
                self.assertEqual({"version": 1}, execute.call_args.args[3])
                self.assertEqual({"apply": True, "state_root": None}, execute.call_args.kwargs)

    def test_apply_without_authorization_is_rejected_before_execute(self):
        with patch.object(cli.adapter, "execute") as execute:
            self.assertEqual((1, "", cli.ACTION_ERROR), self.invoke(self.arguments("status") + ["--apply"]))
            execute.assert_not_called()

    def test_real_adapter_preview_never_authorizes_or_contacts_provider(self):
        self.write("plan.json", {"offer_id": "fixture", "resource_id": "123"})
        decision = {"plan_hash": "a" * 64, "usage_ready": False}
        for action in cli.ACTIONS:
            with self.subTest(action=action), \
                    patch.object(cli.adapter, "validate", return_value=decision), \
                    patch.object(cli.adapter, "authorize", side_effect=AssertionError("no authorization")), \
                    patch.object(cli, "_read_authorization", side_effect=AssertionError("no file read")):
                code, stdout, stderr = self.invoke(self.arguments(action))
                self.assertEqual((0, ""), (code, stderr))
                result = json.loads(stdout)
                if action in {"plan", "validate"}:
                    self.assertEqual(decision, result)
                elif action == "teardown":
                    self.assertTrue(result["preview_only"])
                    self.assertFalse(result["deleted"])
                else:
                    self.assertFalse(result["executed"])
                    self.assertTrue(result["authorization_required"])

    def test_inside_repo_relative_and_directory_authorization_rejected(self):
        for path in [ROOT / "fictional-private-auth.json", Path("relative.json"), self.directory]:
            with self.subTest(path=path), patch.object(cli.adapter, "execute") as execute:
                self.assertEqual((1, "", cli.ACTION_ERROR), self.invoke(
                    self.arguments("status") + ["--apply", "--authorization", path]))
                execute.assert_not_called()

    def test_authorization_posix_exact_mode_owner_and_regular_file(self):
        with patch.object(cli, "os", SimpleNamespace(name="posix", getuid=lambda: 123)):
            cli._private_authorization(SimpleNamespace(st_mode=stat.S_IFREG | 0o600, st_uid=123))
            for mode, owner in [(0o644, 123), (0o400, 123), (0o600, 456), (0o4600, 123)]:
                with self.subTest(mode=mode, owner=owner), self.assertRaises(cli.adapter.Guard):
                    cli._private_authorization(SimpleNamespace(st_mode=stat.S_IFREG | mode, st_uid=owner))
            with self.assertRaises(cli.adapter.Guard):
                cli._private_authorization(SimpleNamespace(st_mode=stat.S_IFDIR | 0o600, st_uid=123))

    @unittest.skipUnless(os.name == "posix", "real POSIX mode check")
    def test_authorization_world_readable_rejected_before_content_read(self):
        self.authorization.chmod(0o644)
        with patch.object(cli.os, "open", side_effect=AssertionError("must not read")):
            with self.assertRaises(cli.adapter.Guard):
                cli._read_authorization(str(self.authorization))

    def test_authorization_size_duplicate_json_and_type_guards(self):
        for raw in [b'{"x":1,"x":2}', b'{"x":NaN}', b'[]', b'\xff',
                    b' ' * (cli.adapter.MAX_BYTES + 1)]:
            with self.subTest(raw=raw[:20]):
                self.authorization.write_bytes(raw)
                self.assertEqual((1, "", cli.ACTION_ERROR), self.invoke(
                    self.arguments("status") + ["--apply", "--authorization", self.authorization]))

    def test_descriptor_permissions_checked_before_read(self):
        with patch.object(cli, "_private_authorization", side_effect=[None, cli.adapter.Guard("changed")]) as check, \
                patch.object(cli.os, "fdopen", side_effect=AssertionError("must not read")):
            with self.assertRaises(cli.adapter.Guard):
                cli._read_authorization(str(self.authorization))
            self.assertEqual(2, check.call_count)

    def test_argparse_errors_never_echo_argument_values(self):
        marker = "PRIVATE-ARGUMENT-CONTENT"
        cases = [[marker], ["status", "--plan", marker],
                 self.arguments("status") + ["--" + marker],
                 self.arguments("status") + [marker],
                 ["catalog", "--source", marker], [],
                 ["status", "--pl", marker, "--catalog", self.catalog]]
        for argv in cases:
            with self.subTest(argv=argv):
                self.assertEqual((2, "", cli.ARGUMENT_ERROR), self.invoke(argv))

    def test_runtime_errors_are_fixed_and_redacted(self):
        marker = "PRIVATE-INPUT-CONTENT"
        for error in [CatalogError(marker), cli.adapter.Guard(marker),
                      OSError(marker), KeyError(marker), RuntimeError(marker)]:
            with self.subTest(error=type(error).__name__), \
                    patch.object(cli, "load_catalog", side_effect=error):
                self.assertEqual((1, "", cli.ACTION_ERROR), self.invoke(self.arguments("plan")))
        with patch.object(cli.adapter, "execute", side_effect=RuntimeError(marker)):
            self.assertEqual((1, "", cli.ACTION_ERROR), self.invoke(self.arguments("verify")))

    def test_invalid_catalog_plan_missing_offer_and_no_output_on_failure(self):
        for plan in [{}, {"offer_id": "absent"}, []]:
            self.write("plan.json", plan)
            self.assertEqual((1, "", cli.ACTION_ERROR), self.invoke(self.arguments("plan")))
        self.source.write_text('{"PRIVATE-KEY":1,"PRIVATE-KEY":2}', encoding="utf-8")
        output = self.directory / "must-not-exist.json"
        self.assertEqual((1, "", cli.ACTION_ERROR), self.invoke(
            ["catalog", "--source", self.source, "--output", output]))
        self.assertFalse(output.exists())

    def test_direct_script_root_import_from_unrelated_directory(self):
        result = subprocess.run([sys.executable, "-I", "-B", str(ROOT / "scripts/vps_adapter.py"),
                                 "catalog", "--source", str(self.source),
                                 "--output", str(self.directory / "subprocess-output.json")],
                                cwd=self.directory, capture_output=True, text=True, timeout=30)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("", result.stderr)
        self.assertEqual(1, json.loads(result.stdout)["offers"])


if __name__ == "__main__":
    unittest.main()
