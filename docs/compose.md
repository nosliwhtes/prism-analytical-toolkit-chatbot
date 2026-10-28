# Create an offline review bundle

The optional helper combines a complete Prism prompt and named local text files into one paste/upload bundle. Python 3.12 or newer is required for the supported maintenance environment; no packages, credentials, model access, or installation are needed. Run commands from the repository root. For direct copy/paste without Python, use the [quickstart](../quickstart.md).

For local UTF-8 text files, an optional Python helper creates one paste/upload bundle containing the **complete selected prompt**, numbered source lines, and SHA-256 hashes of original source bytes:

```sh
python3 scripts/compose.py --prompt full --artifact proposal.md --artifact requirements.md --context review-context.txt --focus "handoff correctness" --output review-bundle.md
```

Repeat `--artifact` in citation order. `--prompt` accepts `scan` (default), `full`, `3way`, `reflect`, or `discover`. Discovery bundles request only domains, without citations or findings. The other four modes request citations to numbered source lines. Omit `--prompt` for Scan, `--context`/`--focus` when unnecessary, and `--output` to print to stdout. Run `python3 scripts/compose.py --help` for options. The helper only reads the named sources and the selected local prompt; it makes no network/model calls, executes no source code, and refuses to overwrite an existing output. It rejects symlinks in selected prompt, artifact and context paths (including parent directories), non-regular files, missing, empty, non-UTF-8, and NUL-containing inputs. Its default combined artifact/context limit is 200,000 bytes, adjustable with `--max-bytes`; oversize inputs fail without truncation. This is **not** a model token/context limit: select smaller excerpts for your chatbot and record omitted parts. PDF, office documents, URLs, and images need text extraction or the chatbot's own upload support.

Secure source reads require POSIX no-follow flags and directory-descriptor support (tested on Linux); unsupported systems fail with an error rather than follow links. Use real, non-symlink source paths. `--output` requires a filesystem supporting hard links: the helper writes and syncs a private staging file in the destination directory, then atomically creates the destination without replacement. Encoding, write, or close failures leave no incomplete destination and handled failures remove the staging file, so a corrected command can retry. Abrupt process termination may leave a private `.prism-bundle-*.tmp` staging file. The direct Markdown copy/paste workflow remains available on all platforms.

Hashes identify bytes, not truth, authority, or document dates. The numbered display normalizes CRLF/CR to LF and omits the final line separator; metadata records original ending counts and whether a final newline was present. This is a readable review copy, not a lossless file export; use original files for byte-sensitive questions. The bundle labels unknown versions as unspecified; supply known versions in context. Review the generated bundle before sharing it: it contains the source text. Both output paths validate UTF-8 before writing, and stdout emits UTF-8 bytes regardless of the terminal encoding. Use `--output` rather than shell redirection when you need overwrite protection. Keep private bundles outside this public repository; `review-bundle*.md` and abandoned `.prism-bundle-*.tmp` staging files are ignored as a convenience.

## Display and provenance

The review copy makes C0/C1 terminal controls (except tabs and line endings), DEL, and Unicode bidirectional controls visible as literal `\uNNNN` escapes, with a replacement count per affected source. Original-byte hashes, byte counts and line numbers are unchanged. Ordinary Unicode text remains readable. Escape spellings may also occur literally in the input; this display is not an unambiguous serialization. Consult the original for character-sensitive analysis. This protects the source display; it does not sanitize the selected protocol or user-supplied command arguments.

## Troubleshooting

| Message or situation | Next step |
| --- | --- |
| Byte limit exceeded | Choose smaller excerpts, recording omissions, or raise `--max-bytes` deliberately. Nothing is truncated. |
| Source must be UTF-8 / contains NUL / is empty | Export readable UTF-8 text; do not rename a PDF or office file to `.txt`. |
| Too many levels of symbolic links / Not a directory | Use actual paths without symlink components. This applies to the selected prompt as well as artifact and context files. |
| Not a regular file | Name an ordinary text file, not a directory, device, or pipe. |
| File exists | Choose a new output name. Existing files, directories and symlinks are preserved. |
| Secure source reads unsupported / hard links unsupported | Use direct Markdown copy/paste, or a local POSIX filesystem with the documented capabilities. |
| Chatbot cannot read the attachment | Paste the complete prompt and a smaller labeled excerpt; an upload does not prove the content was read. |

An input failure exits with status 2 before producing a bundle or staging file. A handled output failure removes its staging file; existing destinations stay intact. An error after publication may leave a complete bundle, so inspect the destination before retrying. Filesystem support and permissions still apply.
