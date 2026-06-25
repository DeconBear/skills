---
name: ocr-parser
description: This skill should be used when the user wants to perform OCR (extract text from images or PDFs) and wants the agent to invoke a provider-agnostic OCR tool. Supports three providers — Alibaba DashScope Qwen-VL-OCR, Volcano Engine Ark (火山方舟) Doubao vision OCR, and Unisound (云知声) U1 OCR — via a single CLI (run scripts/ocr_parser.py with --provider qwen, --provider volcano, or --provider unisound). Use when the user says "OCR this image", "把 PDF 转成文字 / Markdown", "识别图片中的文字", "extract text from this PDF", or explicitly invokes one of the supported providers.
---

# OCR Parser (multi-provider)

Extract text from images and PDFs via a single CLI that dispatches to one of three providers. Each provider is a small, isolated function in `scripts/ocr_parser.py` so a new provider (or a model-name update) is a one-file change.

## When to use

- The user gives an image (path or URL) or a PDF and asks for the text inside.
- The user mentions one of: Qwen / 通义 / DashScope, Volcano / 火山 / Doubao, Unisound / 云知声 / U1.
- A workflow step needs OCR as a sub-task and the agent should pick the right provider.

Do **not** use for handwritten signature verification, layout analysis beyond plain text, or languages the chosen model doesn't support.

## Providers at a glance

| Provider   | Input | Workflow     | Output | Best for                          |
|------------|-------|--------------|--------|-----------------------------------|
| `qwen`     | image | sync         | text   | default; best CJK recognition     |
| `volcano`  | image | sync         | text   | alternative to Qwen on Volcano    |
| `unisound` | PDF   | async 4-step | markdown | native PDF parsing with layout |

## Quick start

```bash
# Default: Qwen on a local image
python scripts/ocr_parser.py ./receipt.png

# Volcano on an image URL
python scripts/ocr_parser.py --provider volcano "https://example.com/page.png"

# Unisound on a PDF (async — takes a minute for big files)
python scripts/ocr_parser.py --provider unisound ./paper.pdf -o paper.md

# Override the model or key for one call
python scripts/ocr_parser.py --provider qwen --model qwen-vl-ocr-latest --key sk-... ./img.jpg
```

## Configuration (API keys)

This skill follows the repo-wide rule: **no real keys in the source repo**. The script auto-loads from `<skill_dir>/.env` (the installed location, e.g. `~/.claude/skills/ocr-parser/.env`). For the full key-handling convention, see the top-level `CLAUDE.md` (local to this checkout, not committed).

Quick setup:

```bash
# In the INSTALLED skill folder, not the source repo:
cp ocr-parser/.env.example ~/.claude/skills/ocr-parser/.env
# Edit ~/.claude/skills/ocr-parser/.env and fill in the keys you have.
```

You only need to fill the keys for the providers you'll actually use. Missing keys produce a clear `error: DASHSCOPE_API_KEY is not set` at call time.

## Workflow

1. Pick the provider. Default is `qwen`. Pick `unisound` if the input is a PDF; pick `volcano` if the user is on Volcano Ark and wants that provider specifically.
2. Run `python scripts/ocr_parser.py --provider <name> <input>`. The script validates the input exists, loads `.env`, and dispatches.
3. If the call fails with an authentication error, surface the env-var name (e.g. `VOLCANO_API_KEY`) so the user knows which key to set.
4. If the result is empty or garbled, try a different provider or a different model id — see `references/providers.md` for how to override.

## Extending the providers

To add a new provider or update a model id, edit `scripts/ocr_parser.py`:
- Add a `<name>_ocr(...)` function (follow the existing pattern).
- Add an entry to the `PROVIDERS` dict.
- Add the API key to `.env.example`.
- Document it in `references/providers.md`.

Because each provider is a standalone function, a user can ask Claude Code to "add a new OCR provider that calls <X> with model <Y>" and the change is mechanical.
