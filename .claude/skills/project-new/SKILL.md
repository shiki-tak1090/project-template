---
name: project-new
description: プロジェクトのひな型から、新しいプロジェクトのドキュメントリポジトリ（<案件名>_document）を作るスキル。Git の置き場所（GitHub か Azure DevOps）、表示名、clone 元、Backlog のプロジェクトキー、リポジトリ構成を対話で聞き、ひな型のプレースホルダーを置き換え、リポジトリ一覧（00_プロジェクト概要/リポジトリ一覧.md）を埋め、新しいリモートに push するところまで行う。「新しいプロジェクトを始めたい」「ひな型からプロジェクトを作って」「/project-new」で使う。ひな型を clone した直後に 1 回だけ使う。
disable-model-invocation: true
---

# 新しいプロジェクトの作成（軸 A）

ひな型を clone した直後のリポジトリを、新しいプロジェクトのドキュメントリポジトリに作り変える。このスキルはプロジェクトごとに 1 回だけ使い、最後に自分自身（このスキルのフォルダ）と `TEMPLATE.md` を削除する。

案件のリポジトリの置き場所は、GitHub と Azure DevOps のどちらでもよい。置き場所によって変わるのは、clone 元の URL の形、PR を作るツール、既定のブランチの設定画面だけである。

## 0. 前提の確認

次の点を確認する。1 つでも満たさなければ、理由を伝えて止まる。

1. カレントディレクトリの名前が `<案件名>_document` で、その親フォルダの名前が `<案件名>` であること。ここから案件名を読み取る。違う場合は、`TEMPLATE.md` の手順 2 のとおりに clone し直してもらう。
2. `TEMPLATE.md` があること（ひな型のままの状態であること）。ない場合は、すでに作成済みのプロジェクトなので何もしない。
3. `.claude/settings.json` のマーケットプレイスの `repo` に、プラグインのリポジトリ（`<オーナー>/claude-plugins`）が設定されていること。空や `YOUR_GITHUB_OWNER/...` のような仮の値なら、ひな型の管理者に `TEMPLATE.md` の「プラグインの参照先を変えるとき」の手順を済ませてもらう。プラグインのリポジトリは GitHub にあり、案件の置き場所が Azure DevOps でもそのまま使う。
4. `git status` に未コミットの変更がないこと。

## 1. 対話で聞くこと

推測で埋めない。

**1-1. Git の置き場所**

AskUserQuestion で、GitHub か Azure DevOps かを選んでもらう（選択肢は 2 つ）。

**1-2. そのほかの項目**

次の項目は自由に記述してもらう答えなので、AskUserQuestion（選択肢から選ばせる道具）は使わない。チャットのメッセージで、項目の一覧を例と一緒に番号付きで 1 回で示し、まとめて答えてもらう。答えが返ってくるまで先に進まない。0 で読み取った案件名も示し、違っていればここで直してもらう。

| 項目 | 例（GitHub） | 例（Azure DevOps） | 使う場所 |
|---|---|---|---|
| プロジェクトの表示名 | ACME 会員アプリ | 同左 | 各文書の見出し |
| ドキュメントリポジトリの clone 元（手順 1 で作った空のリポジトリ） | `git@github.com:acme-inc/acme_document.git` | `git@ssh.dev.azure.com:v3/acme-org/ACME/acme_document` | リポジトリ一覧、README、push 先 |
| Backlog のプロジェクトキー | ACME | 同左 | 課題キーの例、運用ルール |
| リポジトリへのアクセス権の依頼先 | 山田さん | 同左 | リポジトリ一覧、README |
| コードリポジトリの構成・役割・clone 元 | backend（API）`git@github.com:acme-inc/acme_backend.git` | backend（API）`git@ssh.dev.azure.com:v3/acme-org/ACME/acme_backend` | リポジトリ一覧、ワークスペースの構成図 |

- clone 元は、組み立てずに、GitHub や Azure DevOps の画面の「Clone」に表示される URL をそのまま書いてもらう（Azure DevOps は「組織/プロジェクト/リポジトリ」の 3 段になるため）。
- リモートのリポジトリ名は問わない（Azure DevOps では `document`、`backend` のように案件名を付けないことが多い）。手元のフォルダ名は、リモートの名前によらず常に `<案件名>_document`、`<案件名>_backend` の形にする。スキルは手元のフォルダ名でリポジトリを探すため。
- コードリポジトリは、この時点で作られていなくてよい。未作成のものは clone 元を「未作成」とする。
- 各リポジトリの言語やツールは、ここでは聞かない。コードリポジトリを作るときに、そのリポジトリの `CLAUDE.md` の「開発環境の前提」に書く（`workspace/repo-snippets/README.md` を参照）。

AskUserQuestion は、1-1 と、この後の「2 つ以上の本当の選択肢から選ぶ」質問（4 の履歴の扱いなど）にだけ使う。選択肢が 1 つしかない質問を作らない。

## 2. プレースホルダーの置き換え

まず `--dry-run` で置き換わるファイルを確認してから、本実行する。`--git-host` は `github` か `azure-devops` にする。

```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/apply_project.py --slug <案件名> --name "<表示名>" --git-host <github|azure-devops> --doc-repo-url "<clone 元>" --backlog-key <キー> --admin "<依頼先>" --dry-run
```

```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/apply_project.py --slug <案件名> --name "<表示名>" --git-host <github|azure-devops> --doc-repo-url "<clone 元>" --backlog-key <キー> --admin "<依頼先>"
```

スクリプトは、clone 元が選んだ置き場所の URL の形になっているかを確かめる。合わなければエラーで止まるので、ユーザーに URL を確かめてもらう。リモートのリポジトリ名が `<案件名>_document` と違う場合は注意を表示するだけで、そのまま進める。

スクリプトは、置き場所に合わせて次のものも埋める。

- `CLAUDE.md` の「開発環境の前提」の、PR を作るツールの行（GitHub なら GitHub CLI、Azure DevOps なら Azure CLI と azure-devops 拡張）
- 文書の中の「Git の置き場所」「PR を作るツール」
- `README.md` の冒頭にある「ひな型の案内」（ひな型の段階でだけ表示する囲み）の削除

最後に「残っているプレースホルダー」を一覧する。次のものは対話の結果をもとに、手で埋める。

| プレースホルダー | ファイル | 埋める内容 |
|---|---|---|
| `{{コードリポジトリの行}}` | `00_プロジェクト概要/リポジトリ一覧.md` | コードリポジトリの行（手元のフォルダ、役割、clone 元、既定のブランチ）。手元のフォルダは `<案件名>_backend` の形、clone 元は 1-2 で聞いた URL をそのまま書く |
| `{{コードリポジトリの構成図}}` | `workspace/CLAUDE.md` | 構成図のコードリポジトリの行（`├── acme_backend/  # バックエンド` の形） |

あわせて、`.claude/settings.json` の `permissions.additionalDirectories` に、コードリポジトリ（`../<案件名>_backend` など）を追加する。

最後に `--check` を実行し、プレースホルダーが残っていないことを確かめる。

```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/apply_project.py --check
```

## 3. ひな型用のファイルの削除

ユーザーに確認してから、次のものを削除する。

- `TEMPLATE.md`
- このスキルのフォルダ（`.claude/skills/project-new/`）

## 4. Git の履歴とリモート

ユーザーに次のどちらにするかを聞く。

| 選択肢 | 内容 |
|---|---|
| 履歴を作り直す（おすすめ） | ひな型の履歴を消し、「初期構成」の 1 コミットから始める。プロジェクトの履歴にひな型の変更が混ざらない |
| ひな型の履歴を残す | ひな型の変更履歴をそのまま引き継ぐ |

履歴を作り直す場合は、`.git` を削除して作り直すことになるため、実行前にもう一度確認する。

既定のブランチは `develop` にする（作業は `develop` で行い、`main` はリリース済みのドキュメント用）。次の順で進める。

1. `develop` ブランチに切り替える
   - 履歴を作り直す場合: `.git` を削除したあと、`git init -b develop` で作り直す
   - ひな型の履歴を残す場合: `git switch -c develop` で、ひな型の `main` から `develop` を作る
2. `develop` で、変更をすべてコミットする（コミットメッセージ: `初期構成`）
3. `develop` から `main` ブランチを作る（`git branch main`）。作業ブランチは `develop` のままにしておく
4. `origin` を、1-2 で聞いたドキュメントリポジトリの clone 元に向ける。ひな型の履歴を残す場合は、ひな型の remote を `template` という名前に変えて残す
5. **push の前に、push 先の URL とブランチをユーザーに見せて確認を取る。** 了承を得たら、**`develop` を先に** push し、続けて `main` を push する（`git push -u origin develop`、`git push origin main`）。空のリポジトリでは、最初に push したブランチが既定のブランチになることが多いため
6. 既定のブランチが `develop` になったことを確かめる（`git ls-remote --symref origin HEAD` の出力が `refs/heads/develop` を指していること）。`develop` でなければ、次の画面で `develop` に変えるよう、ユーザーに伝える（設定の変更は代行しない）
   - GitHub: リポジトリの Settings → General → Default branch
   - Azure DevOps: Repos → Branches で `develop` の「…」→ Set as default branch

空のリポジトリがまだ作られていなければ、作ってもらうよう伝えて、push の手前で止まる。リポジトリの作成は代行しない。Azure DevOps でリポジトリを作るときは、README を付けずに（「Add a README」を外して）作ってもらう。

## 5. 報告

次の内容を報告する。

1. 置き換えた値（案件名、表示名、Git の置き場所、clone 元、Backlog のキー）
2. リポジトリ一覧.md に登録したリポジトリの一覧
3. push した先と、既定のブランチの確認結果（またはまだ push していない理由）
4. 次の手順: このまま `/project-init` を実行して、自分の環境を整えること。参画メンバーには README の参画手順を案内すること
