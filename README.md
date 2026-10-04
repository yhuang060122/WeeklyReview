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
| `index.html` | 全站目录导航页。新增文档后，把对应卡片加入此处（按分类与时间排序） |
| `*.html` | 各周复盘看板与学习笔记，直接以相对链接互相跳转 |
| `.github/workflows/deploy.yml` | 部署工作流 |
| `.nojekyll` | 跳过 Jekyll 处理，按静态文件原样发布 |

## 维护约定

- 新文档入库：复制 HTML 到仓库根目录 → 在 `index.html` 对应分类下追加卡片 → 推送 `main` 即可生效。
