#!/usr/bin/env python3
"""Multi-provider OCR parser.

Providers:
  qwen       Alibaba DashScope Qwen-VL-OCR (sync, image → text)
  volcano    Volcano Engine Ark — Doubao vision model OCR (sync, image → text)
  unisound   Unisound (云知声) U1 OCR (async 4-step, PDF → markdown)

Usage:
  python ocr_parser.py <input>                          # default: --provider qwen
  python ocr_parser.py --provider volcano <input>
  python ocr_parser.py --provider unisound <input.pdf>  # input must be a PDF

Input can be a local file path or an http(s) URL. For qwen/volcano the input
should be an image; for unisound it should be a PDF.

Auth (auto-loaded from <skill_dir>/.env; see .env.example):
  qwen       → DASHSCOPE_API_KEY
  volcano    → VOLCANO_API_KEY
  unisound   → UNISOUND_API_KEY
  unisound   → UNISOUND_BASE_URL  (optional, default https://maas-api.hivoice.cn)
  unisound   → UNISOUND_MODEL     (optional, default u1-ocr)
"""
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

# ---------------------------------------------------------------------------
# .env loader (mirrors the vision skill's pattern)
# ---------------------------------------------------------------------------

def load_dotenv() -> None:
    """Load KEY=VALUE from <skill_dir>/.env into os.environ (never overrides)."""
    skill_dir = Path(__file__).resolve().parent.parent
    path = skill_dir / ".env"
    if not path.is_file():
        return
    try:
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = val
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Image → OpenAI-compatible image content
# ---------------------------------------------------------------------------

def to_image_content(image: str) -> dict:
    """Local path or http(s) URL → {"type":"image_url", "image_url":{"url":...}}."""
    if image.startswith("http://") or image.startswith("https://"):
        return {"type": "image_url", "image_url": {"url": image}}
    p = Path(image)
    if not p.is_file():
        sys.exit(f"error: image not found: {image}")
    mime = mimetypes.guess_type(p.name)[0] or "image/png"
    b64 = base64.b64encode(p.read_bytes()).decode("ascii")
    return {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}}


# ---------------------------------------------------------------------------
# HTTP helpers (stdlib only)
# ---------------------------------------------------------------------------

def _http_json(url: str, method: str, headers: dict, body: bytes | None = None,
               timeout: int = 60) -> dict:
    req = urllib.request.Request(url=url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        sys.exit(f"error: {method} {url} → HTTP {exc.code}: {detail[:400]}")


def _http_text(url: str, timeout: int = 60) -> str:
    req = urllib.request.Request(url=url, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8")


def _http_download(url: str, dest: Path, timeout: int = 60) -> bool:
    req = urllib.request.Request(url=url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            if not data:
                return False
            if not dest.suffix:
                ctype = resp.headers.get("Content-Type", "").split(";")[0].strip()
                dest = dest.with_suffix(mimetypes.guess_extension(ctype) or ".bin")
            dest.write_bytes(data)
            return True
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
        return False


# ===========================================================================
# Provider: Qwen (Alibaba Cloud DashScope) — sync image OCR
# ===========================================================================
#
# Model choice: DashScope exposes a specialized "qwen-vl-ocr" model, but it
# is invoked via DashScope's native multimodal API, not the OpenAI-compatible
# /chat/completions endpoint used here. Via /chat/completions, that model
# returns an empty content field.
#
# The working approach with the OpenAI-compatible endpoint is to use a
# general Qwen vision model (qwen-vl-plus or qwen-vl-max) and prompt it for
# OCR. Tested: qwen-vl-plus correctly identifies images with no text and
# extracts text from images that contain it. This is also exactly the
# pattern Volcano uses, so the providers stay symmetric.
#
# If you need the specialized OCR model, add a second function
# `qwen_ocr_native()` that calls DashScope's multimodal-generation API and
# register it under a different provider name (e.g. "qwen-ocr"). The
# PROVIDERS-dispatch pattern makes this a contained change.

QWEN_BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1"
QWEN_DEFAULT_MODEL = "qwen-vl-plus"
# Kept short on purpose: a very strict "only output the text, no explanation" instruction
# causes DashScope's OpenAI-compatible endpoint to return content=None for some
# responses. This prompt reliably returns either the recognized text or a short
# "no text" sentence.
QWEN_PROMPT = "请识别图片中所有可见的文字。如果图片中没有文字，请直接说「图片中没有文字」。"


def qwen_ocr(image: str, model: str = QWEN_DEFAULT_MODEL, api_key: str | None = None,
             base: str = QWEN_BASE) -> str:
    api_key = api_key or os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        sys.exit("error: DASHSCOPE_API_KEY is not set (see .env.example)")
    body = {
        "model": model,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": QWEN_PROMPT},
                to_image_content(image),
            ],
        }],
    }
    data = _http_json(
        f"{base.rstrip('/')}/chat/completions", "POST",
        {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json.dumps(body).encode("utf-8"), timeout=120,
    )
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        sys.exit(f"error: unexpected Qwen response: {json.dumps(data, ensure_ascii=False)[:400]}")
    # Some responses (especially with strict prompts) come back with content=None.
    # Treat that as "no text found" rather than crashing.
    return (content or "").strip() or "(no text returned by model)"


# ===========================================================================
# Provider: Volcano Engine Ark (火山方舟) — sync image OCR via a Doubao model
# ===========================================================================
#
# NOTE on model id: Volcano Ark doesn't currently (as of writing) expose a
# dedicated OCR model on the public model list — OCR is done by prompting a
# vision model. The default below is "doubao-1.5-vision-pro-32k", which
# supports image inputs and handles OCR well. If Ark publishes a dedicated
# OCR model, change the default here (or pass --model).
#
# If you hit "model not found" or want a cheaper alternative, the model list
# is at https://www.volcengine.com/docs/82379 — pick a vision-capable
# Doubao model and update VOLCANO_MODEL or pass --model.

VOLCANO_BASE = "https://ark.cn-beijing.volces.com/api/v3"
VOLCANO_DEFAULT_MODEL = "doubao-1.5-vision-pro-32k"
# Same shape as Qwen's prompt for consistency; see QWEN_PROMPT for why it's short.
VOLCANO_PROMPT = "请识别图片中所有可见的文字。如果图片中没有文字，请直接说「图片中没有文字」。"


def volcano_ocr(image: str, model: str = VOLCANO_DEFAULT_MODEL, api_key: str | None = None,
                base: str = VOLCANO_BASE) -> str:
    api_key = api_key or os.environ.get("VOLCANO_API_KEY")
    if not api_key:
        sys.exit("error: VOLCANO_API_KEY is not set (see .env.example)")
    body = {
        "model": model,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": VOLCANO_PROMPT},
                to_image_content(image),
            ],
        }],
    }
    data = _http_json(
        f"{base.rstrip('/')}/chat/completions", "POST",
        {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json.dumps(body).encode("utf-8"), timeout=120,
    )
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        sys.exit(f"error: unexpected Volcano response: {json.dumps(data, ensure_ascii=False)[:400]}")
    return (content or "").strip() or "(no text returned by model)"


# ===========================================================================
# Provider: Unisound (云知声) U1 OCR — async 4-step PDF → Markdown
# ===========================================================================
#
# Endpoint and protocol read from the original unisound-ocr-parser skill
# (scripts/convert_pdf.py). Workflow: upload → create task → poll → download.

UNISOUND_DEFAULT_BASE = "https://maas-api.hivoice.cn"
UNISOUND_DEFAULT_MODEL = "u1-ocr"
UNISOUND_POLL_INTERVAL = 3     # seconds
UNISOUND_TASK_TIMEOUT = 600    # max total wait
UNISOUND_UPLOAD_TIMEOUT = 180  # max for file upload

# Match ![alt](url) in markdown
_IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def _detect_status(resp: dict) -> str:
    for candidate in (
        resp.get("status"),
        (resp.get("task") or {}).get("status"),
        (resp.get("data") or {}).get("status"),
    ):
        if candidate:
            return str(candidate).lower()
    return "unknown"


def _build_multipart(file_path: Path, purpose: str) -> tuple[bytes, str]:
    boundary = f"----OCRParser{uuid.uuid4().hex}"
    mime = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    parts: list[bytes] = [
        f"--{boundary}\r\n".encode(),
        f'Content-Disposition: form-data; name="purpose"\r\n\r\n'.encode(),
        purpose.encode("utf-8"),
        b"\r\n",
        f"--{boundary}\r\n".encode(),
        f'Content-Disposition: form-data; name="file"; filename="{file_path.name}"\r\n'
        f"Content-Type: {mime}\r\n\r\n".encode(),
        file_path.read_bytes(),
        b"\r\n",
        f"--{boundary}--\r\n".encode(),
    ]
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


def unisound_ocr(pdf_path: str, api_key: str | None = None, base: str | None = None,
                 model: str | None = None, images_dir: str = "",
                 log=print) -> str:
    api_key = api_key or os.environ.get("UNISOUND_API_KEY")
    if not api_key:
        sys.exit("error: UNISOUND_API_KEY is not set (see .env.example)")
    base = (base or os.environ.get("UNISOUND_BASE_URL", UNISOUND_DEFAULT_BASE)).rstrip("/")
    if base.endswith("/v1"):
        base = base[:-3]
    model = model or os.environ.get("UNISOUND_MODEL", UNISOUND_DEFAULT_MODEL)

    p = Path(pdf_path)
    if not p.is_file():
        sys.exit(f"error: PDF not found: {pdf_path}")
    size_mb = p.stat().st_size / (1024 * 1024)
    if p.stat().st_size > 100 * 1024 * 1024:
        sys.exit(f"error: PDF is {size_mb:.1f} MB, exceeds 100 MB limit")

    headers_auth = {"Authorization": f"Bearer {api_key}"}
    log(f"[1/4] Uploading {p.name} ({size_mb:.1f} MB)…")

    body, ctype = _build_multipart(p, "ocr_async_input")
    resp = _http_json(
        f"{base}/v1/files/upload", "POST",
        {**headers_auth, "Content-Type": ctype}, body, timeout=UNISOUND_UPLOAD_TIMEOUT,
    )
    file_id = (resp.get("file") or {}).get("file_id")
    if not file_id:
        sys.exit(f"error: no file_id in upload response: {json.dumps(resp, ensure_ascii=False)[:300]}")
    log(f"  file_id: {file_id}")

    log("[2/4] Creating parser task…")
    payload = json.dumps({"file_id": file_id, "model": model}).encode("utf-8")
    resp = _http_json(
        f"{base}/v1/files/parser/tasks", "POST",
        {**headers_auth, "Content-Type": "application/json"}, payload, timeout=60,
    )
    task_id = (resp.get("task_id") or resp.get("id")
               or (resp.get("task") or {}).get("task_id"))
    if not task_id:
        sys.exit(f"error: no task_id in create response: {json.dumps(resp, ensure_ascii=False)[:300]}")
    log(f"  task_id: {task_id}")

    log("[3/4] Polling for completion…")
    deadline = time.time() + UNISOUND_TASK_TIMEOUT
    last: dict = {}
    idx = 0
    while time.time() < deadline:
        last = _http_json(
            f"{base}/v1/files/parser/tasks/{urllib.parse.quote(str(task_id))}",
            "GET", headers_auth, timeout=30,
        )
        status = _detect_status(last)
        idx += 1
        if status in {"success", "succeeded", "completed", "done", "finished"}:
            log(f"  done (poll {idx})")
            break
        if status in {"failed", "error", "cancelled", "canceled"}:
            sys.exit(f"error: task failed ({status}): {json.dumps(last, ensure_ascii=False)[:300]}")
        if idx % 10 == 1:
            log(f"  poll {idx}: {status}…")
        time.sleep(UNISOUND_POLL_INTERVAL)
    else:
        sys.exit(f"error: polling timed out after {UNISOUND_TASK_TIMEOUT}s")

    md_url = last.get("md_file_url")
    if not md_url:
        sys.exit(f"error: task done but no md_file_url: {json.dumps(last, ensure_ascii=False)[:300]}")
    log("[4/4] Downloading Markdown…")
    markdown = _http_text(md_url, timeout=180)
    if not markdown.strip():
        sys.exit("error: empty Markdown returned")
    log(f"  {len(markdown)} chars")

    if images_dir:
        markdown = extract_local_images(markdown, Path(images_dir).resolve(), log=log)
        log(f"  images: {images_dir}")
    return markdown


def extract_local_images(markdown: str, images_dir: Path, log=print) -> str:
    """Download remote image URLs found in markdown to images_dir, rewrite refs."""
    matches = list(_IMG_RE.finditer(markdown))
    if not matches:
        return markdown
    images_dir.mkdir(parents=True, exist_ok=True)
    log(f"  found {len(matches)} image references")
    url_to_local: dict[str, str] = {}
    for idx, m in enumerate(matches, 1):
        url = m.group(2)
        if not (url.startswith("http://") or url.startswith("https://")):
            continue
        if url in url_to_local:
            continue
        parsed = urllib.parse.urlparse(url)
        name = os.path.basename(parsed.path) or f"img_{idx}"
        if "." not in name:
            name = f"img_{idx}"
        dest = images_dir / name
        if dest.exists():
            dest = images_dir / f"{dest.stem}_{idx}{dest.suffix}"
        if _http_download(url, dest):
            rel = os.path.relpath(dest, start=Path.cwd()).replace(os.sep, "/")
            url_to_local[url] = rel
            log(f"  [{idx}/{len(matches)}] {name}")
        else:
            log(f"  [{idx}/{len(matches)}] FAILED: {url}")
    if not url_to_local:
        return markdown
    return _IMG_RE.sub(lambda m: f"![{m.group(1)}]({url_to_local.get(m.group(2), m.group(2))})", markdown)


# ---------------------------------------------------------------------------
# Provider dispatch
# ---------------------------------------------------------------------------

PROVIDERS = {
    "qwen": {
        "fn":      qwen_ocr,
        "env":     "DASHSCOPE_API_KEY",
        "input":   "image",
        "default": QWEN_DEFAULT_MODEL,
    },
    "volcano": {
        "fn":      volcano_ocr,
        "env":     "VOLCANO_API_KEY",
        "input":   "image",
        "default": VOLCANO_DEFAULT_MODEL,
    },
    "unisound": {
        "fn":      unisound_ocr,
        "env":     "UNISOUND_API_KEY",
        "input":   "pdf",
        "default": UNISOUND_DEFAULT_MODEL,
    },
}


def main() -> None:
    load_dotenv()

    p = argparse.ArgumentParser(
        description="Multi-provider OCR (Qwen / Volcano Ark / Unisound U1).",
    )
    p.add_argument("input", help="Image path/URL (qwen, volcano) or PDF path (unisound)")
    p.add_argument("--provider", "-p", default="qwen", choices=sorted(PROVIDERS),
                   help="OCR provider (default: qwen)")
    p.add_argument("--model", "-m", default="",
                   help="Override the provider's default model")
    p.add_argument("--key", default="",
                   help="Override the provider's API key (else from env)")
    p.add_argument("--base", default="",
                   help="Override the API base URL (qwen/volcano/unisound)")
    p.add_argument("--images-dir", default="",
                   help="[unisound only] download embedded images here and rewrite Markdown")
    p.add_argument("-o", "--output", default="",
                   help="Write result to this file (default: stdout)")
    p.add_argument("--quiet", "-q", action="store_true",
                   help="Suppress progress logs (e.g. unisound polling)")
    args = p.parse_args()

    prov = PROVIDERS[args.provider]
    log = (lambda *a, **kw: None) if args.quiet else print

    fn = prov["fn"]
    model = args.model or prov["default"]
    # Each provider function has its own defaults. Pass a kwarg ONLY if the
    # user provided a non-empty value — otherwise let the function use its
    # own default. (Passing None would override string defaults and crash
    # inside f-strings like f"{base.rstrip('/')}/...".)
    import inspect
    sig = inspect.signature(fn)
    kwargs: dict = {}
    if "model" in sig.parameters and model:          kwargs["model"] = model
    if "api_key" in sig.parameters and args.key:    kwargs["api_key"] = args.key
    if "base" in sig.parameters and args.base:      kwargs["base"] = args.base
    if "images_dir" in sig.parameters and args.images_dir:
        kwargs["images_dir"] = args.images_dir
    if "log" in sig.parameters:                     kwargs["log"] = log

    try:
        result = fn(args.input, **kwargs)
    except SystemExit:
        raise
    except Exception as exc:
        sys.exit(f"error: {exc}")

    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
        if not args.quiet:
            print(f"Saved: {args.output} ({len(result)} chars)", file=sys.stderr)
    else:
        sys.stdout.write(result)
        if not result.endswith("\n"):
            sys.stdout.write("\n")


if __name__ == "__main__":
    main()
