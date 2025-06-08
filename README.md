# Webスクレイピングデータ収集システム

## プロジェクト内容

requestsとBeautifulSoupを使用したWebスクレイピングツールです。練習用サイトから商品情報を自動的に収集し、CSVファイルに保存する機能を実装しています。Pythonによる HTTP通信、HTML解析、データ抽出技術を学習することを目的として開発しました。

## プロジェクト構成

```
web_data_collector/
├── src/
│   └── web_scraper.py          # メインプログラム
├── collected_data/             # 収集データ保存フォルダ
├── requirements.txt            # 依存関係管理
├── README.md                   # プロジェクト説明書
└── .gitignore                  # Git除外ファイル設定
```

## 必要要件/開発環境

- **Python 3.7以上**
- **VSCode** (開発環境)
- **Git** (バージョン管理)
- **インターネット接続** (Webスクレイピング用)

### 使用ライブラリ

- **requests** HTTP通信とWebページ取得処理
- **beautifulsoup4** HTML解析とデータ抽出処理
- **csv** CSVファイル形式での保存処理
- **os** ファイルシステム操作

## 機能

- **URL検証** 入力されたURLの形式確認と妥当性チェック
- **Webページ取得** HTTP通信によるWebページの自動取得
- **HTML解析** BeautifulSoupを使用したHTML構造の解析
- **データ抽出** 商品タイトル、価格、説明の自動抽出
- **CSV保存** 抽出データのCSVファイル形式での保存
- **エラーハンドリング** 通信エラーや解析エラーの適切な処理
- **再試行機能** 失敗時の自動再試行機能
- **対話式インターフェース** ユーザーフレンドリーなコマンドライン操作

## 実行方法

### 1. リポジトリのクローン

```bash
git clone https://github.com/yourusername/web_data_collector.git
cd web_data_collector
```

### 2. 仮想環境の作成・アクティベート

**Windows**

```bash
python -m venv myenv
myenv\Scripts\activate
```

**macOS**

```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 4. プログラムの実行

```bash
python src/web_scraper.py
```

実行後、対話式インターフェースが起動し、URLを入力するとcollected_dataフォルダに収集したデータがCSVファイルとして保存されます。

## 使用方法

1. プログラムを実行すると対話式モードが開始されます
2. スクレイピング対象のURLを入力してください
3. 練習用URL: https://webscraper.io/test-sites/e-commerce/allinone
4. 'exit'と入力するとプログラムが終了します

## データ形式について

* **対象URL** 練習用スクレイピングサイト
* **出力データ** CSV形式の商品情報ファイル
* **保存場所** collected_dataフォルダ内

## 注意事項

- このツールは教育目的で作成されています
- 練習用サイト以外をスクレイピングする際は利用規約を確認してください
- 今後このコードを元に他のURLに合わせて改良してみてください

## 開発者

YuYu