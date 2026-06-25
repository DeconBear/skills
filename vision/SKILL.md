---
name: vision
description: Give the text-only model the ability to "see" images by delegating to the Qwen-VL multimodal model. Use when the user references an image, screenshot, photo, diagram, or asks what's in / about a picture, and you (a text-only model) cannot actually view it. Delegates vision to Qwen-VL and returns text you can reason over.
---

# Vision (multimodal proxy)

You are a **text-only** model: you cannot actually see images. This skill lets you
offload vision to a multimodal model (Qwen-VL) and get back **text** you can reason about.

Whenever an image is involved, **never guess or pretend to see it**. Call the script below
to obtain real information first.

## When to use

- The user gives an image path / URL / screenshot and asks anything about it.
- The user says "看这张图 / 图里有什么 / 这张图是不是…" or similar.
- You need OCR, layout, color, counting, or any visual detail from an image.
- A task references a figure/diagram you'd otherwise have to assume.

Do **not** use it for images you can already see natively (if your runtime injected the image
into your context as a real image block, just answer directly).

## How to call

Run the script from this skill's `scripts/` folder via your shell tool.
`<image>` is whatever you have: a local file path or an `http(s)` URL — the script auto-detects.

```bash
# 1. One-shot description (optionally focus on an aspect)
python scripts/vision.py describe <image>                 # full description
python scripts/vision.py describe <image> --focus 文字     # focus: text / 颜色 / 局部 / 布局 …

# 2. Ask a specific question about the image
python scripts/vision.py ask <image> "图中的红色按钮上写了什么？"
```

> On Windows the shell is PowerShell; quote the question with double quotes.

## How to use the results

1. **Describe first, then ask.** When the task is open-ended, start with `describe` to get the
   lay of the land. Only follow up with targeted `ask` calls for specifics you're unsure about.
2. **Cap follow-ups.** Limit yourself to ~2–3 `ask` rounds per image. If you still lack
   information, tell the user what's missing rather than looping.
3. **Quote faithfully.** Treat the returned text as ground truth about the image. Don't
   embellish or contradict it. If it says "uncertain" / "无法判断", relay that.
4. **Attribute.** When your answer depends on the vision call, it's fine to just answer —
   but if the user might doubt a visual claim, mention the detail came from the image.
5. **Pass concrete questions.** "图里有什么" is weak; "左下角的表格第三列的数值是多少" is strong
   and gets a better answer.

## Example flow

User: "帮我看看 ./screenshot.png 里报错信息是什么意思"

```bash
python scripts/vision.py ask ./screenshot.png "图中的报错信息文字是什么？逐字输出。"
# → 报错原文
python scripts/vision.py ask ./screenshot.png "根据报错，最可能的原因是什么？"
# → 推断
```
Then answer the user based on the returned text.

## Configuration

The script reads `DASHSCOPE_API_KEY` from the first place it finds it (existing env vars
always win over file values):

1. **Process environment** — Windows User/System env vars, or `export` in your shell.
2. **`./.env`** in the current working directory — project-local override (useful for testing). Wins over the skill's .env.
3. **`<skill_dir>/.env`** — the installed skill's own folder, e.g. `~/.claude/skills/vision/.env`. **Recommended** for your real key, because it's scoped to the skill and lives outside any repo.

A template is committed as `vision/.env.example`. Copy it to the installed location and fill
in your key:

```bash
# Recommended — one .env per installed skill:
cp vision/.env.example ~/.claude/skills/vision/.env
# Then edit ~/.claude/skills/vision/.env and replace the placeholder with your real key.
```

> **Never commit a real `.env` file.** The repo's `.gitignore` already excludes `.env` and
> allows only `.env.example` to be tracked.

## Requirements

- `DASHSCOPE_API_KEY` available via the methods above (Qwen-VL / DashScope).
- Python 3.7+ (stdlib only — no pip install needed).
- Optional: override model with `VISION_MODEL` (default `qwen-vl-max`).

If the API key is missing or a call fails, the script prints `error: ...` to stderr and exits
non-zero — surface that to the user instead of guessing the image.
