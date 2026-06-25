# skills

[English](README.md) · [中文](README-zh.md)

---

一个 [Claude Code](https://claude.ai/code) skill 集合。每个 skill 给 Claude 专门的指令,以及(可选的)可执行辅助、参考材料和即用型资源。在源码中开发,然后复制到 `~/.claude/skills/` 让它在每个会话里都能加载。

## 仓库中的 skills

| Skill | 作用 | 一句话用法 |
|---|---|---|
| [`premium-ui-gallery`](./premium-ui-gallery/SKILL.md) | 10 个设计灵感画廊的参考目录(landing.love、mobbin、hugeicons 等)+ 一份 10 节设计自检清单 + 6 个即用型 2D/3D 动效模板。| "参考这些画廊做一个高端落地页。" |
| [`vision`](./vision/SKILL.md) | 通过委托 Qwen-VL(DashScope)给纯文本模型"看图"的能力。| "描述一下这张截图里的内容。" / "读出这张图里的报错文字。" |
| [`ocr-parser`](./ocr-parser/SKILL.md) | 多提供商 OCR。一个 CLI 分发到 Qwen(DashScope)、火山方舟(Doubao 视觉模型)、或云知声(图像→文本 或 PDF→Markdown)。| "OCR 这张图。" / "把这个 PDF 转成 Markdown。" |

每个 `SKILL.md` 是入口:它告诉 Claude *何时*使用这个 skill 以及*如何*调用它的辅助。skill-creator 的约定在[上游文档](https://github.com/anthropics/skills)里有详细说明;本仓库遵循它。

## 安装

把一个 skill 放到 `~/.claude/skills/` 有三种方式,选适合你的:

**1. 从本仓库(开发安装):**

```bash
cp -r ./<skill-name>/. "$HOME/.claude/skills/<skill-name>/"
```

**2. 从 GitHub,不下载 git 历史(推荐给终端用户 —— 需要 Node):**

```bash
# npx degit 克隆子目录但不带 .git 文件夹
npx degit DeconBear/skills/<skill-name> "$HOME/.claude/skills/<skill-name>"
```

**3. 从 GitHub Release 下载 zip(不需要 Node —— 任何装了 curl + unzip 的机器都行):**

```bash
SKILL=<skill-name>
curl -L -o "/tmp/$SKILL.zip" \
  "https://github.com/DeconBear/skills/releases/download/$SKILL-v0.1.0/$SKILL.zip"
unzip "/tmp/$SKILL.zip" -d "$HOME/.claude/skills/$SKILL"
```

任何一种方式装好后,在 `~/.claude/skills/<skill>/.env` 里填入你有的 key(见下面的
[配置](#配置--唯一硬规则))。每个 skill 的 `.env.example` 列出了可用的环境变量,
只需要填你实际要用到的提供商对应的那些。

> 想要 `npx @decon/get-skill <name>` 这种一行命令的精致 npx 体验?那需要发一个
> 小的 npm 包 —— 可以做,见 `references/install-options.md`(或开 issue)。

## 配置 — 唯一硬规则

**真实的 API key 和其他密钥永远不进这个仓库。** 对一个开源仓库来说这是不可妥协的,规则只有一种简单形态:

| 位置 | 放什么 |
|---|---|
| `<skill>/.env.example`(源码里) | 带占位符值和说明注释的模板。**已提交。** |
| `~/.claude/skills/<skill>/.env`(安装后) | 你的真实 key。**已 gitignore,在仓库外。** |

仓库里的每个脚本在调用时自动加载它所在安装位置的 `.env`。参考实现是 [`vision/scripts/vision.py → load_dotenv()`](./vision/scripts/vision.py);`ocr-parser` 用同样的模式。

**快速设置**(以 `ocr-parser` 为例):

```bash
# 把模板复制到安装位置(不是源码仓库)
cp ocr-parser/.env.example ~/.claude/skills/ocr-parser/.env

# 编辑它,填入你有的 key
$EDITOR ~/.claude/skills/ocr-parser/.env
```

你只需要填入你实际会用的那些提供商的 key。缺失的 key 在调用时会产生清晰的 `error: <KEY_NAME> is not set`,所以很明显要设哪个环境变量。

仓库的 [`.gitignore`](./.gitignore) 在所有位置排除 `.env`,并明确允许只有 `.env.example` 被跟踪。提交前的安全检查:

```bash
git diff --cached --name-only | grep -E '(^|/)\.env$' | grep -v '\.env\.example$' && echo "ERROR" || echo "safe"
```

## 用 AI 辅助扩展提供商

仓库里的几个 skill 会调用第三方 API(DashScope、火山方舟、云知声、HugeIcons 等)。这些 API 会变——模型改名、端点迁移、响应结构演化。为了让更新成本最低,每个提供商都实现为一个独立的小函数,它的配置集中在文件顶部的一个 dict 里。

提供商坏掉或你想加一个时,推荐的工作流:

1. **开一个 issue** 描述问题(贴出错误、model id、你试过的方法)。
2. **或者——让 Claude Code(或任何 AI 编程工具)帮你修。** 把文件和错误交给它,改动通常是一行:一个 model id、一个端点 URL、一个 header。效果好的示例 prompt:
   - *"ocr-parser/scripts/ocr_parser.py 里的 Volcano 提供商返回 404。去 https://www.volcengine.com/docs/82379 查最新的 Doubao 视觉模型,选一个支持图像输入的,然后更新默认值和文档。"*
   - *"Qwen 提供商现在用的是 qwen-vl-ocr,但这个模型需要 DashScope 原生 multimodal API,不是 OpenAI-compatible。再加一个函数 qwen_ocr_native() 来调用原生端点,并把它注册成独立的提供商 qwen-ocr。"*
3. **或者——发个 PR。** 维护者会 review 和 merge。

因为每个提供商都是独立函数、自己用 `load_dotenv()` 管理 key,加第四个 OCR 提供商是大约 50 行的改动:一个新函数、`PROVIDERS` dict 里一个新条目、`.env.example` 里一个新环境变量、参考文档里新加一段。

## 仓库结构

```
.
├── <skill-name>/         # 每个 skill 一个目录
│   ├── SKILL.md          # 必需
│   ├── references/       # 可选
│   ├── scripts/          # 可选
│   └── assets/           # 可选
├── demo/                 # gitignored: skill 产出的输出
├── dist/                 # gitignored: 打包好的 skill zip
├── .claude/              # 项目级 Claude Code 设置
├── .gitignore
├── CLAUDE.md             # 本地的 Claude Code 指引(不跟踪)
└── README.md             # 英文(主入口) · README-zh.md (中文)
```

## 贡献

欢迎 issue 和 pull request。几点注意:

- **不要提交 `.env` 文件。** CI 检查(以及上面的 pre-commit 一行)会拒绝这个提交。先 rotate key,再改写历史。
- **保持 key 处理规则不变。** 如果你加的新 skill 需要凭证,遵循 `.env.example`(源码)+ `.env`(安装)模式,并在脚本里加一个 `load_dotenv()`。vision skill 是参考。
- **一个提供商一个函数,从单个 `PROVIDERS` dict 分发。** 这是让扩展变成一行改动的模式。
- **改行为时同步更新 `references/`。** 参考文档是 AI 编程工具会读来修下一次破损的东西的,所以保持更新。

不确定怎么组织一个新 skill,上游 [skill-creator](https://github.com/anthropics/skills/tree/main/skill-creator) 参考里有完整的流程。

## 许可证

[MIT](./LICENSE) © 2026 DeconBear。
