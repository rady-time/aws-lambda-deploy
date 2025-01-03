# GitHub Actions の説明と使い方

## GitHub Actionsとは
GitHub Actionsは、GitHubリポジトリで継続的インテグレーション（CI）および継続的デプロイメント（CD）を自動化するためのツールです。  
リポジトリ内のイベント（例: push、pull request、issue作成）をトリガーとして、さまざまなジョブを実行できます。

### 主な特徴
- **ワークフローの自動化**: コードのビルド、テスト、デプロイなどのプロセスを自動化。
- **YAML形式での設定**: `.github/workflows/`フォルダ内にYAMLファイルを配置して設定。
- **GitHubと統合**: 他のGitHub機能（リポジトリ、Issue、Pull Request）とシームレスに連携。

---

## 基本用語
- **Workflow**: 一連の自動化プロセス。YAMLファイルで定義。
- **Job**: ワークフロー内の1つのタスク群。並行または順次実行可能。
- **Step**: Job内の個々のタスク。
- **Runner**: ジョブを実行する環境。GitHubホストのランナーまたはセルフホスト型ランナー。

## よく使われる設定
### トリガーイベント
- **push**: 指定したブランチにコードがプッシュされたときに実行。
- **pull_request**: プルリクエストが作成または更新されたときに実行。
- **schedule**: 定期的なジョブ実行（Cron形式で指定）。
- **workflow_dispatch**: 手動でワークフローを実行。

### 使用するランナー
- **ubuntu-latest**: Ubuntu環境。
- **windows-latest**: Windows環境。
- **macos-latest**: macOS環境。

### 他のアクションを利用

GitHub Marketplaceには多数のアクションが公開されています。以下はその例です：

- **actions/checkout**: リポジトリのコードをチェックアウト。
- **actions/setup-node**: Node.js環境のセットアップ。
- **actions/setup-python**: Python環境のセットアップ。
- **actions/setup-java**:Java環境のセットアップ。
- **docker/login-action**: Docker Hubへのログイン。
- **aws-actions/configure-aws-credentials**:AWS認証情報のセットアップ。
- **aws-actions/amazon-ecr-login**:AWS ECRへのログイン。
- **aws-actions/setup-sam**:AWS SAMのセットアップ。

---

## GitHub Actionsのセットアップ

### 1. ワークフローファイルの作成
リポジトリのルートに以下のディレクトリとファイルを作成します。  
`.github/workflows/<ワークフローファイル名>.yml`

### 2. YAMLファイルの基本構造
以下は、pythonアプリケーションのAWSのLambdaにテストとデプロイを行う例です。

```yaml
# ワークフローの名称
name: Workflow

# Actionsを実行するトリガー
on:
  push:
    branches:
      - main

# 変数
env:
  ENV: dev/prod
  AWS_REGION: ap-northeast-1
  AWS_ROLE_ARN: arn:aws:iam::xxxxxxxxx:role/github_actions_role

# ジョブ
jobs:
  # ジョブ名称
  test-and-deploy:
    # ジョブを実行する環境（ランナー）
    runs-on: ubuntu-latest

    # ジョブ内で実行するステップ
    steps:
      # 資材のチェックアウト
      - name: Checkout code
        uses: actions/checkout@v3 

      # Python環境のセットアップ
      - name: Set up Python
        uses: actions/setup-python@v4 
        with:
          python-version: '3.12'

      # 必要な依存関係をインストール
      - name: Install dependencies
        run: pip install -r requirements.txt

      # SAM環境のセットアップ
      - name: Set up SAM
        uses: aws-actions/setup-sam@v2

      # テスト
      - name: Run tests
        run: pytest tests/

      # AWS環境の認証設定
      - name: Configure AWS credentials from IAM Role
        uses: aws-actions/configure-aws-credentials@v2
        with:
          role-to-assume: ${{ env.AWS_ROLE_ARN }}
          aws-region: ${{ env.AWS_REGION }}

      # SAMビルド
      - name: SAM deploy
        run: sam build 

      # SAMデプロイ
      - name: SAM deploy
        run: sam deploy --config-env ${{ env.ENV }} --no-confirm-changeset --no-fail-on-empty-changeset
```
