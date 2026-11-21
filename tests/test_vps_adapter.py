"""Offline adapter contracts: synthetic identities, no real transport or key reads."""

import base64
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from tools.vps import adapter


NOW = datetime(2026, 11, 18, 12, tzinfo=timezone.utc)
BOOTSTRAP = b"synthetic bootstrap fixture, never executed\n"
TOKEN = "SYNTHETIC-NOT-A-CREDENTIAL"


def public_key(byte=1):
    prefix = b"\x00\x00\x00\x0bssh-ed25519\x00\x00\x00\x20"
    return "ssh-ed25519 " + base64.b64encode(prefix + bytes([byte]) * 32).decode()


def fixture_plan():
    return {
        "version": 1, "provider": "gcp", "account_ref": "fixture-project",
        "region": "europe-west3", "zone": "europe-west3-a",
        "resource_name": "fixture-vm", "resource_id": "123456789",
        "sku": "e2-small", "os_image": "projects/ubuntu-os-cloud/global/images/fixture-image",
        "architecture": "x86_64", "usage": "monitoring", "offer_id": "gcp",
        "owner": "fixture-owner", "dedicated_host": True,
        "bootstrap_sha256": hashlib.sha256(BOOTSTRAP).hexdigest(),
        "service_public_key": public_key(2),
        "pricing": {"currency": "EUR", "hourly": "0.10", "setup": "1.00",
                    "extras": "0.20", "tax": "0.30", "reviewed_on": "2026-11-17",
                    "source_url": "https://pricing.example.invalid/fixture"},
        "budget": {"amount": "2.50", "hours": 10},
        "review": {"usage_state": "allowed", "account_state": "existing_account_required",
                   "reviewed_on": "2026-11-17", "source_url": "https://terms.example.invalid/fixture"},
        "ssh": {"host": "192.0.2.10", "port": 22, "user": "fixtureadmin",
                "recovery_user": "fixturerecovery", "key_env": "OPENCLAW_VPS_TEST_KEY",
                "recovery_key_env": "OPENCLAW_VPS_TEST_RECOVERY_KEY",
                "known_hosts_env": "OPENCLAW_VPS_TEST_KNOWN_HOSTS",
                "api_token_env": "OPENCLAW_VPS_TEST_TOKEN",
                "host_fingerprint": adapter.hostkey_fingerprint(public_key())},
    }


def fixture_auth(plan, actions=None):
    return {"version": 1, "plan_hash": adapter.digest(plan),
            "actions": list(adapter.ACTIONS) if actions is None else actions,
            "valid_from": (NOW - timedelta(minutes=5)).isoformat(),
            "expires_at": (NOW + timedelta(minutes=5)).isoformat(),
            "budget_amount": plan["budget"]["amount"], "max_hours": plan["budget"]["hours"],
            "max_resources": 1}


def fixture_resource(plan):
    base = "https://www.googleapis.com/compute/v1/projects/" + plan["account_ref"]
    zone = base + "/zones/" + plan["zone"]
    return {"id": plan["resource_id"], "name": plan["resource_name"],
            "zone": zone, "machineType": zone + "/machineTypes/" + plan["sku"],
            "status": "RUNNING", "labels": {"openclaw-owner": plan["owner"],
                                              "openclaw-plan": adapter.digest(plan)[:32]},
            "networkInterfaces": [{"networkIP": "10.0.0.2", "accessConfigs": [
                {"natIP": plan["ssh"]["host"]}]}]}


def fixture_facts(**changes):
    value = {"system": "Linux", "architecture": "x86_64", "cpu": 2,
             "free_disk": 80 * 1024**3, "memory_pages": 2097152, "page_size": 4096,
             "os_release": {"ID": "ubuntu", "VERSION_ID": "24.04"},
             "existing_llmops": False, "cgroups": True, "tun": False,
             "kernel_scope": "metadata_only", "uid": 1001}
    value.update(changes)
    return value


def verified(**facts):
    return {"ssh_verified": True, "recovery_verified": True, "facts": fixture_facts(**facts)}


def stats(changed=0, failures=0, unreachable=0):
    return json.dumps({"stats": {"target": {"changed": changed, "failures": failures,
                                            "unreachable": unreachable}}}).encode()


class OfflineCase(unittest.TestCase):
    def setUp(self):
        # Trap live escape routes even when a test forgets an injected dependency.
        for target in ("socket.socket", "subprocess.Popen", "os.system",
                       "urllib.request.OpenerDirector.open", "multiprocessing.process.BaseProcess.start"):
            self.enterContext(patch(target, side_effect=AssertionError("live operation forbidden")))
        self.enterContext(patch.dict(os.environ, {}, clear=True))
        self.plan = fixture_plan()
        self.offer = {"id": "gcp", "kind": "vm"}
        self.auth = fixture_auth(self.plan)
        self.provider = Mock()
        self.provider.status.return_value = fixture_resource(self.plan)
        self.run = Mock(side_effect=AssertionError("unexpected process call"))

    def execute(self, action, **kwargs):
        options = {"authorization": self.auth, "provider": self.provider,
                   "run": self.run, "now": NOW}
        options.update(kwargs)
        return adapter.execute(action, self.plan, self.offer, **options)


class ValidationTests(OfflineCase):
    def test_valid_plan_decimal_estimate_and_no_execution_approval(self):
        result = adapter.validate(self.plan, self.offer, NOW)
        self.assertEqual("2.50", result["estimated_total"])
        self.assertEqual(adapter.digest(self.plan), result["plan_hash"])
        self.assertEqual("human_action_required", result["registration"])
        self.assertEqual("explicit_authorization_required", result["execution"])
        self.assertTrue(result["usage_ready"])
        self.assertIn("blocked", result["provision"])

    def test_unknown_or_missing_fields_rejected(self):
        for candidate in ({**self.plan, "command": "never-run"},
                          {k: v for k, v in self.plan.items() if k != "budget"}):
            with self.subTest(candidate=candidate), self.assertRaises(adapter.Guard):
                adapter.validate(candidate, self.offer, NOW)

    def test_nested_unknown_fields_rejected(self):
        for field in ("pricing", "budget", "review", "ssh"):
            plan = deepcopy(self.plan)
            plan[field]["unexpected"] = "fixture"
            with self.subTest(field=field), self.assertRaises(adapter.Guard):
                adapter.validate(plan, self.offer, NOW)

    def test_invalid_identifiers_and_types_rejected(self):
        cases = [("version", True), ("provider", "oracle"), ("account_ref", "../project"),
                 ("zone", "us-central1-a"), ("resource_name", "vm;command"),
                 ("resource_id", "not-an-id"), ("sku", "--flag"),
                 ("os_image", "latest"), ("architecture", "unknown"),
                 ("usage", "unknown"), ("dedicated_host", "false"),
                 ("bootstrap_sha256", "not-a-hash")]
        for field, value in cases:
            with self.subTest(field=field), self.assertRaises(adapter.Guard):
                adapter.validate({**self.plan, field: value}, self.offer, NOW)

    def test_offer_mismatch_and_non_vm_rejected(self):
        for offer in ({"id": "other", "kind": "vm"}, {"id": "gcp", "kind": "trial"}):
            with self.subTest(offer=offer), self.assertRaises(adapter.Guard):
                adapter.validate(self.plan, offer, NOW)

    def test_money_rejects_unknown_negative_nonfinite_and_float_prices(self):
        for value in (None, True, 0, 0.1, "unknown", "-1", "NaN", "Infinity", "1e3", "0.0000001"):
            with self.subTest(value=value), self.assertRaises(adapter.Guard):
                adapter.money(value)

    def test_price_components_and_hours_are_all_budgeted(self):
        plan = deepcopy(self.plan)
        plan["budget"]["amount"] = "2.49"
        with self.assertRaisesRegex(adapter.Guard, "planned_cost_exceeds_authorized_budget"):
            adapter.validate(plan, self.offer, NOW)
        for hours in (True, 0, 169, "10"):
            plan = deepcopy(self.plan)
            plan["budget"]["hours"] = hours
            with self.subTest(hours=hours), self.assertRaises(adapter.Guard):
                adapter.validate(plan, self.offer, NOW)

    def test_review_date_window_and_https_sources(self):
        for section in ("pricing", "review"):
            for field, value in (("reviewed_on", "2026-11-10"), ("reviewed_on", "2026-11-19"),
                                 ("reviewed_on", "bad"), ("source_url", "http://example.invalid")):
                plan = deepcopy(self.plan)
                plan[section][field] = value
                with self.subTest(section=section, field=field, value=value), self.assertRaises(adapter.Guard):
                    adapter.validate(plan, self.offer, NOW)
            plan = deepcopy(self.plan)
            plan[section]["reviewed_on"] = "2026-11-11"
            adapter.validate(plan, self.offer, NOW)

    def test_duplicate_and_nonfinite_json_rejected(self):
        for raw in (b'{"x":1,"x":2}', b'{"nested":{"x":1,"x":2}}', b'{"x":NaN}'):
            with self.subTest(raw=raw), self.assertRaises(adapter.Guard):
                adapter.strict_json(raw)

    def test_hash_is_order_independent_but_binds_plan_changes(self):
        self.assertEqual(adapter.digest(self.plan), adapter.digest(dict(reversed(list(self.plan.items())))))
        self.assertNotEqual(adapter.digest(self.plan), adapter.digest({**self.plan, "owner": "other-owner"}))


class AuthorizationTests(OfflineCase):
    def test_exact_start_valid_and_expiry_exclusive(self):
        adapter.authorize(self.plan, self.auth, "status", NOW)
        start = adapter.timestamp(self.auth["valid_from"])
        adapter.authorize(self.plan, self.auth, "status", start)
        for now in (start - timedelta(microseconds=1), adapter.timestamp(self.auth["expires_at"])):
            with self.subTest(now=now), self.assertRaisesRegex(adapter.Guard, "authorization_expired_or_unbounded"):
                adapter.authorize(self.plan, self.auth, "status", now)

    def test_invalid_or_unbounded_authorization_window(self):
        for changes in ({"valid_from": NOW.isoformat(), "expires_at": NOW.isoformat()},
                        {"expires_at": (NOW + timedelta(days=8)).isoformat()},
                        {"valid_from": "2026-11-18T11:59:00"}, {"expires_at": "bad"}):
            with self.subTest(changes=changes), self.assertRaises(adapter.Guard):
                adapter.authorize(self.plan, {**self.auth, **changes}, "status", NOW)

    def test_authorization_schema_version_and_plan_binding(self):
        for changes in ({"version": True}, {"version": 2}, {"plan_hash": "a" * 64}, {"extra": True}):
            with self.subTest(changes=changes), self.assertRaises(adapter.Guard):
                adapter.authorize(self.plan, {**self.auth, **changes}, "status", NOW)

    def test_action_scope_is_mandatory(self):
        for actions in ([], "status", ["verify"], ["status", "signup"]):
            with self.subTest(actions=actions), self.assertRaisesRegex(adapter.Guard, "authorization_scope_missing"):
                adapter.authorize(self.plan, {**self.auth, "actions": actions}, "status", NOW)

    def test_budget_hours_and_single_resource_must_match(self):
        for field, value in (("budget_amount", "2.49"), ("budget_amount", "2.51"),
                             ("max_hours", 9), ("max_hours", True),
                             ("max_resources", 0), ("max_resources", 2), ("max_resources", True)):
            with self.subTest(field=field, value=value), self.assertRaises(adapter.Guard):
                adapter.authorize(self.plan, {**self.auth, field: value}, "status", NOW)

    def test_equivalent_decimal_budget_is_accepted(self):
        adapter.authorize(self.plan, {**self.auth, "budget_amount": "2.500000"}, "status", NOW)


class DispatchTests(OfflineCase):
    def test_no_apply_and_plans_never_read_environment_or_call_provider(self):
        with patch.object(adapter.os.environ, "get", side_effect=AssertionError("environment read")):
            for action in ("plan", "validate", "status", "verify", "configure", "provision", "teardown"):
                with self.subTest(action=action):
                    result = self.execute(action, authorization=None)
                    self.assertNotEqual(True, result.get("executed"))
        self.provider.status.assert_not_called()
        self.run.assert_not_called()

    def test_provision_is_blocked_before_environment_and_provider_construction(self):
        with patch.object(adapter.os.environ, "get", side_effect=AssertionError("environment read")), \
                patch.object(adapter, "GcpAdapter", side_effect=AssertionError("provider constructed")):
            with self.assertRaisesRegex(adapter.Guard, "provision_blocked_no_hard_cost_and_lifetime_enforcement"):
                self.execute("provision", apply=True, provider=None)
        self.provider.status.assert_not_called()

    def test_missing_or_expired_authorization_never_contacts_provider(self):
        for authorization in (None, {**self.auth, "expires_at": NOW.isoformat()}):
            with self.subTest(authorization=authorization), self.assertRaises(adapter.Guard):
                self.execute("status", apply=True, authorization=authorization)
        self.provider.status.assert_not_called()
        self.run.assert_not_called()

    def test_all_inspection_and_configure_actions_require_existing_account(self):
        for account in ("human_action_required", "terms_unclear", "unavailable", "unsupported"):
            self.plan["review"]["account_state"] = account
            self.auth = fixture_auth(self.plan)
            for action in ("status", "verify", "configure"):
                with self.subTest(account=account, action=action), \
                        self.assertRaisesRegex(adapter.Guard, "human_account_or_terms_verification_required"):
                    self.execute(action, apply=True)
        self.provider.status.assert_not_called()

    def test_configure_requires_allowed_usage_and_dedicated_host(self):
        for section, field, value in (("review", "usage_state", "forbidden"),
                                      ("review", "usage_state", "unverified"),
                                      (None, "dedicated_host", False)):
            self.plan = fixture_plan()
            (self.plan[section] if section else self.plan)[field] = value
            self.auth = fixture_auth(self.plan)
            with self.subTest(field=field, value=value), self.assertRaises(adapter.Guard):
                self.execute("configure", apply=True)
        self.provider.status.assert_not_called()

    def test_status_redacts_provider_body_and_only_reads_named_token(self):
        self.provider.status.return_value["private_provider_body"] = "SYNTHETIC-DO-NOT-RETURN"
        with patch.object(adapter.os.environ, "get", return_value=TOKEN) as get:
            result = self.execute("status", apply=True)
        get.assert_called_once_with(self.plan["ssh"]["api_token_env"])
        self.provider.status.assert_called_once_with(self.plan, TOKEN)
        self.assertTrue(result["ownership_verified"])
        self.assertEqual("RUNNING", result["state"])
        self.assertNotIn("SYNTHETIC", json.dumps(result))
        self.run.assert_not_called()

    def test_unknown_provider_state_is_not_echoed(self):
        self.provider.status.return_value["status"] = "SYNTHETIC-PRIVATE-STATUS"
        self.assertEqual("other", self.execute("status", apply=True)["state"])

    def test_verify_dispatches_with_injected_runner(self):
        with patch.object(adapter, "verify_ssh", return_value=verified()) as verify:
            self.assertTrue(self.execute("verify", apply=True)["recovery_verified"])
        verify.assert_called_once_with(self.plan, self.provider.status.return_value, self.run)

    def test_teardown_apply_and_unknown_actions_never_contact_provider(self):
        for action in ("teardown", "signup", "delete", "start"):
            with self.subTest(action=action), self.assertRaises(adapter.Guard):
                self.execute(action, apply=True)
        self.provider.status.assert_not_called()


class GcpStatusTests(OfflineCase):
    def client(self, responses, clock=None):
        transport = Mock(side_effect=responses)
        sleep = Mock()
        client = adapter.GcpAdapter(transport=transport, sleep=sleep, clock=clock or Mock(return_value=0))
        return client, transport, sleep

    def test_exact_project_zone_instance_url_and_bounded_request(self):
        data = fixture_resource(self.plan)
        client, transport, sleep = self.client([(200, data)])
        self.assertEqual(data, client.status(self.plan, TOKEN))
        transport.assert_called_once_with(
            "https://compute.googleapis.com/compute/v1/projects/fixture-project/zones/europe-west3-a/instances/fixture-vm",
            TOKEN, 12)
        sleep.assert_not_called()

    def test_transient_failures_retry_once_only(self):
        for failure in ((0, None), (429, None), (500, None), (502, None), (503, None),
                        (504, None), TimeoutError(), adapter.Guard("provider_timeout")):
            with self.subTest(failure=failure):
                client, transport, sleep = self.client([failure, (200, fixture_resource(self.plan))])
                client.status(self.plan, TOKEN)
                self.assertEqual(2, transport.call_count)
                sleep.assert_called_once_with(1)

    def test_permanent_failure_never_retries(self):
        for code in (301, 400, 401, 403, 404, 409):
            client, transport, sleep = self.client([(code, {"secret": "not-logged"})])
            with self.subTest(code=code), self.assertRaisesRegex(adapter.Guard, "^provider_status_failed_" + str(code) + "$"):
                client.status(self.plan, TOKEN)
            self.assertEqual(1, transport.call_count)
            sleep.assert_not_called()

    def test_repeated_transient_failure_stops_after_two_calls(self):
        client, transport, _ = self.client([(503, None)] * 3)
        with self.assertRaisesRegex(adapter.Guard, "provider_status_failed_503"):
            client.status(self.plan, TOKEN)
        self.assertEqual(2, transport.call_count)

    def test_deadline_prevents_request_and_clamps_remaining_timeout(self):
        client, transport, _ = self.client([], Mock(side_effect=[0, 31]))
        with self.assertRaisesRegex(adapter.Guard, "provider_timeout"):
            client.status(self.plan, TOKEN)
        transport.assert_not_called()
        client, transport, _ = self.client([(200, fixture_resource(self.plan))], Mock(side_effect=[0, 29]))
        client.status(self.plan, TOKEN)
        self.assertEqual(1, transport.call_args.args[2])

    def test_invalid_token_never_reaches_transport(self):
        client, transport, _ = self.client([])
        for token in (None, "", "token\nheader", "x" * 8193):
            with self.subTest(token_type=type(token).__name__), self.assertRaises(adapter.Guard):
                client.status(self.plan, token)
        transport.assert_not_called()

    def test_wrong_resource_owner_plan_location_or_sku_fail_without_retry(self):
        changes = [("id", "other"), ("name", "other"), ("zone", "zones/us-central1-a"),
                   ("machineType", "zones/europe-west3-a/machineTypes/a2-highgpu-1g"),
                   ("machineType", ""), ("labels", {}), ("labels", None),
                   ("labels", {"openclaw-owner": "wrong", "openclaw-plan": adapter.digest(self.plan)[:32]}),
                   ("labels", {"openclaw-owner": self.plan["owner"], "openclaw-plan": "wrong"})]
        for field, value in changes:
            data = fixture_resource(self.plan)
            data[field] = value
            client, transport, sleep = self.client([(200, data)])
            with self.subTest(field=field, value=value), self.assertRaises(adapter.Guard):
                client.status(self.plan, TOKEN)
            self.assertEqual(1, transport.call_count)
            sleep.assert_not_called()

    def test_non_object_response_fails_closed(self):
        client, _, _ = self.client([(200, [])])
        with self.assertRaisesRegex(adapter.Guard, "resource_identity_mismatch"):
            client.status(self.plan, TOKEN)


class SshTests(OfflineCase):
    def setUp(self):
        super().setUp()
        # No private key is created or opened: these are mocked file references.
        self.known = Mock()
        self.known.stat.return_value.st_size = 100
        self.known.read_text.return_value = self.plan["ssh"]["host"] + " " + public_key() + "\n"
        self.primary, self.recovery = Mock(), Mock()
        self.primary.samefile.return_value = False
        self.references = {self.plan["ssh"]["known_hosts_env"]: self.known,
                           self.plan["ssh"]["key_env"]: self.primary,
                           self.plan["ssh"]["recovery_key_env"]: self.recovery}
        self.enterContext(patch.object(adapter, "external_reference", side_effect=self.references.__getitem__))
        self.run = Mock(side_effect=[json.dumps(fixture_facts()).encode(),
                                     json.dumps(fixture_facts(uid=1002)).encode()])

    def test_two_pinned_connections_use_separate_users_keys_and_no_agent(self):
        result = adapter.verify_ssh(self.plan, fixture_resource(self.plan), self.run)
        self.assertTrue(result["recovery_verified"])
        self.assertFalse(result["k3s_join_allowed"])
        self.assertFalse(result["kernel_runtime_tested"])
        self.assertEqual(2, self.run.call_count)
        for call, user, key in zip(self.run.call_args_list,
                                   ("fixtureadmin", "fixturerecovery"), (self.primary, self.recovery)):
            args = call.args[0]
            self.assertEqual("ssh", args[0])
            self.assertIn(user + "@192.0.2.10", args)
            self.assertEqual(str(key), args[args.index("-i") + 1])
            for option in ("BatchMode=yes", "StrictHostKeyChecking=yes", "IdentitiesOnly=yes", "IdentityAgent=none"):
                self.assertIn(option, args)
            self.assertEqual(os.devnull, args[args.index("-F") + 1])
            self.assertEqual(30, call.kwargs["timeout"])
        self.assertEqual(False, result["facts"]["existing_llmops"])

    def test_host_not_in_provider_response_blocks_before_file_reference(self):
        data = fixture_resource(self.plan)
        data["networkInterfaces"] = []
        with patch.object(adapter, "external_reference", side_effect=AssertionError("file lookup")):
            with self.assertRaisesRegex(adapter.Guard, "host_not_bound_to_provider_resource"):
                adapter.verify_ssh(self.plan, data, self.run)
        self.run.assert_not_called()

    def test_missing_duplicate_or_mismatched_host_pin_blocks_ssh(self):
        host = self.plan["ssh"]["host"]
        for text in ("", host + " " + public_key(3), (host + " " + public_key() + "\n") * 2):
            self.known.read_text.return_value = text
            with self.subTest(text=text), self.assertRaisesRegex(adapter.Guard, "host_key_pin_mismatch"):
                adapter.verify_ssh(self.plan, fixture_resource(self.plan), self.run)
        self.run.assert_not_called()

    def test_oversized_host_key_file_rejected_before_read(self):
        self.known.stat.return_value.st_size = adapter.MAX_BYTES + 1
        with self.assertRaisesRegex(adapter.Guard, "host_key_file_too_large"):
            adapter.check_known_hosts(self.plan, self.known)
        self.known.read_text.assert_not_called()

    def test_extra_wildcard_host_key_must_not_expand_ssh_trust(self):
        self.known.read_text.return_value += "* " + public_key(3) + "\n"
        # Regression: merely finding the expected line is not exclusive pinning.
        with self.assertRaises(adapter.Guard):
            adapter.verify_ssh(self.plan, fixture_resource(self.plan), self.run)
        self.run.assert_not_called()

    def test_same_file_recovery_key_is_rejected_before_ssh(self):
        self.primary.samefile.return_value = True
        with self.assertRaisesRegex(adapter.Guard, "independent_recovery_key_files_required"):
            adapter.verify_ssh(self.plan, fixture_resource(self.plan), self.run)
        self.run.assert_not_called()

    def test_same_user_or_same_environment_reference_rejected_in_plan(self):
        for field, value in (("recovery_user", self.plan["ssh"]["user"]),
                             ("recovery_key_env", self.plan["ssh"]["key_env"]),
                             ("host", "example.invalid"), ("port", 2222)):
            plan = deepcopy(self.plan)
            plan["ssh"][field] = value
            with self.subTest(field=field), self.assertRaises(adapter.Guard):
                adapter.validate(plan, self.offer, NOW)

    def test_failed_recovery_never_reports_success(self):
        self.run.side_effect = [json.dumps(fixture_facts()).encode(), adapter.Guard("synthetic_ssh_failure")]
        with self.assertRaises(adapter.Guard):
            adapter.verify_ssh(self.plan, fixture_resource(self.plan), self.run)
        self.assertEqual(2, self.run.call_count)

    def test_wrong_remote_os_or_architecture_rejected(self):
        for changes in ({"system": "Windows"}, {"architecture": "mips"}, {"architecture": "aarch64"}):
            run = Mock(return_value=json.dumps(fixture_facts(**changes)).encode())
            with self.subTest(changes=changes), self.assertRaises(adapter.Guard):
                adapter.verify_ssh(self.plan, fixture_resource(self.plan), run)
            self.assertEqual(1, run.call_count)

    def test_arm64_plan_accepts_aarch64_metadata(self):
        self.plan["architecture"] = "arm64"
        run = Mock(return_value=json.dumps(fixture_facts(architecture="aarch64")).encode())
        self.assertTrue(adapter.verify_ssh(self.plan, fixture_resource(self.plan), run)["ssh_verified"])


class ConfigureTests(OfflineCase):
    def setUp(self):
        super().setUp()
        self.temp = self.enterContext(tempfile.TemporaryDirectory())
        self.base = Path(self.temp).resolve()
        self.source = self.base / "source"
        (self.source / "ansible").mkdir(parents=True)
        (self.source / "ansible/vps_bootstrap.yml").write_bytes(BOOTSTRAP)
        self.enterContext(patch.object(adapter, "ROOT", self.source))
        self.state_root = self.base / "private-state"
        self.enterContext(patch.object(adapter, "external_reference", side_effect=lambda name: self.base / name))
        self.post = Mock(return_value=verified(existing_llmops=True))

    def configure(self, run=None, ssh_result=None, **kwargs):
        options = {"run": self.run if run is None else run, "post_verify": self.post}
        options.update(kwargs)
        return adapter.configure(self.plan, self.state_root,
                                 verified() if ssh_result is None else ssh_result, **options)

    def state(self):
        return self.state_root / (adapter.digest(self.plan) + ".json")

    def write_state(self, record):
        self.state_root.mkdir(mode=0o700, exist_ok=True)
        self.state().write_text(json.dumps(record), encoding="utf-8")

    def test_first_configuration_checks_applies_checks_recovery_then_commits(self):
        captured = []

        def run(command, timeout):
            self.assertEqual(900, timeout)
            self.assertEqual("intent", json.loads(self.state().read_text())["phase"])
            inventory = json.loads(Path(command[command.index("-i") + 1]).read_text())
            variables = json.loads(Path(command[command.index("--extra-vars") + 1][1:]).read_text())
            target = inventory["all"]["children"]["vps"]["hosts"]["target"]
            self.assertEqual(self.plan["ssh"]["host"], target["ansible_host"])
            self.assertEqual(self.plan["ssh"]["user"], target["ansible_user"])
            self.assertIn("StrictHostKeyChecking=yes", target["ansible_ssh_common_args"])
            self.assertIn("ControlMaster=no", target["ansible_ssh_common_args"])
            self.assertIn("ControlPersist=no", target["ansible_ssh_common_args"])
            self.assertTrue(variables["bootstrap_key_access_confirmed"])
            self.assertEqual(self.plan["service_public_key"], variables["llmops_ssh_public_key"])
            captured.append(command)
            return stats(changed=0 if len(captured) == 3 else 1)

        result = self.configure(run=run)
        self.assertEqual([True, False, True], ["--check" in command for command in captured])
        self.post.assert_called_once_with()
        self.assertEqual({"plan_hash": adapter.digest(self.plan), "phase": "configured"},
                         json.loads(self.state().read_text()))
        self.assertEqual([self.state()], list(self.state_root.iterdir()))
        self.assertTrue(result["idempotence_check_passed"])
        self.assertTrue(result["host_services_may_change"])
        self.assertFalse(result["model_or_cluster_start_requested"])
        if os.name == "posix":
            self.assertEqual(0o600, self.state().stat().st_mode & 0o777)

    def test_repeat_configured_skips_existing_account_guard_and_apply(self):
        self.write_state({"plan_hash": adapter.digest(self.plan), "phase": "configured"})
        run = Mock(return_value=stats())
        self.assertTrue(self.configure(run=run, ssh_result=verified(existing_llmops=True))["configured"])
        self.assertEqual(2, run.call_count)
        self.assertTrue(all("--check" in call.args[0] for call in run.call_args_list))
        self.post.assert_called_once_with()

    def test_first_configuration_requires_explicit_absence_of_existing_llmops(self):
        for value in (True, None, 0, "false"):
            with self.subTest(value=value), self.assertRaisesRegex(
                    adapter.Guard, "existing_service_account_requires_separate_migration"):
                self.configure(ssh_result=verified(existing_llmops=value))
            self.assertFalse(self.state().exists())
        missing = verified()
        del missing["facts"]["existing_llmops"]
        with self.assertRaises(adapter.Guard):
            self.configure(ssh_result=missing)
        self.run.assert_not_called()

    def test_source_hash_mismatch_blocks_before_journal_or_process(self):
        (self.source / "ansible/vps_bootstrap.yml").write_bytes(b"changed fixture")
        with self.assertRaisesRegex(adapter.Guard, "bootstrap_source_changed_since_authorization"):
            self.configure()
        self.assertFalse(self.state_root.exists())
        self.run.assert_not_called()

    def test_dedicated_host_and_recovery_required_before_writes(self):
        for field in ("dedicated", "recovery"):
            self.plan["dedicated_host"] = field != "dedicated"
            result = verified()
            result["recovery_verified"] = field != "recovery"
            with self.subTest(field=field), self.assertRaises(adapter.Guard):
                self.configure(ssh_result=result)
        self.assertFalse(self.state_root.exists())

    def test_incomplete_or_wrong_plan_journal_never_runs_ansible(self):
        for record in ({"plan_hash": adapter.digest(self.plan), "phase": "intent"},
                       {"plan_hash": "a" * 64, "phase": "configured"}):
            self.write_state(record)
            with self.subTest(record=record), self.assertRaisesRegex(
                    adapter.Guard, "prior_incomplete_operation_requires_review"):
                self.configure()
        self.run.assert_not_called()

    def test_ansible_failures_leave_intent_and_block_replay(self):
        scenarios = [(stats(failures=1),), (stats(unreachable=1),), (b'{}',),
                     (stats(), stats(failures=1)), (stats(), stats(), stats(changed=1))]
        for index, responses in enumerate(scenarios):
            self.state_root = self.base / ("failure-" + str(index))
            run = Mock(side_effect=responses)
            with self.subTest(index=index), self.assertRaises(adapter.Guard):
                self.configure(run=run)
            self.assertEqual("intent", json.loads(self.state().read_text())["phase"])
            replay = Mock(side_effect=AssertionError("unsafe replay"))
            with self.assertRaisesRegex(adapter.Guard, "prior_incomplete_operation_requires_review"):
                self.configure(run=replay)
            self.assertFalse(list(self.state_root.glob("*.lock")))
        self.post.assert_not_called()

    def test_missing_or_failed_post_recovery_does_not_mark_configured(self):
        for index, post in enumerate((None, Mock(return_value={"recovery_verified": False}),
                                      Mock(side_effect=adapter.Guard("recovery_lost")))):
            self.state_root = self.base / ("post-" + str(index))
            with self.subTest(index=index), self.assertRaises(adapter.Guard):
                self.configure(run=Mock(return_value=stats()), post_verify=post)
            self.assertEqual("intent", json.loads(self.state().read_text())["phase"])

    def test_runner_exception_cleans_lock_but_preserves_intent(self):
        with self.assertRaisesRegex(adapter.Guard, "synthetic_failure"):
            self.configure(run=Mock(side_effect=adapter.Guard("synthetic_failure")))
        self.assertEqual("intent", json.loads(self.state().read_text())["phase"])
        self.assertEqual([self.state()], list(self.state_root.iterdir()))

    def test_journal_lock_blocks_reentry_and_releases_after_exception(self):
        with self.assertRaisesRegex(adapter.Guard, "synthetic_abort"):
            with adapter.journal(self.state_root, self.plan):
                with self.assertRaisesRegex(adapter.Guard, "operation_already_active_or_needs_review"):
                    with adapter.journal(self.state_root, self.plan):
                        self.fail("lock bypass")
                raise adapter.Guard("synthetic_abort")
        self.assertFalse(list(self.state_root.glob("*.lock")))
        with adapter.journal(self.state_root, self.plan):
            pass

    def test_journal_rejects_repo_local_or_relative_state(self):
        for root in (Path("relative-state"), self.source / "state"):
            with self.subTest(root=root), self.assertRaises(adapter.Guard):
                with adapter.journal(root, self.plan):
                    self.fail("invalid journal accepted")

    def test_execute_configure_wires_post_verification_without_real_ssh(self):
        with patch.object(adapter, "verify_ssh", return_value=verified()) as verify, \
                patch.object(adapter, "configure", return_value={"configured": True}) as configure:
            if os.name != "posix":
                with self.assertRaisesRegex(adapter.Guard, "live_configuration_requires_posix_controller"):
                    self.execute("configure", apply=True, state_root=self.state_root)
                configure.assert_not_called()
            else:
                self.assertTrue(self.execute("configure", apply=True, state_root=self.state_root)["configured"])
                configure.call_args.kwargs["post_verify"]()
                self.assertEqual(2, verify.call_count)


if __name__ == "__main__":
    unittest.main()
