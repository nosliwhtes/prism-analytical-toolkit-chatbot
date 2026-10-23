"""Mutation checks: demonstrate detection without modifying the working pack."""
import importlib.util
import json
import os
from pathlib import Path, PureWindowsPath
import shutil
import tempfile
import subprocess
import sys
import stat
from types import SimpleNamespace
import unittest
from unittest.mock import patch

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

    def test_markdown_inventory_respects_platform_case_matching(self):
        (self.root / "EXTRA.MD").write_text("[missing](missing.txt)\n")
        # Emulate case normalization without claiming native Windows execution.
        with patch.object(os.path, "normcase", lambda name: name.lower()):
            errors = validator.validate(self.root)["errors"]
        self.assertIn({"path": "EXTRA.MD", "rule": "broken_local_link", "detail": "missing.txt"},
                      errors)

    @unittest.skipUnless(os.name == "posix", "synthetic local symlinks")
    def test_source_symlinks_are_not_opened_or_traversed(self):
        with tempfile.TemporaryDirectory() as outside:
            external = Path(outside)
            (external / "source.md").write_text("[HARMLESS MARKER](missing.txt)\n")
            leaf = self.root / "extra.md"
            leaf.symlink_to(external / "source.md")
            parent = self.root / "prompts"
            shutil.rmtree(parent)
            parent.symlink_to(external, target_is_directory=True)
            original_open, original_scandir = os.open, os.scandir

            def guarded_open(path, *args, **kwargs):
                candidate = Path(path)
                self.assertNotEqual(candidate, leaf, "source symlink was opened")
                self.assertNotIn(parent, candidate.parents, "linked parent was followed")
                return original_open(path, *args, **kwargs)

            def guarded_scandir(path):
                self.assertNotEqual(Path(path), parent, "linked directory was traversed")
                return original_scandir(path)

            with patch.object(os, "open", guarded_open), patch.object(os, "scandir", guarded_scandir):
                errors = validator.validate(self.root)["errors"]
            rejected = {e["path"] for e in errors if e["rule"] == "unsafe_source"}
            self.assertTrue({"extra.md", "prompts"} <= rejected)
            self.assertNotIn("broken_local_link", {e["rule"] for e in errors})

    @unittest.skipUnless(os.name == "posix", "synthetic local symlinks")
    def test_source_root_with_linked_ancestor_is_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            alias = Path(outside) / "alias"
            alias.symlink_to(self.root.parent, target_is_directory=True)
            with patch.object(os, "scandir", side_effect=AssertionError("unsafe root traversed")):
                result = validator.validate(alias / self.root.name)
            self.assertFalse(result["ok"])
            self.assertIn("unsafe_source", {e["rule"] for e in result["errors"]})

    def test_source_reparse_points_are_rejected_before_open_or_traversal(self):
        leaf = self.root / "extra.md"
        leaf.write_text("[HARMLESS MARKER](missing.txt)\n")
        directory = self.root / "prompts"
        original_lstat, original_open, original_scandir = Path.lstat, os.open, os.scandir

        def guarded_lstat(path):
            self.assertNotIn(directory, path.parents, "reparse directory metadata traversed")
            if path in (leaf, directory):
                mode = stat.S_IFDIR if path == directory else stat.S_IFREG
                return SimpleNamespace(st_mode=mode, st_file_attributes=stat.FILE_ATTRIBUTE_REPARSE_POINT)
            return original_lstat(path)

        def guarded_open(path, *args, **kwargs):
            self.assertNotEqual(Path(path), leaf, "reparse file opened")
            self.assertNotIn(directory, Path(path).parents, "reparse parent followed")
            return original_open(path, *args, **kwargs)

        def guarded_scandir(path):
            self.assertNotEqual(Path(path), directory, "reparse directory traversed")
            return original_scandir(path)

        with patch.object(Path, "lstat", guarded_lstat), patch.object(os, "open", guarded_open), \
                patch.object(os, "scandir", guarded_scandir):
            errors = validator.validate(self.root)["errors"]
        self.assertTrue({"extra.md", "prompts"} <=
                        {e["path"] for e in errors if e["rule"] == "unsafe_source"})

    @unittest.skipUnless(hasattr(os, "mkfifo"), "POSIX named pipes")
    def test_nonregular_markdown_is_rejected_without_opening(self):
        fifo = self.root / "pipe.md"
        os.mkfifo(fifo)
        run = subprocess.run([sys.executable, str(ROOT / "scripts/validate.py"),
                              "--root", str(self.root), "--json"],
                             capture_output=True, text=True, timeout=3)
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertIn({"path": "pipe.md", "rule": "unsafe_source"},
                      json.loads(run.stdout)["errors"])

    def test_source_descriptor_is_checked_and_closed_on_rejection(self):
        path = self.root / "extra.md"
        path.write_text("HARMLESS TEST CONTENT\n")
        metadata = path.stat()
        cases = (
            SimpleNamespace(st_mode=stat.S_IFREG,
                            st_file_attributes=stat.FILE_ATTRIBUTE_REPARSE_POINT),
            SimpleNamespace(st_mode=stat.S_IFIFO),
            SimpleNamespace(st_mode=stat.S_IFREG, st_dev=metadata.st_dev,
                            st_ino=metadata.st_ino + 1),
        )
        for result in cases:
            with self.subTest(metadata=result):
                with patch.object(os, "fstat", return_value=result) as probe:
                    with self.assertRaises(ValueError):
                        validator.read_markdown(path)
                fd = probe.call_args.args[0]
                with self.assertRaises(OSError):
                    os.fstat(fd)

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

    def test_unsafe_local_links_are_rejected_before_filesystem_probe(self):
        targets = (
            "%2F%2Fserver.invalid/share/file.md", "%2f%2fserver.invalid/share/file.md",
            "%5C%5Cserver.invalid%5Cshare%5Cfile.md", "/absolute.md", "%2Fabsolute.md",
            "C:/outside.md", "C:outside.md", "%43%3A%5Coutside.md", "%5Crooted.md",
            "../outside.md", "%2e%2e/outside.md", "folder/../../outside.md",
            "folder%2F..%2F..%2Foutside.md", "..%5Coutside.md", "folder%5C..%5Coutside.md",
            "..%20/outside.md", "folder/file:stream", "NUL", "folder/CON.txt",
            "conout$.txt", "ConIn$", "COM1", "lpt9.log", "COM%C2%B9.txt", "LPT%C2%B3",
            "NUL%20.txt", "name.", "name%20",
            "file%00.md", "file%0A.md", "%ff.md",
        )
        # Pure path parsing establishes the Windows interpretation without
        # instantiating a WindowsPath or contacting any network filesystem.
        self.assertTrue(PureWindowsPath("//server.invalid/share/file.md").is_absolute())
        original_lstat = Path.lstat
        for target in targets:
            with self.subTest(target=target):
                (self.root / "links.md").write_text(f"[docs]({target})\n")
                approved = {self.root, *self.root.parents, *self.root.rglob("*")}

                def guarded_lstat(path):
                    if path not in approved:
                        self.fail(f"unapproved filesystem probe intercepted: {path}")
                    return original_lstat(path)

                with patch.object(Path, "lstat", guarded_lstat):
                    errors = validator.validate(self.root)["errors"]
                self.assertEqual(errors, [{"path": "links.md", "rule": "unsafe_local_link",
                                           "detail": target}])

    def test_safe_relative_links_keep_encoded_filename_characters(self):
        docs = self.root / "docs"
        docs.mkdir()
        for name in ("a file(1).txt", "café.txt", "hash#question?.txt", "%2Fdouble.txt", "COM10.txt"):
            (self.root / name).write_text("harmless target", encoding="utf-8")
        (docs / "links.md").write_text(
            "[space](../a%20file(1).txt#section)\n"
            "[unicode](../caf%C3%A9.txt?view=1)\n"
            "[punctuation](../hash%23question%3F.txt)\n"
            "[once](../%252Fdouble.txt)\n[dir](../docs/)\n"
            "[inside](../docs/../a%20file(1).txt)\n"
            "[ordinary](../COM10.txt)\n"
        )
        self.assertTrue(validator.validate(self.root)["ok"])

    def test_nested_link_boundaries_and_nondirectory_parents(self):
        docs = self.root / "docs"
        docs.mkdir()
        (self.root / "target.txt").write_text("harmless target")
        (docs / "links.md").write_text(
            "[escape](../../outside.txt)\n"
            "[encoded](../%2e%2e/outside.txt)\n"
            "[file parent](../target.txt/../target.txt)\n"
        )
        errors = validator.validate(self.root)["errors"]
        self.assertEqual([e["rule"] for e in errors],
                         ["unsafe_local_link", "unsafe_local_link", "broken_local_link"])

    def test_unreadable_link_target_is_a_diagnostic(self):
        target = self.root / "target.txt"
        target.write_text("harmless target")
        (self.root / "links.md").write_text("[docs](target.txt)\n")
        original_lstat = Path.lstat

        def guarded_lstat(path):
            if path == target:
                raise PermissionError("synthetic denied metadata access")
            return original_lstat(path)

        with patch.object(Path, "lstat", guarded_lstat):
            errors = validator.validate(self.root)["errors"]
        self.assertEqual(errors, [{"path": "links.md", "rule": "unreadable_local_link",
                                   "detail": "target.txt"}])

    def test_external_links_never_probe_their_destinations(self):
        (self.root / "links.md").write_text(
            "[https](https://example.invalid/file)\n[network](//example.invalid/file)\n"
            "[encoded](%68ttps%3A//example.invalid/file)\n"
            "[mail](mailto:someone@example.invalid)\n[file](file:///outside.md)\n[anchor](#local)\n"
            "[external bytes](https://example.invalid/caf%E9)\n"
            "[network bytes](//example.invalid/caf%E9)\n"
            "[data bytes](data:application/octet-stream,%FF)\n"
            "[external controls](https://example.invalid/file%00%0A)\n"
        )
        approved = {self.root, *self.root.parents, *self.root.rglob("*")}
        original_lstat = Path.lstat

        def guarded_lstat(path):
            if path not in approved:
                self.fail(f"external destination probe intercepted: {path}")
            return original_lstat(path)

        with patch.object(Path, "lstat", guarded_lstat):
            self.assertTrue(validator.validate(self.root)["ok"])

    @unittest.skipUnless(os.name == "posix", "synthetic local symlink fixtures")
    def test_link_checks_do_not_follow_symlink_components(self):
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "target.txt"
            target.write_text("HARMLESS TEST TARGET")
            alias = self.root / "alias.txt"
            alias.symlink_to(target)
            directory = self.root / "alias-dir"
            directory.symlink_to(outside, target_is_directory=True)
            (self.root / "links.md").write_text(
                "[leaf](alias.txt)\n[parent](alias-dir/target.txt)\n"
                "[dot parent](alias-dir/../prompts/prism-scan.md)\n"
            )
            original_lstat = Path.lstat

            def guarded_lstat(path):
                if directory in path.parents:
                    self.fail(f"following symlink probe intercepted: {path}")
                return original_lstat(path)

            with patch.object(Path, "lstat", guarded_lstat):
                errors = validator.validate(self.root)["errors"]
            self.assertEqual([e["rule"] for e in errors if e["path"] == "links.md"],
                             ["unsafe_local_link"] * 3)

    def test_link_checks_reject_synthetic_windows_reparse_point(self):
        directory = self.root / "junction"
        directory.mkdir()
        (self.root / "links.md").write_text("[docs](junction/file.txt)\n")
        original_lstat = Path.lstat

        def guarded_lstat(path):
            if directory in path.parents:
                self.fail("reparse-point traversal intercepted")
            if path == directory:
                return SimpleNamespace(st_mode=stat.S_IFDIR | 0o755,
                                       st_file_attributes=stat.FILE_ATTRIBUTE_REPARSE_POINT)
            return original_lstat(path)

        with patch.object(Path, "lstat", guarded_lstat):
            errors = validator.validate(self.root)["errors"]
        self.assertEqual([e["rule"] for e in errors if e["path"] == "links.md"],
                         ["unsafe_local_link"])

    def test_target_mocks_support_direct_os_lstat_dispatch(self):
        # Simulate CPython 3.14's dispatch, without claiming a native 3.14 run.
        with patch.object(Path, "lstat", lambda path: os.lstat(path)):
            self.test_unreadable_link_target_is_a_diagnostic()
            self.test_link_checks_reject_synthetic_windows_reparse_point()

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
        for indent in ("    ", "\t", " \t", "  \t", "   \t"):
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
            for indent in ("    ", "\t", " \t", "  \t", "   \t"):
                with self.subTest(prefix=prefix, indent=indent):
                    (self.root / "links.md").write_text(prefix + indent + "[docs](missing.md)\n")
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
