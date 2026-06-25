# Provider reference

One section per supported OCR provider. The script's defaults are at the top of each section — override per call with `--model`, `--base`, or `--key`.

## Quick verification commands

After updating this file (or the script), verify with:

```bash
# Help and provider list
python scripts/ocr_parser.py --help

# Missing-key path (clear error)
unset DASHSCOPE_API_KEY VOLCANO_API_KEY UNISOUND_API_KEY
python scripts/ocr_parser.py ./img.png 2>&1 | head -1   # expect: error: DASHSCOPE_API_KEY is not set
```

---

## qwen — Alibaba Cloud DashScope (sync image → text)

- **API style**: OpenAI-compatible chat completions.
- **Endpoint**: `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`
- **Auth**: `Authorization: Bearer $DASHSCOPE_API_KEY`
- **Input**: image — local file (any browser-readable format) or `http(s)://` URL. Sent as a base64 data URI or URL inside a `image_url` content part.
- **Default model**: `qwen-vl-plus`
- **Env vars**: `DASHSCOPE_API_KEY`
- **Override**: `--model <id>`, `--key <key>`, `--base <url>`

### Model notes — read this before changing the default

DashScope exposes a specialized **`qwen-vl-ocr`** model. It is **not** callable through the
OpenAI-compatible `/chat/completions` endpoint used by this script — when invoked there it
returns 200 OK with an empty `content` field. The dedicated OCR model is invoked through
DashScope's **native multimodal-generation API** (a different endpoint and request shape).

With the OpenAI-compatible endpoint, the working approach is to use a **general Qwen
vision model** and prompt it for OCR. This script defaults to `qwen-vl-plus`, which:

- returns clean OCR text for images that contain text,
- correctly answers "no text in the image" for images that don't,
- has the same `image_url` request shape as Volcano, keeping the providers symmetric.

`qwen-vl-max` is a higher-accuracy (and more expensive) alternative — pass `--model qwen-vl-max`
per call. The full DashScope model list is at
<https://help.aliyun.com/zh/model-studio/getting-started/models>.

### If you specifically need the specialized `qwen-vl-ocr` model

Add a second function `qwen_ocr_native()` to `scripts/ocr_parser.py` that calls
DashScope's multimodal-generation API (see the DashScope docs for the exact request shape)
and register it as a separate provider entry, e.g. `"qwen-ocr"`. The dispatch loop will
route to it automatically. This keeps the two Qwen entry points cleanly separated.

### Request shape (what the script sends)

```json
{
  "model": "qwen-vl-ocr",
  "messages": [{
    "role": "user",
    "content": [
      {"type": "text", "text": "<OCR prompt, see QWEN_PROMPT>"},
      {"type": "image_url", "image_url": {"url": "data:image/png;base64,..." | "https://..."}}
    ]
  }]
}
```

### Response shape

The recognized text is at `choices[0].message.content`.

---

## volcano — Volcano Engine Ark / 火山方舟 (sync image → text)

- **API style**: OpenAI-compatible chat completions.
- **Endpoint**: `https://ark.cn-beijing.volces.com/api/v3/chat/completions`
- **Auth**: `Authorization: Bearer $VOLCANO_API_KEY`
- **Input**: image — local file or `http(s)://` URL. Same `image_url` content shape as Qwen.
- **Default model**: `doubao-1.5-vision-pro-32k`
- **Env vars**: `VOLCANO_API_KEY`
- **Override**: `--model <id>`, `--key <key>`, `--base <url>`

### Model notes

> **Heads-up — please verify the model id before relying on this provider.**
> Volcano Ark's public model list ([docs/82379](https://www.volcengine.com/docs/82379)) evolves
> frequently, and there is no widely-advertised dedicated OCR model on Ark at time of writing.
> The default `doubao-1.5-vision-pro-32k` is a Doubao **vision** model that handles OCR well
> when prompted. If Ark publishes a dedicated OCR model, change `VOLCANO_DEFAULT_MODEL` in
> `scripts/ocr_parser.py`, or override per call with `--model`.

The script's structure is designed so this is a one-line change.

### Request / response shape

Identical to Qwen: chat completions with `image_url` content. Recognized text at
`choices[0].message.content`.

---

## unisound — Unisound (云知声) U1 OCR (async 4-step PDF → markdown)

The most involved provider — it parses documents asynchronously. Implementation is ported
verbatim from the original `unisound-ocr-parser` skill's `scripts/convert_pdf.py`.

- **Endpoint base**: `https://maas-api.hivoice.cn` (override with `UNISOUND_BASE_URL` or `--base`)
- **Auth**: `Authorization: Bearer $UNISOUND_API_KEY`
- **Input**: **PDF only** (≤100 MB).
- **Default model**: `u1-ocr` (override with `UNISOUND_MODEL` or `--model`)
- **Output**: **Markdown** with embedded image URLs.
- **Env vars**: `UNISOUND_API_KEY`, `UNISOUND_BASE_URL` (optional), `UNISOUND_MODEL` (optional)

### Workflow

```
[1/4] POST {base}/v1/files/upload           multipart: purpose=ocr_async_input, file=<pdf>
                                            → file_id

[2/4] POST {base}/v1/files/parser/tasks     JSON: {file_id, model}
                                            → task_id

[3/4] GET  {base}/v1/files/parser/tasks/{task_id}   every 3s, until status is one of
                                                    success / succeeded / completed /
                                                    done / finished  (max 600s)

[4/4] GET  {task.md_file_url}                → Markdown text
```

### Optional: download embedded images

```bash
python scripts/ocr_parser.py --provider unisound --images-dir ./imgs paper.pdf -o paper.md
```

This walks the resulting markdown, downloads any `http(s)://…` image URLs to `--images-dir`,
and rewrites the markdown to reference the local files. Skipped silently if no remote image
URLs are present.

### Limitations

- PDF only. For images, use `qwen` or `volcano`.
- Hard 100 MB cap on the input PDF.
- Async; for very large or many documents, expect several minutes per file.

---

## Adding a new provider

The `PROVIDERS` dict in `scripts/ocr_parser.py` is the single source of truth. To add
`newprovider`:

1. Write a `newprovider_ocr(input, model=..., api_key=..., base=...)` function following the
   existing pattern (use `to_image_content` for image inputs, `_http_json` / `_http_text`
   for HTTP, `sys.exit("error: ...")` for failures).
2. Add an entry to `PROVIDERS`:
   ```python
   "newprovider": {
       "fn":      newprovider_ocr,
       "env":     "NEWPROVIDER_API_KEY",
       "input":   "image",  # or "pdf"
       "default": "<model-id>",
   },
   ```
3. Add the env var to `.env.example`.
4. Document it in this file.

That's the whole integration. The dispatch loop in `main()` introspects the function's
signature with `inspect.signature`, so only matching kwargs are passed.
