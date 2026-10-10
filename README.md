# WeeklyReview

每周复盘看板与学习笔记的静态站点，推送后由 GitHub Actions 自动部署到 GitHub Pages。

## 访问地址

`https://yhuang060122.github.io/WeeklyReview/`

## 部署机制

- 推送（或合并）到 `main` 分支后，`.github/workflows/deploy.yml` 自动构建并部署；也可在仓库 Actions 页面手动触发（workflow_dispatch）。
- 工作流只把仓库根目录的 `*.html` 与 `.nojekyll` 打包成 Pages 产物，`.git`、`.github` 不会进入站点。

### 首次启用（只需一次）

仓库 **Settings → Pages → Source** 选择 **GitHub Actions**，保存后即可自动部署。

## 内容结构

| 文件 | 说明 |
| --- | --- |
| `index.html` | 目录导航页。通过 JavaScript 读取构建时生成的 `manifest.json` 动态渲染，无需手工维护 |
| `handoff.html` | 站点使用与维护指南，置顶展示于目录「📖 使用指南」 |
| `*.html` | 各周复盘看板与学习笔记，直接以相对链接互相跳转 |
| `scripts/generate_manifest.py` | 在 CI 中扫描 HTML、提取 `<title>`、分类排序并生成 `manifest.json` |
| `.github/workflows/deploy.yml` | 部署工作流（打包站点 + 生成 manifest） |
| `.nojekyll` | 跳过 Jekyll 处理，按静态文件原样发布 |

## 命名约定

| 类型 | 格式 | 示例 |
| --- | --- | --- |
| 周复盘看板 | `周复盘看板_YYYYMMDD-YYYYMMDD.html` | `周复盘看板_20260928-20261004.html` |
| 周复盘常驻模块 | `周复盘模块_<主题>.html` | `周复盘模块_AI财务验证追踪.html` |
| 学习笔记 | `<主题>.html`（不带导出时间戳） | `渐进式实现Promise-六步演进的设计思路.html` |
| 站点指南 | `handoff.html` | `handoff.html` |

分类、标签与排序由 `scripts/generate_manifest.py` 依据命名约定自动判定（含 C# / 前端 / AI / 可观测性 / 开发 / 数学等关键词）。

## 维护约定

- **新增文档**：按命名约定放入仓库根目录 → push `main` → 工作流自动提取标题、重建 manifest，目录页即时更新，无需改 `index.html`。
- **分类规则调整**：编辑 `scripts/generate_manifest.py` 中的 `classify()` 即可。
