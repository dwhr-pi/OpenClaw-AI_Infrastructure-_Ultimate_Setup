"""Offline standard-library tests; all provider claims below are synthetic."""

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.vps.catalog import (
    CatalogError, DIMENSION_FIELDS, MAX_JSON_BYTES, get_offer,
    import_catalog, load_catalog,
)


STAMP = "2020-02-20T10:00:00Z"


def record(identifier="fixture", group="gratis", art="VM"):
    return {
        "id": identifier, "name": "Synthetic " + identifier,
        "gruppe": group, "art": art, "geprueft_am": "2020-02-19",
        "registrierung": ["Human contract acceptance"],
        "automatisierung": "VM API after legitimate account registration",
        "agent_registrierung": "No proven signup API",
        "mining": "Not evidenced", "ki": "Not evidenced",
        "extra": {"nested": ["preserve this verbatim", 3, False]},
    }


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "fixture.json"

    def write(self, value):
        self.path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
        return self.path

    def source(self, records=None, **kwargs):
        value = {"schema_version": 1, "recherchiert_am": "2020-02-19",
                 "angebote": [record()] if records is None else records}
        value.update(kwargs)
        return value

    def imported(self, records=None):
        return import_catalog(self.write(self.source(records)), retrieved_at=STAMP)

    def test_all_56_records_preserved_with_conservative_families(self):
        families = [
            ("gratis", "VM (AMD64)", "vm"),
            ("gratis", "Linux-Systemcontainer, Root", "system_container"),
            ("alternative", "App-/Shared-Hosting, kein Root-VPS", "app_hosting"),
            ("alternative", "Kurzlebiger CI-Runner", "ci_runner"),
            ("trial", "VM", "trial"),
            ("zweckgebunden", "Brokergebundener Trading-VPS", "broker_funded"),
            ("rueckerstattung", "VM", "refund"),
            ("kandidat", "Beworbene KVM-VM", "unverified"),
            ("historisch", "KVM-VM, historisch", "historical"),
        ]
        records = [record(str(i), *families[i % len(families)][:2]) for i in range(56)]
        catalog = self.imported(records)
        self.assertEqual(56, len(catalog["offers"]))
        for i, offer in enumerate(catalog["offers"]):
            self.assertEqual(families[i % len(families)][2], offer["kind"])
            self.assertEqual(records[i], offer["source_fields"])
            self.assertIsNone(offer["content_reviewed_at"])
            self.assertEqual("2020-02-19", offer["source_claimed_reviewed_on"])
            self.assertTrue(set(DIMENSION_FIELDS).issubset(offer["dimensions"]))
            for key, dimension in offer["dimensions"].items():
                self.assertEqual("unverified", dimension["state"])
                self.assertEqual(records[i].get(key), dimension["value"])

    def test_provenance_exact_bytes_and_no_mutable_aliases(self):
        original = self.source()
        path = self.write(original)
        raw = path.read_bytes()
        catalog = import_catalog(path, retrieved_at=STAMP, source_head="a" * 40)
        self.assertEqual(hashlib.sha256(raw).hexdigest(), catalog["source"]["sha256"])
        self.assertEqual("a" * 40, catalog["source"]["head"])
        self.assertEqual("https://github.com/dwhr-pi/Free-VPS", catalog["source"]["repository"])
        self.assertEqual("2020-02-19", catalog["source"]["source_claimed_reviewed_on"])
        self.assertEqual(STAMP, catalog["retrieved_at"])
        offer = catalog["offers"][0]
        offer["dimensions"]["extra"]["value"]["nested"].append("change")
        self.assertEqual(original["angebote"][0], offer["source_fields"])

    def test_registration_api_is_not_signup_permission(self):
        offer = self.imported()["offers"][0]
        self.assertEqual({"state": "human_action_required"}, offer["registration"])
        for group in ["kandidat", "ausgeschlossen", "historisch"]:
            offer = self.imported([record(group=group)])["offers"][0]
            self.assertIn(offer["registration"]["state"], {"terms_unclear", "unsupported"})

    def test_ambiguous_families_remain_unverified(self):
        for art in ["Gesponserter VPS", "IPv6-VPS, Technik je nach Node",
                    "Entwicklungsumgebung, kein dauerhafter VPS", "unknown"]:
            self.assertEqual("unverified", self.imported([record(art=art)])["offers"][0]["kind"])

    def test_unrecognized_metadata_types_do_not_grant_classification(self):
        for group in [None, [], {}, 42]:
            with self.subTest(group=group):
                offer = self.imported([record(group=group)])["offers"][0]
                self.assertEqual("unverified", offer["kind"])
                self.assertEqual("terms_unclear", offer["registration"]["state"])
                self.assertEqual(group, offer["source_fields"]["gruppe"])

    def test_directory_input_and_invalid_head_rejected(self):
        with self.assertRaises(CatalogError):
            import_catalog(self.directory.name)
        self.write(self.source())
        for head in [True, 42, "", "line\nbreak", "x" * 201]:
            with self.subTest(head=head), self.assertRaises(CatalogError):
                import_catalog(self.path, retrieved_at=STAMP, source_head=head)

    def test_missing_review_dates_stay_null_even_with_http_200(self):
        source = self.source()
        del source["recherchiert_am"]
        del source["angebote"][0]["geprueft_am"]
        source["angebote"][0]["http_status"] = 200
        catalog = import_catalog(self.write(source), retrieved_at=STAMP)
        self.assertIsNone(catalog["source"]["source_claimed_reviewed_on"])
        self.assertIsNone(catalog["offers"][0]["source_claimed_reviewed_on"])
        self.assertIsNone(catalog["offers"][0]["content_reviewed_at"])

    def test_bad_source_review_dates_rejected(self):
        for value in ["yesterday", "2020-02-30", "2020-2-19", "2099-01-01", 200, True, "2020-02-19T00:00:00Z"]:
            for location in ["root", "offer"]:
                with self.subTest(value=value, location=location):
                    source = self.source()
                    if location == "root":
                        source["recherchiert_am"] = value
                    else:
                        source["angebote"][0]["geprueft_am"] = value
                    with self.assertRaises(CatalogError):
                        import_catalog(self.write(source), retrieved_at=STAMP)

    def test_retrieval_timestamp_validation_and_utc_normalization(self):
        self.write(self.source())
        for stamp in ["invalid", "2020-02-20", "2020-02-20T00:00:00", "2099-01-01T00:00:00Z", True]:
            with self.subTest(stamp=stamp), self.assertRaises(CatalogError):
                import_catalog(self.path, retrieved_at=stamp)
        for stamp in ["2020-02-20T11:00:00+01:00", datetime(2020, 2, 20, 10, tzinfo=timezone.utc)]:
            self.assertEqual(STAMP, import_catalog(self.path, retrieved_at=stamp)["retrieved_at"])
        self.assertTrue(import_catalog(self.path)["retrieved_at"].endswith("Z"))

    def test_invalid_json_duplicate_keys_nonfinite_and_depth(self):
        payloads = [b'{"a":1,"a":2}', b'{"nested":{"a":1,"a":2}}',
                    b'{"x":NaN}', b'{"x":Infinity}', b'{"x":-Infinity}',
                    b'{"x":1e9999}', b'[]', b'{', b'\xff',
                    b'{"x":' + b'[' * 70 + b'0' + b']' * 70 + b'}']
        for payload in payloads:
            with self.subTest(payload=payload[:50]):
                self.path.write_bytes(payload)
                for reader in [import_catalog, load_catalog]:
                    with self.assertRaises(CatalogError):
                        reader(self.path)

    def test_size_limit_on_source_and_snapshot(self):
        self.path.write_bytes(b" " * (MAX_JSON_BYTES + 1))
        for reader in [import_catalog, load_catalog]:
            with self.assertRaises(CatalogError):
                reader(self.path)
        raw = json.dumps(self.source()).encode()
        self.path.write_bytes(raw + b" " * (MAX_JSON_BYTES - len(raw)))
        self.assertEqual(1, len(import_catalog(self.path, retrieved_at=STAMP)["offers"]))

    def test_source_shape_and_duplicate_ids(self):
        for source in [self.source([record(), record()]), self.source([None]),
                       self.source(angebote={}), self.source(schema_version=True),
                       self.source(schema_version=2), self.source([{"id": "x"}]),
                       self.source([record(identifier=" ")])]:
            with self.subTest(source=source), self.assertRaises(CatalogError):
                import_catalog(self.write(source), retrieved_at=STAMP)

    def test_snapshot_roundtrip_and_lookup(self):
        catalog = self.imported()
        loaded = load_catalog(self.write(catalog))
        self.assertEqual(catalog, loaded)
        self.assertIs(get_offer(loaded, "fixture"), loaded["offers"][0])
        with self.assertRaises(KeyError):
            get_offer(loaded, "absent")
        loaded["offers"].append(loaded["offers"][0])
        with self.assertRaises(CatalogError):
            get_offer(loaded, "fixture")

    def test_snapshot_tampering_rejected(self):
        catalog = self.imported()
        mutations = [
            lambda c: c.update(schema_version=True),
            lambda c: c.pop("retrieved_at"),
            lambda c: c.update(retrieved_at="2099-01-01T00:00:00Z"),
            lambda c: c["source"].update(sha256="wrong"),
            lambda c: c["source"].update(repository="https://invalid.test"),
            lambda c: c["source"].pop("head"),
            lambda c: c["source"].update(source_claimed_reviewed_on="2099-01-01"),
            lambda c: c["offers"].append(deepcopy(c["offers"][0])),
            lambda c: c["offers"][0].update(content_reviewed_at=STAMP),
            lambda c: c["offers"][0]["registration"].update(state="allowed"),
            lambda c: c["offers"][0]["dimensions"]["mining"].update(state="allowed"),
            lambda c: c["offers"][0].update(kind="vm_approved"),
            lambda c: c["offers"][0].update(source_claimed_reviewed_on="2099-01-01"),
            lambda c: c["offers"][0].pop("dimensions"),
        ]
        for mutate in mutations:
            candidate = deepcopy(catalog)
            mutate(candidate)
            with self.subTest(mutation=mutate), self.assertRaises(CatalogError):
                load_catalog(self.write(candidate))

    def test_no_network_execution_or_writes_during_import(self):
        self.write(self.source())
        original = self.path.read_bytes()
        real_open = Path.open

        def read_only(path, mode="r", *args, **kwargs):
            self.assertEqual("rb", mode)
            return real_open(path, mode, *args, **kwargs)

        with patch("pathlib.Path.open", read_only), \
                patch("socket.socket", side_effect=AssertionError("network")), \
                patch("subprocess.Popen", side_effect=AssertionError("execution")), \
                patch("os.system", side_effect=AssertionError("execution")):
            import_catalog(self.path, retrieved_at=STAMP)
        self.assertEqual(original, self.path.read_bytes())
        self.assertEqual([self.path], list(Path(self.directory.name).iterdir()))


if __name__ == "__main__":
    unittest.main()
