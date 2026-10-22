"""Mutation checks: demonstrate detection without modifying the working pack."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validate", ROOT / "scripts/validate.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for directory in ("prompts", "reference-prisms"):
            shutil.copytree(ROOT / directory, self.root / directory)

    def mutate(self, name, old, new):
        path = self.root / name
        text = path.read_text()
        self.assertIn(old, text)
        path.write_text(text.replace(old, new))

    def rules(self):
        return {item["rule"] for item in validator.validate(self.root)["errors"]}

    def test_repository_passes(self):
        self.assertTrue(validator.validate(ROOT)["ok"])

    def test_missing_prompt(self):
        (self.root / "prompts/prism-scan.md").unlink()
        self.assertIn("missing_prompt", self.rules())

    def test_missing_save_guard(self):
        self.mutate("prompts/prism-reflect.md", "Do not write files unless the user explicitly requests saving", "Always save")
        self.assertIn("missing_boundary", self.rules())

    def test_forced_conclusion(self):
        path = self.root / "prompts/prism-3way.md"
        with path.open("a") as stream:
            stream.write("\nProve these three properties CANNOT all coexist.\n")
        self.assertIn("contradictory_mandate", self.rules())

    def test_reviewed_contradictions(self):
        cases = (
            ("prompts/prism-scan.md", "End with bugs, not just observations."),
            ("reference-prisms/simulation.md", "Apply this law to your own simulation."),
            ("reference-prisms/error_resilience.md", "trace forward through ALL downstream code"),
        )
        for name, mandate in cases:
            with self.subTest(name=name):
                path = self.root / name
                original = path.read_text()
                path.write_text(original + "\n" + mandate)
                self.assertIn("contradictory_mandate", self.rules())
                path.write_text(original)

    def test_discovery_opener(self):
        self.mutate("prompts/prism-discover.md", "Return only a numbered list", "First show the generated lens")
        self.assertIn("discovery_format", self.rules())

    def test_measurement_guard(self):
        self.mutate("reference-prisms/optimize.md", "Never invent timing", "Estimate timing freely")
        self.assertIn("measurement_provenance", self.rules())

    def test_broken_local_link(self):
        (self.root / "links.md").write_text("[missing](missing.md)\n[external](https://example.invalid)\n[anchor](#unknown)\n")
        result = validator.validate(self.root)
        self.assertEqual([e["detail"] for e in result["errors"]], ["missing.md"])

    def test_titled_and_angle_links(self):
        (self.root / "links.md").write_text(
            '[docs](missing.md "Docs")\n[more](<also missing.md> \'More\')\n'
        )
        errors = validator.validate(self.root)["errors"]
        self.assertEqual([e["detail"] for e in errors], ["missing.md", "also missing.md"])

    def test_encoded_paths_and_balanced_parentheses(self):
        (self.root / "a file(1).md").write_text("hello")
        (self.root / "links.md").write_text(
            '[a](a%20file(1).md#section "A")\n[b](<a file(1).md>)\n'
            '[remote](//example.invalid/docs)\n'
        )
        self.assertTrue(validator.validate(self.root)["ok"])

    def test_code_samples_are_not_links(self):
        (self.root / "links.md").write_text(
            '```text\n[example](missing.md)\n```\n'
            '~~~md\n[example](missing2.md)\n~~~\n'
            '`[example](missing3.md)` and ``[example](missing4.md)``\n\n'
            '    [example](missing5.md)\n[real](missing6.md)\n'
        )
        errors = validator.validate(self.root)["errors"]
        self.assertEqual([e["detail"] for e in errors], ["missing6.md"])

    def test_indented_paragraph_continuation_is_prose(self):
        for indent in ("    ", "\t"):
            with self.subTest(indent=indent):
                (self.root / "links.md").write_text(f"Intro\n{indent}[docs](missing.md)\n")
                errors = validator.validate(self.root)["errors"]
                self.assertEqual([e["detail"] for e in errors], ["missing.md"])

    def test_unicode_spacing_text_does_not_end_a_paragraph(self):
        for text in ("\u00a0", "\u2003"):
            with self.subTest(text=text):
                (self.root / "links.md").write_text(f"Intro\n{text}\n    [docs](missing.md)\n")
                errors = validator.validate(self.root)["errors"]
                self.assertEqual([e["detail"] for e in errors], ["missing.md"])

    def test_actual_indented_code_after_block_boundary_is_ignored(self):
        for prefix in ("", "Intro\n\n", "# Heading\n", "---\n", "Title\n===\n"):
            with self.subTest(prefix=prefix):
                (self.root / "links.md").write_text(prefix + "    [docs](missing.md)\n")
                self.assertTrue(validator.validate(self.root)["ok"])

    def test_setext_marker_without_heading_text_starts_a_paragraph(self):
        (self.root / "links.md").write_text("===\n    [docs](missing.md)\n")
        errors = validator.validate(self.root)["errors"]
        self.assertEqual([e["detail"] for e in errors], ["missing.md"])

    def test_escaped_closing_bracket_in_label(self):
        (self.root / "links.md").write_text(r"[API \] notes](missing.md)" + "\n")
        errors = validator.validate(self.root)["errors"]
        self.assertEqual([e["detail"] for e in errors], ["missing.md"])

    def test_inline_code_requires_equal_length_delimiters(self):
        (self.root / "links.md").write_text('`literal `` [docs](missing.md) tail`\n')
        self.assertTrue(validator.validate(self.root)["ok"])

    def test_escaped_backtick_does_not_hide_real_links(self):
        (self.root / "links.md").write_text('\\`literal [docs](missing.md) tail`\n')
        errors = validator.validate(self.root)["errors"]
        self.assertEqual([e["detail"] for e in errors], ["missing.md"])

    def test_code_spans_do_not_cross_paragraphs(self):
        (self.root / "links.md").write_text('`unclosed\n\n[docs](missing.md) tail`\n')
        errors = validator.validate(self.root)["errors"]
        self.assertEqual([e["detail"] for e in errors], ["missing.md"])

    def test_backticks_in_link_destination_are_literal(self):
        (self.root / "a`b`c.md").write_text("target")
        (self.root / "links.md").write_text('[docs](<a`b`c.md>)\n')
        self.assertTrue(validator.validate(self.root)["ok"])

    def test_code_span_cannot_join_disconnected_link_syntax(self):
        (self.root / "links.md").write_text('[docs]`example`(missing.md)\n')
        self.assertTrue(validator.validate(self.root)["ok"])

    def test_invalid_utf8_is_a_diagnostic(self):
        for name in ("prompts/prism-scan.md", "extra.md"):
            with self.subTest(name=name):
                path = self.root / name
                original = path.read_bytes() if path.exists() else b""
                path.write_bytes(b"\xff")
                try:
                    result = validator.validate(self.root)
                except UnicodeError as exc:
                    self.fail(f"validator crashed instead of reporting invalid UTF-8: {exc}")
                self.assertIn({"path": name, "rule": "invalid_utf8"}, result["errors"])
                path.write_bytes(original)

    def test_new_prompts_are_not_silently_ignored(self):
        (self.root / "prompts/prism-extra.md").write_text("No boundaries")
        result = validator.validate(self.root)
        self.assertTrue(any(e["path"] == "prompts/prism-extra.md" and
                            e["rule"] == "missing_boundary" for e in result["errors"]))

    def test_forced_tradeoff_is_detected(self):
        path = self.root / "reference-prisms/deep_scan.md"
        path.write_text(path.read_text() + "\nFind the fundamental trade-off the system is managing.")
        self.assertIn("contradictory_mandate", self.rules())

    def test_cli_reports_invalid_file_as_json(self):
        (self.root / "bad.md").write_bytes(b"\xff")
        run = subprocess.run([sys.executable, str(ROOT / "scripts/validate.py"),
                              "--root", str(self.root), "--json"], capture_output=True, text=True)
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertEqual(run.stderr, "")
        self.assertFalse(json.loads(run.stdout)["ok"])


if __name__ == "__main__":
    unittest.main()
