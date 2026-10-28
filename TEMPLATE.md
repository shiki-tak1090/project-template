# プロジェクトひな型の使い方

このリポジトリは、新しいプロジェクトのドキュメントリポジトリ（`<案件名>_document`）を作るためのひな型です。このファイルは、`/project-new` の実行後に削除されます。

## ひな型の初期設定（最初の 1 回だけ）

この設定は済んでいます（プラグインのリポジトリは `shiki-tak1090/claude-plugins`）。ひな型を別の GitHub アカウントや組織に移すときだけ、次の設定をやり直します。

1. プラグインのリポジトリ（`claude-plugins`）を GitHub に push する
2. このひな型の `YOUR_GITHUB_OWNER/claude-plugins` を、手順 1 のリポジトリ（例: `your-name/claude-plugins`）にすべて書き換えて、ひな型に commit・push する。書き換える場所は `.claude/settings.json` と `workspace/repo-snippets/README.md` の 2 か所

`/project-new` は、この設定が済んでいないと止まります。

## 新しいプロジェクトを始める手順

以下では、案件名を `acme` とします。案件名は英小文字・数字・`_`・`-` で付けます（フォルダ名とリポジトリ名に使うため）。

### 1. GitHub に空のリポジトリを作る

GitHub で `acme_document` という空のリポジトリを作ります（README も .gitignore も付けない）。コードのリポジトリ（`acme_backend` など）は、この時点では作らなくてかまいません。

### 2. 親フォルダを作り、ひな型を clone する

```bash
mkdir acme
```

```bash
git clone git@github.com:shiki-tak1090/project-template.git acme/acme_document
```

フォルダ名は必ず `<案件名>/<案件名>_document` にします。`/project-new` は、このフォルダ名から案件名を読み取ります。

### 3. `/project-new` を実行する

`acme/acme_document` で Claude Code を起動し、`/project-new` を実行します。次のことを対話で行います。

- プロジェクトの表示名、GitHub のオーナー、Backlog のプロジェクトキーなどを聞き、ひな型の `xxxxx` などを置き換える
- リポジトリの構成（backend、frontend など）を聞き、`00_プロジェクト概要/リポジトリ一覧.md` を埋める（各リポジトリの言語やツールは、コードリポジトリを作るときにそのリポジトリの中で宣言する）
- Git の履歴を作り直すか、ひな型の履歴を残すかを確認する
- 手順 1 で作ったリポジトリに push する（実行前に確認する）

### 4. `/project-init` を実行する

立ち上げ担当も、参画メンバーと同じ `/project-init` で自分の環境を整えます。参画手順に抜けがないかを、最初に確かめるためです。

## ひな型自体を直すとき

- 設計書の作成・変換スキルは、このひな型ではなく `project-docs` プラグインのリポジトリで管理しています。スキルを直すときはプラグインのリポジトリを更新します。各プロジェクトには自動更新で届きます
- このひな型で直すのは、フォルダ構成、テンプレート、`/project-new`、`/project-init`、CLAUDE.md などです
- `/project-new` と `/project-init` をプラグインに入れず、ひな型に置いているのは、プラグインが入る前に動く必要があるためです（`/project-init` はプラグインが入っているかを確認する側です）
- ひな型を直しても、すでに始まったプロジェクトには反映されません。必要なら各プロジェクトに手で取り込みます
