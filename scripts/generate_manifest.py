#!/usr/bin/env python3
"""生成 index.html 动态目录所需的 manifest.json。

在 GitHub Actions 构建时运行：扫描仓库根目录的 *.html，
提取 <title>，并按命名约定分类 / 打标签 / 排序列出。
index.html 通过 JavaScript 读取本文件动态渲染目录，无需手工维护。
"""
import glob
import html
import json
import os
import re
import sys

CAT_GUIDE = "guide"
CAT_WEEKLY = "weekly"
CAT_NOTE = "note"


def title_of(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read(200_000)
    m = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
    if not m:
        return os.path.splitext(os.path.basename(path))[0]
    return html.unescape(m.group(1).strip())


def fmt_ymd(d: str) -> str:
    return f"{d[:4]}-{d[4:6]}-{d[6:]}"


def classify(name: str):
    """按命名约定返回 (category, tag, label)。

    handoff.html                       -> guide / 使用指南 / 无日期（置顶）
    周复盘看板_YYYYMMDD-YYYYMMDD.html -> weekly / 周复盘 / 日期区间
    周复盘模块_<主题>.html            -> weekly / 常驻模块 / 无日期
    其余 *.html                       -> note  / 按关键词打标签
    """
    base = os.path.splitext(name)[0]
    if name == "handoff.html":
        return CAT_GUIDE, "使用指南", ""
    if "周复盘" in name:
        dates = re.findall(r"(\d{8})", name)
        if len(dates) >= 2:
            return CAT_WEEKLY, "周复盘", f"{fmt_ymd(dates[0])} → {fmt_ymd(dates[1])}"
        return CAT_WEEKLY, "常驻模块", ""
    if "数学" in base:
        return CAT_NOTE, "数学", ""
    if re.search(r"c#|csharp", base, re.I):
        return CAT_NOTE, "C#", ""
    if re.search(r"前端|js|javascript|webpack|模块化|promise", base, re.I):
        return CAT_NOTE, "前端", ""
    if re.search(r"llm|大模型|gemini", base, re.I):
        return CAT_NOTE, "AI", ""
    if re.search(r"correlation|trace", base, re.I):
        return CAT_NOTE, "可观测性", ""
    if re.search(r"软件|开发", base):
        return CAT_NOTE, "开发", ""
    return CAT_NOTE, "笔记", ""


def date_key(entry: dict) -> str:
    dates = re.findall(r"(\d{8})", entry["name"])
    return dates[0] if dates else "00000000"


def main() -> None:
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "public"
    entries = []
    for path in sorted(glob.glob("*.html")):
        name = os.path.basename(path)
        if name.lower() == "index.html":
            continue
        category, tag, label = classify(name)
        entries.append({
            "name": name,
            "title": title_of(path),
            "category": category,
            "tag": tag,
            "label": label,
        })

    # 使用指南置顶；周复盘按日期倒序（常驻模块排最后）；学习笔记按文件名排序
    guide = [e for e in entries if e["category"] == CAT_GUIDE]
    weekly = sorted((e for e in entries if e["category"] == CAT_WEEKLY),
                    key=date_key, reverse=True)
    notes = sorted((e for e in entries if e["category"] == CAT_NOTE),
                   key=lambda e: e["name"])

    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(guide + weekly + notes, f, ensure_ascii=False, indent=2)
    print(f"manifest.json: {len(entries)} files -> {out_dir}")


if __name__ == "__main__":
    main()
