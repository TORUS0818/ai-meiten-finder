# AI Meiten Finder

AIによる感情分析を使った、公平な飲食店スコアリングシステム。

## 概要

このプロジェクトは、食べログなどのレビューサイトから口コミを収集し、AIによる感情分析でスコアリングすることで、広告やバイアスに左右されない、真の店舗評価を提供することを目指します。

## ディレクトリ構成 (Directory Structure)

```
ai-meiten-finder/
├── src/
│   └── ai_meiten_finder/
│       ├── __init__.py     # パッケージの初期化ファイル
│       ├── cli.py          # CLIのエントリーポイント
│       ├── scraper.py      # スクレイピング処理
│       └── analyzer.py     # 感情分析処理
│
├── tests/                  # テストコード
├── notebooks/              # 実験用のJupyter Notebook
├── .venv/                  # 仮想環境 (Git管理外)
├── .gitignore              # Gitの無視ファイル
├── pyproject.toml          # プロジェクト設定
└── README.md               # このファイル
```

## 開発環境のセットアップ (Setup)

開発を始めるには、以下の手順で環境を構築してください。

1.  **リポジトリをクローンする**
    ```bash
    git clone https://github.com/[YOUR_GITHUB_USERNAME]/ai-meiten-finder.git
    cd ai-meiten-finder
    ```

2.  **`uv` をインストールする**
    `uv` がまだインストールされていない場合は、以下のコマンドでインストールしてください。
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

3.  **仮想環境の作成と有効化**
    ```bash
    # 仮想環境を作成
    uv venv

    # 仮想環境を有効化
    source .venv/bin/activate
    ```
    ターミナルのプロンプトの前に `(.venv)` と表示されれば成功です。

4.  **依存ライブラリのインストール**
    ```bash
    # zsh をお使いの場合
    uv pip install -e ".[dev]"

    # bash など、その他のシェルをお使いの場合
    uv pip install -e .[dev]
    ```
    これで、開発に必要なライブラリがすべてインストールされます。

## 開発の進め方 (Development Workflow)

私たちは、以下の流れで開発を進めます。

1.  **タスクの管理 (Task Management)**
    -   **Issueの作成:** まず、[GitHub Issues](https://github.com/[YOUR_GITHUB_USERNAME]/ai-meiten-finder/issues) で作業チケット（Issue）を作成します。すべての作業はIssueから始めます。
    -   **期限の設定:** 作成したIssueは、関連する**マイルストーン**に紐付け、期限を明確にします。
    -   **進捗の可視化:** Issueは[GitHub Projects](https://github.com/[YOUR_GITHUB_USERNAME]/ai-meiten-finder/projects)のボード上で管理します。作業を開始する際に「Todo」から「In Progress」へ移動させるなど、常に最新の状態を保ちます。

2.  **ブランチを作成する**
    -   作業を始める前に、`main`ブランチから、作業内容に合わせた名前のブランチを作成します。
    -   ブランチ名のルール:
        -   機能追加: `feature/issue番号-分かりやすい名前` (例: `feature/1-add-scraper-function`)
        -   バグ修正: `bugfix/issue番号-分かりやすい名前` (例: `bugfix/2-fix-login-error`)
    ```bash
    # 最新のmainブランチに移動
    git checkout main
    git pull origin main

    # 新しいブランチを作成して移動
    git checkout -b feature/1-add-scraper-function
    ```

3.  **コーディングとコミット**
    -   コードを書き、一区切りついたらコミットします。コミットメッセージは、何をしたか分かりやすく記述します。

4.  **プルリクエストを作成する**
    -   作業が終わったら、GitHubにプッシュし、`main`ブランチへの**プルリクエスト (Pull Request)** を作成します。
    -   プルリクエストの説明には、どのIssueに対応しているか (`Closes #1` など) と、どんな変更をしたかを記述します。
    -   もう一人の開発者をレビュアーに指定します。

5.  **レビューとマージ**
    -   レビュアーはコードを確認し、問題がなければ承認 (Approve) します。
    -   承認されたら、プルリクエストを`main`ブランチにマージします。