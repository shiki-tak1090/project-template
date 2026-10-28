# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""ひな型のプレースホルダーを、プロジェクトの値に置き換える。

置き換えるのは決まったトークンだけで、表の行のように対話で埋める {{コードリポジトリの行}} などは残す。
99_テンプレート/ の {{機能名}} などは文書を作るときに埋めるものなので、対象外にする。
README.md などにある「ひな型の案内」の囲み（ひな型の段階でだけ表示するもの）は、ここで取り除く。

  uv run apply_project.py --slug acme --name "ACME 会員アプリ" --github-owner acme-inc \
      --backlog-key ACME --admin "山田" [--dry-run]
  uv run apply_project.py --check   # 置き換え後に残っているプレースホルダーを一覧する
"""
from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

ROOT = Path.cwd()
SKIP_DIRS = {".git", ".obsidian", "99_テンプレート", "project-new"}
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".txt", ""}
SLUG = re.compile(r"^[a-z][a-z0-9_-]{1,30}$")
PLACEHOLDER = re.compile(r"\{\{[^{}]+\}\}|xxxxx|YOUR_GITHUB_OWNER|<!-- ひな型の案内")
TEMPLATE_NOTICE = re.compile(r"<!-- ひな型の案内: ここから.*?<!-- ひな型の案内: ここまで -->\r?\n", re.S)


def targets() -> list[Path]:
    return [p for p in sorted(ROOT.rglob("*"))
            if p.is_file() and p.suffix in TEXT_SUFFIXES
            and not SKIP_DIRS & set(p.relative_to(ROOT).parts)
            and p.name != "TEMPLATE.md"]  # ひな型の説明。/project-new の最後に削除する


def leftovers() -> list[tuple[Path, int, str]]:
    found = []
    for p in targets():
        for no, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            for m in PLACEHOLDER.finditer(line):
                found.append((p.relative_to(ROOT), no, m.group(0)))
    return found


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug", help="案件名（英小文字で始まり、英小文字・数字・_・- のみ）")
    ap.add_argument("--name", help="プロジェクトの表示名")
    ap.add_argument("--github-owner", help="GitHub のユーザー名または組織名")
    ap.add_argument("--backlog-key", help="Backlog のプロジェクトキー（英大文字）")
    ap.add_argument("--admin", help="アクセス権の依頼先")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if not args.check:
        missing = [k for k in ("slug", "name", "github_owner", "backlog_key", "admin") if not getattr(args, k)]
        if missing:
            sys.exit(f"引数が足りません: {', '.join('--' + m.replace('_', '-') for m in missing)}")
        if not SLUG.match(args.slug):
            sys.exit(f"案件名 {args.slug!r} は使えません。英小文字で始まり、英小文字・数字・_・- だけにしてください。")
        if not re.fullmatch(r"[A-Z][A-Z0-9_]*", args.backlog_key):
            sys.exit(f"Backlog のプロジェクトキー {args.backlog_key!r} は英大文字・数字・_ にしてください。")
        replacements = {
            "xxxxx": args.slug,
            "{{プロジェクト名}}": args.name,
            "{{GitHubのオーナー}}": args.github_owner,
            "{{Backlogのプロジェクトキー}}": args.backlog_key,
            "{{管理者}}": args.admin,
            "{{作成日}}": args.date,
        }
        changed = 0
        for p in targets():
            text = p.read_text(encoding="utf-8")
            new = TEMPLATE_NOTICE.sub("", text)
            for old, value in replacements.items():
                new = new.replace(old, value)
            if new != text:
                changed += 1
                print(f"{'[dry-run] ' if args.dry_run else ''}置換: {p.relative_to(ROOT)}")
                if not args.dry_run:
                    p.write_text(new, encoding="utf-8", newline="\n")
        print(f"{changed} ファイルを{'置き換えます（dry-run のため未変更）' if args.dry_run else '置き換えました'}。")
        if args.dry_run:
            return

    rest = leftovers()
    if rest:
        print("\n残っているプレースホルダー（対話で埋めるもの）:")
        for path, no, token in rest:
            print(f"  {path}:{no}  {token}")
    else:
        print("\nプレースホルダーは残っていません。")


if __name__ == "__main__":
    main()
