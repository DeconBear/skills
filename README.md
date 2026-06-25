# skills

[English](README.md) · [中文](README-zh.md)

---

A small collection of [Claude Code](https://claude.ai/code) skills. Each skill gives
Claude specialized instructions plus, optionally, executable helpers, reference material,
and ready-to-use assets. Developed here in source, then copied into
`~/.claude/skills/` so they load in every session.

## Skills in this repo

| Skill | What it does | One-line use |
|---|---|---|
| [`premium-ui-gallery`](./premium-ui-gallery/SKILL.md) | Reference catalog of 10 design-inspiration galleries (landing.love, mobbin, hugeicons, etc.) + a 10-section design checklist + 6 ready-to-use 2D/3D motion templates. | "Build a premium landing page inspired by these galleries." |
| [`vision`](./vision/SKILL.md) | Gives a text-only model the ability to "see" images by delegating to Qwen-VL (DashScope). | "Describe what's in this screenshot." / "Read the error text in this image." |
| [`ocr-parser`](./ocr-parser/SKILL.md) | Multi-provider OCR. One CLI dispatches to Qwen (DashScope), Volcano Ark (Doubao vision), or Unisound U1 — image-to-text or PDF-to-markdown. | "OCR this image." / "Convert this PDF to Markdown." |

Each `SKILL.md` is the entry point: it tells Claude *when* to use the skill and *how* to
call its helpers. The skill-creator convention is
[documented upstream](https://github.com/anthropics/skills); this repo follows it.

## Install

The fastest path — one command, downloads the skill straight from the
matching GitHub release and extracts it to `~/.claude/skills/<skill>/`:

```bash
npx @decon/get-skill ocr-parser      # or: vision, premium-ui-gallery
```

The `[@decon/get-skill](packages/get-skill/)` wrapper is a tiny (~100 lines, one
runtime dep) CLI that lives in this repo under `packages/get-skill/`. It:

- downloads the `<skill>-<version>` release zip from GitHub (following the 302 to
  `objects.githubusercontent.com`),
- extracts it into `~/.claude/skills/<skill>/` (or `--dest` if you want it elsewhere),
- and if the skill ships a `.env.example` and no `.env` yet, prints the exact
  `cp` + edit command to run next.

It also works for pinning: `npx @decon/get-skill ocr-parser --version v0.2.0`
once a future release exists.

### Alternative install methods

If you'd rather not use Node, or you're working from this repo's source:

```bash
# Release zip — curl + unzip, no npm (works on any *nix and on Windows with Git Bash)
SKILL=ocr-parser
curl -L -o "/tmp/$SKILL.zip" \
  "https://github.com/DeconBear/skills/releases/download/$SKILL-v0.1.0/$SKILL.zip"
unzip "/tmp/$SKILL.zip" -d "$HOME/.claude/skills/$SKILL"

# Clone just the subdirectory — degit, no git history (needs Node)
npx degit DeconBear/skills/ocr-parser "$HOME/.claude/skills/ocr-parser"

# From this repo's source — for development
cp -r ./ocr-parser/. "$HOME/.claude/skills/ocr-parser/"
```

After any install, fill the API key in `~/.claude/skills/<skill>/.env` (see
[Configuration](#configuration--the-one-strict-rule)) for any skill that needs one.
Each skill's `.env.example` shows the variables you can set; only the ones for
providers you actually use are required.

## Configuration — the one strict rule

**Real API keys and secrets never live in this repository.** This is non-negotiable
for an open-source repo and the rule has a single, simple shape:

| Where | What goes there |
|---|---|
| `<skill>/.env.example` (in source) | A template with placeholder values and explanatory comments. **Committed.** |
| `~/.claude/skills/<skill>/.env` (after install) | Your real keys. **Gitignored, outside any repo.** |

Every script in this repo auto-loads its installed `.env` at call time. The reference
implementation is [`vision/scripts/vision.py → load_dotenv()`](./vision/scripts/vision.py);
the `ocr-parser` script uses the same pattern.

**Quick setup** (example for the `ocr-parser` skill):

```bash
# Copy the template into the INSTALLED location (NOT the source repo)
cp ocr-parser/.env.example ~/.claude/skills/ocr-parser/.env

# Edit it and fill in the keys you have
$EDITOR ~/.claude/skills/ocr-parser/.env
```

You only need to fill in the keys for the providers you'll actually use. Missing keys
produce a clear `error: <KEY_NAME> is not set` at call time, so it's obvious which
env var to set.

The repo's [`.gitignore`](./.gitignore) excludes `.env` everywhere and explicitly
allows only `.env.example` to be tracked. The pre-commit safety check is:

```bash
git diff --cached --name-only | grep -E '(^|/)\.env$' | grep -v '\.env\.example$' && echo "ERROR" || echo "safe"
```

## Extending a provider with AI assistance

Several skills in this repo talk to third-party APIs (DashScope, Volcano Ark, Unisound,
HugeIcons, etc.). These APIs change — models get renamed, endpoints move, response
shapes evolve. To make updates cheap, each provider is implemented as a small, isolated
function with its configuration in a single dict at the top of the file.

The intended workflow when a provider breaks or you want to add one:

1. **Open an issue** describing the problem (paste the error, the model id, what you tried).
2. **Or — ask Claude Code (or any AI coding tool) to fix it.** Give it the file and the
   error, and the change is usually a one-liner: a model id, an endpoint URL, a header.
   Example prompts that work well:
   - *"The Volcano provider in `ocr-parser/scripts/ocr_parser.py` returns 404. Look up
     the current Doubao vision models on https://www.volcengine.com/docs/82379 and
     pick one that supports image inputs, then update the default and the doc."*
   - *"The Qwen provider is using `qwen-vl-ocr` but that model now requires the
     DashScope native multimodal API, not the OpenAI-compatible one. Add a second
     function `qwen_ocr_native()` that calls the native endpoint, and register it as a
     separate provider called `qwen-ocr`."*
3. **Or — send a PR.** The maintainers will review and merge.

Because each provider is a standalone function with its own `load_dotenv()`-managed key,
adding a fourth OCR provider is a ~50-line change: a new function, a new entry in the
`PROVIDERS` dict, a new env var in `.env.example`, a paragraph in the reference doc.

## Repository layout

```
.
├── <skill-name>/         # one directory per skill
│   ├── SKILL.md          # required
│   ├── references/       # optional
│   ├── scripts/          # optional
│   └── assets/           # optional
├── demo/                 # gitignored: outputs produced BY skills
├── dist/                 # gitignored: packaged skill zips
├── .claude/              # project-level Claude Code settings
├── .gitignore
├── CLAUDE.md             # local-only guidance for Claude Code (not tracked)
└── README.md
```

## Contributing

Issues and pull requests are welcome. A few notes:

- **Don't commit `.env` files.** The CI check (and the pre-commit one-liner above) will
  reject the commit. Rotate the key first, then rewrite history.
- **Keep the key-handling rule intact.** If you add a new skill that needs credentials,
  follow the `.env.example` (source) + `.env` (install) pattern and add a `load_dotenv()`
  to the script. The vision skill is the reference.
- **One provider per function, dispatched from a single `PROVIDERS` dict.** This is the
  pattern that makes extensions a one-line change.
- **Update `references/` when you change behavior.** The reference docs are what an AI
  coding tool will read to fix the next breakage, so make them current.

If you're unsure how to structure a new skill, the
[skill-creator](https://github.com/anthropics/skills/tree/main/skill-creator) reference
in the upstream skills repo walks through the process.

## License

[MIT](./LICENSE) © 2026 DeconBear.
