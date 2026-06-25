# vision skill

让纯文本模型获得"看图"能力：把视觉任务委托给多模态模型 Qwen-VL，拿回文字后再推理。

## 工作原理

文本模型本身不看图，而是通过本 skill 提供的脚本调用 Qwen-VL：

- `describe` → 一次性获取图片文字描述
- `ask` → 针对图片提问（VQA）

详见 `SKILL.md`。

## 安装

把 `vision/` 目录放到你的 skills 目录（Claude Code 用 `~/.claude/skills/`，Codex 用对应 skills 路径）。
脚本仅用 Python 标准库，无需 `pip install`。

## 配置 API Key

在环境中设置 DashScope 的 key：

```powershell
# PowerShell（当前会话）
$env:DASHSCOPE_API_KEY = "sk-xxxxxx"

# 持久化（用户级）
[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "sk-xxxxxx", "User")
```

获取地址：https://dashscope.console.aliyun.com/

可选环境变量：

- `VISION_MODEL`：覆盖默认模型 `qwen-vl-max`（如改为 `qwen-vl-plus` 省钱）。
- `VISION_API_BASE`：覆盖 API 基址，默认 `https://dashscope.aliyuncs.com/compatible-mode/v1`（OpenAI 兼容）。

## 用法（手动验证）

```bash
python scripts/vision.py describe ./test.png
python scripts/vision.py describe ./test.png --focus 文字
python scripts/vision.py ask ./test.png "图中有几个人？"
python scripts/vision.py ask https://example.com/photo.jpg "这张图拍摄于什么场景？"
```

## 文件结构

```
vision/
  SKILL.md            # 文本模型的调用指令
  scripts/vision.py   # Qwen-VL 封装，自动识别本地路径 / URL
  README.md
```
