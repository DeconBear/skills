#!/usr/bin/env python3
"""Vision proxy for text-only models via Qwen-VL (DashScope).

Subcommands:
  describe <image> [--focus ASPECT]   one-shot text description of the image
  ask <image> "<question>"            answer a question about the image

<image> may be a local file path or an http(s) URL. Local files are read,
base64-encoded and sent as a data URI; URLs are forwarded as-is.

Auth: set DASHSCOPE_API_KEY in the environment, OR place it in a .env file
the script will auto-load (see load_dotenv() below). Existing env vars
take precedence over .env values.
Override model with VISION_MODEL (default: qwen-vl-max).
"""
import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.request
import urllib.error

# Force UTF-8 stdout/stderr so non-GBK characters (e.g. \xa0, CJK) don't crash
# print() on Windows consoles.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

DEFAULT_API_BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1"
DEFAULT_MODEL = "qwen-vl-max"


def load_dotenv():
    """Load KEY=VALUE pairs from .env files into os.environ.

    Does NOT override existing environment variables — the process env always wins,
    so this is purely a fallback for users who prefer a file over registry/shell vars.

    Lookup order (all files are read; per-key, first-set wins via `os.environ` check):
      1. ./.env  in the current working directory (project-local override)
      2. ~/.claude/.env  (global Claude Code config — recommended for your real key)
    """
    candidates = [
        os.path.join(os.getcwd(), ".env"),
        os.path.expanduser("~/.claude/.env"),
    ]
    for path in candidates:
        if not os.path.isfile(path):
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                for raw in f:
                    line = raw.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, _, val = line.partition("=")
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key and key not in os.environ:
                        os.environ[key] = val
        except OSError:
            # unreadable .env — silently skip, don't break the script
            pass


# Auto-load on import. Safe to call multiple times (idempotent).
load_dotenv()


def api_url():
    base = os.environ.get("VISION_API_BASE", DEFAULT_API_BASE).rstrip("/")
    return f"{base}/chat/completions"


def resolve_image(image: str) -> str:
    """Return a URL or data URI the API can consume."""
    if image.startswith("http://") or image.startswith("https://"):
        return image
    if not os.path.isfile(image):
        sys.exit(f"error: image not found: {image}")
    mime, _ = mimetypes.guess_type(image)
    mime = mime or "image/png"
    with open(image, "rb") as f:
        data = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{data}"


def call_vision(image_ref: str, prompt: str, model: str) -> str:
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        sys.exit("error: DASHSCOPE_API_KEY is not set in the environment")

    body = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_ref}},
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    }
    req = urllib.request.Request(
        api_url(),
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        sys.exit(f"error: API returned {e.code}: {detail}")
    except urllib.error.URLError as e:
        sys.exit(f"error: network failure: {e.reason}")

    try:
        return payload["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError):
        sys.exit(f"error: unexpected API response: {json.dumps(payload, ensure_ascii=False)}")


def cmd_describe(args):
    prompt = "请详细、客观地描述这张图片的内容。"
    if args.focus:
        prompt += f" 重点关注：{args.focus}。"
    print(call_vision(resolve_image(args.image), prompt, args.model))


def cmd_ask(args):
    if not args.question:
        sys.exit("error: a question is required for 'ask'")
    print(call_vision(resolve_image(args.image), args.question, args.model))


def main():
    parser = argparse.ArgumentParser(description="Vision proxy via Qwen-VL.")
    parser.add_argument("--model", default=os.environ.get("VISION_MODEL", DEFAULT_MODEL),
                        help=f"Qwen-VL model id (default: {DEFAULT_MODEL})")
    sub = parser.add_subparsers(dest="command", required=True)

    p_desc = sub.add_parser("describe", help="one-shot description of the image")
    p_desc.add_argument("image", help="local path or http(s) URL")
    p_desc.add_argument("--focus", help="aspect to focus on (e.g. 文字 / 颜色 / 局部)")
    p_desc.set_defaults(func=cmd_describe)

    p_ask = sub.add_parser("ask", help="answer a question about the image")
    p_ask.add_argument("image", help="local path or http(s) URL")
    p_ask.add_argument("question", help="question to ask about the image")
    p_ask.set_defaults(func=cmd_ask)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
