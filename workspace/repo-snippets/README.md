# コードリポジトリ用の設定例

`xxxxx_backend` などのコードリポジトリに入れておく設定の例。コードリポジトリを作ったときに、各リポジトリへ手で取り込む（開発工程に入ったときに、エージェントに取り込ませてもよい）。`/project-init` は、各リポジトリにこれらが入っているかを確認し、足りなければ報告する（コードリポジトリを勝手に書き換えることはしない）。

## 1. CLAUDE.md に追記する内容

各リポジトリの `CLAUDE.md` に、次の節を追記する。「開発環境の前提」「セットアップ」「テスト・lint・ビルド」の節は、リポジトリの言語やツールに合わせて書き換える。

- 「開発環境の前提」は `/project-init` が読み、入っているかを確認する
- 「セットアップ」のコマンドは `/project-init` が実行しない。参画したメンバーが自分で最初に実行する
- 「テスト・lint・ビルド」は `/project-dev:implement` がテストの実行に使う

言語の版は、表に書くだけでなく、言語の標準的な版の指定ファイル（`.nvmrc`、`.python-version`、`go.mod`、`.tool-versions` など）にも書く。`/project-init` は両方を読み、食い違っていれば報告する。

```markdown
## 開発環境の前提

このリポジトリのセットアップ（下の「セットアップ」のコマンド）を実行する前に、入っている必要があるもの。依存パッケージ（`npm install` などで入るもの）はここに書かない。

| ツール | 必要な版 | 用途 | 確認コマンド | 必須 |
|---|---|---|---|---|
| （例: Node.js） | （例: 22.x。`.nvmrc` と同じ） | （例: 実行環境） | `node --version` | 必須 |
| （例: pnpm） | （例: 9.x） | （例: パッケージ管理） | `pnpm --version` | 必須 |
| （例: Docker） | 任意 | （例: ローカルの DB を動かす） | `docker --version` | 必須 |

## セットアップ

clone した後に、最初に 1 回実行するコマンド。

| 作業 | コマンド |
|---|---|
| 依存パッケージのインストール | （例: `pnpm install`） |
| 環境変数のファイルの作成 | （例: `.env.example` を `.env` にコピーして値を埋める） |

## 設計書

このリポジトリの設計書は、ドキュメントリポジトリ `../xxxxx_document` にある。

- 要件定義: `../xxxxx_document/01_要件定義/`
- 詳細設計: `../xxxxx_document/03_詳細設計/`
- API の統合仕様: `../xxxxx_document/04_API仕様/`（`openapi.yaml` を正とする）
- DB の統合仕様: `../xxxxx_document/05_DB設計/`
- 実装タスク: `../xxxxx_document/97_タスク分解/`

実装が設計と食い違う場合は、黙って設計と違う実装をしない。設計の誤りや決め漏れを見つけたら、作業を止めてユーザーに確認する。

## テスト・lint・ビルド

| 作業 | コマンド |
|---|---|
| テスト（全体） | （例: `uv run pytest`） |
| テスト（1 ファイル） | （例: `uv run pytest tests/test_xxx.py`） |
| lint | （例: `uv run ruff check .`） |
| 型チェック | （例: `uv run mypy src`） |
| ビルド | （例: なし） |

## Git とタスク管理

- 作業は `develop` から `feature/<課題キー>-<内容>` のブランチを切り、PR は `develop` に向ける
- このリポジトリのコミットに、他のリポジトリの変更を混ぜない
- タスクは Backlog（プロジェクトキー: `{{Backlogのプロジェクトキー}}`）で管理する。ブランチ名とコミットメッセージに課題キー（例: `{{Backlogのプロジェクトキー}}-123`）を入れる
- PR は GitHub で作り、PR のリンクを Backlog の課題にコメントする
- タスクの実装は `/project-dev:implement <タスク ID>` で行う
```

## 2. .claude/settings.json

このリポジトリで起動した Claude Code から設計書を読めるようにし、実装用のプラグインを有効にする。マーケットプレイスの `repo` は、ドキュメントリポジトリの `.claude/settings.json` と同じ値にする。

```json
{
  "extraKnownMarketplaces": {
    "project-plugins": {
      "source": {
        "source": "github",
        "repo": "shiki-tak1090/claude-plugins"
      },
      "autoUpdate": true
    }
  },
  "enabledPlugins": {
    "project-dev@project-plugins": true
  },
  "permissions": {
    "additionalDirectories": ["../xxxxx_document"]
  }
}
```
