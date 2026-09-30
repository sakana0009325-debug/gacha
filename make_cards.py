#!/usr/bin/env python3
"""videos フォルダの mp4 を読み取って cards.js を作る。

ファイル名のルール: s3_名前.mp4 / s4_名前.mp4 / s5_名前.mp4
ルールに合わないファイルは無視して、一覧を表示する。
"""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parent
folder = root / "videos"
pattern = re.compile(r"^s[345]_.+\.mp4$", re.IGNORECASE)

files, skipped = [], []
if folder.is_dir():
    for p in sorted(folder.iterdir()):
        if p.suffix.lower() != ".mp4":
            continue
        (files if pattern.match(p.name) else skipped).append(p.name)

body = ",\n".join("  " + json.dumps(f, ensure_ascii=False) for f in files)
(root / "cards.js").write_text(
    "// このファイルは make_cards.py が videos フォルダから自動で作ります。手で編集しなくてOK。\n"
    "window.GACHA_CARDS = [\n" + body + ("\n" if body else "") + "];\n",
    encoding="utf-8",
)

print(f"カード {len(files)} 枚を cards.js に書き出しました")
for level in "543":
    print(f"  ★{level}: {sum(1 for f in files if f[1] == level)} 枚")
for name in skipped:
    print(f"  ※名前のルールに合わないため除外: {name}")
