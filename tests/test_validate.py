"""Mutation checks: demonstrate detection without modifying the working pack."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
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


if __name__ == "__main__":
    unittest.main()
