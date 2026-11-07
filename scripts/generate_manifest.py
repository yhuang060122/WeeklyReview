#!/usr/bin/env python3
"""生成 index.html 动态目录所需的 manifest.json。

在 GitHub Actions 构建时运行：递归扫描站点目录（public/）下的 *.html，
按「所在文件夹」分类，提取 <title>，输出 [{path, title, category, tag, label}]。
index.html 通过 JavaScript 读取本文件动态渲染目录，无需手工维护。

目录即分类：
    guide/             -> 使用指南（置顶）
    weekly/            -> 周复盘（文件名以日期开头，倒序排列）
    notes/<主题>/      -> 学习笔记（主题目录决定标签）
其余散落在根目录的 HTML 兜底归入笔记。
"""
import html
import json
import os
import re
import sys

CAT_GUIDE = "guide"
CAT_WEEKLY = "weekly"
CAT_NOTE = "note"

# notes/ 下的主题目录 -> 展示标签
TOPIC_TAGS = {
    "ai": "AI",
    "frontend": "前端",
    "csharp": "C#",
    "math": "数学",
    "observability": "可观测性",
    "engineering": "开发",
}

# 笔记分组展示顺序（未列出的排最后）
TOPIC_ORDER = ["ai", "frontend", "csharp", "math", "observability", "engineering"]

DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")


def title_of(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read(200_000)
    m = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
    if not m:
        return os.path.splitext(os.path.basename(path))[0]
    return html.unescape(m.group(1).strip())


def label_of(base: str) -> str:
    """从文件名开头的日期生成展示区间：2026-10-26_2026-11-01 -> '2026-10-26 → 2026-11-01'."""
    dates = DATE_RE.findall(base)
    if len(dates) >= 2:
        first = "-".join(dates[0])
        second = "-".join(dates[1])
        return f"{first} → {second}"
    if dates:
        return "-".join(dates[0])
    return ""


def classify(rel: str):
    """按文件夹返回 (category, tag, label)。"""
    parts = rel.replace("\\", "/").split("/")
    top = parts[0] if len(parts) > 1 else ""
    base = os.path.splitext(parts[-1])[0]

    if top == "guide":
        return CAT_GUIDE, "使用指南", ""
    if top == "weekly":
        label = label_of(base)
        return CAT_WEEKLY, ("周复盘" if label else "常驻模块"), label
    if top == "notes":
        topic = parts[1] if len(parts) > 2 else ""
        return CAT_NOTE, TOPIC_TAGS.get(topic, "笔记"), ""
    return CAT_NOTE, "笔记", ""


def date_key(entry: dict) -> str:
    dates = DATE_RE.findall(entry["path"])
    return "-".join(dates[0]) if dates else "0000-00-00"


def topic_key(entry: dict) -> int:
    parts = entry["path"].split("/")
    topic = parts[1] if len(parts) > 2 and parts[0] == "notes" else ""
    return TOPIC_ORDER.index(topic) if topic in TOPIC_ORDER else len(TOPIC_ORDER)


def main() -> None:
    root = sys.argv[1] if len(sys.argv) > 1 else "public"
    entries = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        for filename in sorted(filenames):
            if not filename.lower().endswith(".html"):
                continue
            if filename.lower() == "index.html":
                continue
            path = os.path.join(dirpath, filename)
            rel = os.path.relpath(path, root).replace("\\", "/")
            category, tag, label = classify(rel)
            entries.append({
                "path": rel,
                "title": title_of(path),
                "category": category,
                "tag": tag,
                "label": label,
            })

    # 使用指南置顶；周复盘按日期倒序（常驻模块排最后）；笔记按主题分组、组内按路径
    guide = sorted((e for e in entries if e["category"] == CAT_GUIDE),
                   key=lambda e: e["path"])
    weekly = sorted((e for e in entries if e["category"] == CAT_WEEKLY),
                    key=lambda e: (date_key(e), e["path"]), reverse=True)
    notes = sorted((e for e in entries if e["category"] == CAT_NOTE),
                   key=lambda e: (topic_key(e), e["path"]))

    os.makedirs(root, exist_ok=True)
    with open(os.path.join(root, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(guide + weekly + notes, f, ensure_ascii=False, indent=2)
    print(f"manifest.json: {len(entries)} files -> {root}")


if __name__ == "__main__":
    main()
