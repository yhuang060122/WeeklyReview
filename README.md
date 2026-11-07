# WeeklyReview

每周复盘看板与学习笔记的静态站点，推送后由 GitHub Actions 自动部署到 GitHub Pages。

## 访问地址

`https://yhuang060122.github.io/WeeklyReview/`

## 部署机制

- 推送（或合并）到 `main` 分支后，`.github/workflows/deploy.yml` 自动构建并部署；也可在仓库 Actions 页面手动触发（workflow_dispatch）。
- 工作流把站点内容（`index.html`、`favicon.*`、`.nojekyll` 及 `guide/`、`weekly/`、`notes/` 目录树）整体同步进 `public/`，`.git`、`.github`、`scripts` 不会进入站点。

### 首次启用（只需一次）

仓库 **Settings → Pages → Source** 选择 **GitHub Actions**，保存后即可自动部署。

## 内容结构

```
.
├── index.html              目录导航页（站点入口，唯一放在根目录的页面）
├── favicon.png / .ico      站点图标（秋日枫叶）
├── guide/                  使用与维护指南
│   └── handoff.html
├── weekly/                 周复盘看板（文件名以日期开头，按日期倒序展示）
│   ├── 2026-09-14_2026-09-20.html
│   ├── 2026-10-05_2026-10-11-multi-asset.html
│   ├── 2026-11-06-mag7.html
│   └── module-ai-financial-verification.html   常驻模块
├── notes/                  学习笔记，按四类子目录归档
│   ├── ai/                 Transformer / Attention / LLM
│   ├── frontend/           Angular / JS / 前端架构
│   ├── backend/            C# / TPL Dataflow / 可观测性
│   └── other/              数学 / 工程与职业
├── scripts/generate_manifest.py   构建时扫描 HTML、提取 <title>、生成 manifest.json
└── .github/workflows/deploy.yml   部署工作流
```

`manifest.json` 由 CI 在 `public/` 中生成，不提交入库。

## 命名约定

| 类型 | 位置与格式 | 示例 |
| --- | --- | --- |
| 周复盘看板 | `weekly/YYYY-MM-DD_YYYY-MM-DD.html` | `weekly/2026-10-26_2026-11-01.html` |
| 周复盘变体 | 在日期后缀语义：`-multi-asset`、`-global-cross-asset` | `weekly/2026-10-05_2026-10-11-multi-asset.html` |
| 单日周报 | `weekly/YYYY-MM-DD-<主题>.html` | `weekly/2026-11-06-mag7.html` |
| 周复盘常驻模块 | `weekly/module-<主题>.html` | `weekly/module-ai-financial-verification.html` |
| 学习笔记 | `notes/<子类>/<kebab-case 名称>.html` | `notes/frontend/angular-http-resource.html` |
| 站点指南 | `guide/handoff.html` | `guide/handoff.html` |

一律使用英文小写 kebab-case 文件名（不含空格、中文、导出时间戳）。页面上展示的标题取自 HTML 的 `<title>`，因此文件名只承担 URL 与排序职责。

分类与标签由 `scripts/generate_manifest.py` 按**所在文件夹**判定：`guide/` → 使用指南，`weekly/` → 周复盘，`notes/<子类>/` → 四个子类标签（AI / 前端 / 后端 / 其他）。

## 维护约定

- **新增文档**：放进对应目录（`weekly/` 或 `notes/<子类>/`）→ push `main` → 工作流自动提取标题、重建 manifest，目录页即时更新，无需改 `index.html`。
- **笔记子类固定为四个**：`notes/ai/`、`notes/frontend/`、`notes/backend/`、`notes/other/`。要调整子类，需同时改目录与 `scripts/generate_manifest.py` 的 `TOPIC_TAGS` / `TOPIC_ORDER`。
- **分类规则调整**：编辑 `scripts/generate_manifest.py` 中的 `classify()`。
- **本地预览**：`python3 -m http.server 8000` 后访问 `http://localhost:8000/`（`manifest.json` 需先执行 `python3 scripts/generate_manifest.py .` 生成；直接双击 HTML 时浏览器会拦截 `fetch`）。
