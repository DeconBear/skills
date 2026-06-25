# @deconbear/get-skill

> A one-liner installer for the [DeconBear/skills](https://github.com/DeconBear/skills)
> collection of Claude Code skills.

```bash
npx @deconbear/get-skill ocr-parser
npx @deconbear/get-skill vision
npx @deconbear/get-skill premium-ui-gallery
```

Each command downloads the corresponding skill's latest release zip from
GitHub and extracts it into `~/.claude/skills/<skill>/`. After the install
the script tells you the exact `cp .env.example .env` command to run for
skills that need an API key.

## Usage

```
npx @deconbear/get-skill <skill> [--dest PATH] [--version VER]

Skills:
  - premium-ui-gallery
  - vision
  - ocr-parser

Options:
  --dest PATH      extract to this directory
                   (default: ~/.claude/skills/<skill>)
  --version VER    release version tag (default: v0.1.0)
  --list           list known skills and exit
  -h, --help       show this help
```

## Examples

```bash
# Default: install ocr-parser to ~/.claude/skills/ocr-parser
npx @deconbear/get-skill ocr-parser

# Install to a custom path
npx @deconbear/get-skill vision --dest ./my-skill

# Pin to a specific release
npx @deconbear/get-skill premium-ui-gallery --version v0.1.0

# List available skills
npx @deconbear/get-skill --list
```

## How it works

1. Resolves `<skill>` to a GitHub release tag (`<skill>-<version>`).
2. Downloads the zip from
   `https://github.com/DeconBear/skills/releases/download/<tag>/<skill>.zip`
   (follows the 302 to `objects.githubusercontent.com`).
3. Extracts the zip into `--dest` (default `~/.claude/skills/<skill>`).
4. If the skill ships a `.env.example` and no `.env` exists yet, prints
   the exact `cp` command to set up credentials.

No config files, no global state, no telemetry. The only runtime
dependency is [adm-zip](https://www.npmjs.com/package/adm-zip) for
cross-platform zip extraction.

## Requirements

- Node.js ≥ 18 (for `npx`).
- Network access to `github.com` and `objects.githubusercontent.com`.
- On the target filesystem: write permission to the install directory
  (default: `~/.claude/skills/`).

## License

[MIT](https://github.com/DeconBear/skills/blob/main/LICENSE) © 2026 DeconBear.

## Repository

https://github.com/DeconBear/skills
