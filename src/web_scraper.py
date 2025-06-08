import requests
from bs4 import BeautifulSoup
import os
import csv
from datetime import datetime

class WebScraper:
    def __init__(self, output_directory="collected_data"):
        """
        WebScraperクラスの初期化
        output_directory: 収集したデータを保存するフォルダ名
        """
        # データ保存先ディレクトリの設定
        self.output_folder = output_directory
        # ディレクトリが存在しない場合は作成
        os.makedirs(self.output_folder, exist_ok=True)
        
        # HTTP設定の初期化
        self.setup_http_config()
        
        print(f"WebScraper初期化完了 - 保存先: {self.output_folder}")

    def setup_http_config(self):
        """
        HTTP通信用の設定を初期化
        練習用ページ取得のためのヘッダー情報とタイムアウト設定を行う
        """
        # HTTP通信用ヘッダー設定（ブラウザのふりをするための情報）
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',  # ブラウザの種類とバージョン情報
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',  # 受け取り可能なデータ形式
            'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',  # 言語設定（日本語優先）
            'Accept-Encoding': 'gzip, deflate, br',  # 圧縮形式の対応状況
            'Connection': 'keep-alive',  # 接続を維持する設定
            'Upgrade-Insecure-Requests': '1'  # セキュアな接続への自動アップグレード
        }
        
        # リクエストのタイムアウト時間（秒）
        self.timeout = 10
        
        print("HTTP設定完了")

    def fetch_webpage(self, url):
        """
        指定されたURLから練習用Webページを取得
        url: 取得したい練習ページのURL
        """
        try:
            print(f"練習用ページ取得開始: {url}")
            
            # HTTPリクエストを送信してWebページを取得
            response = requests.get(
                url,                    # 取得するURL
                headers=self.headers,   # HTTPヘッダー情報
                timeout=self.timeout    # タイムアウト時間
            )
            
            # HTTPステータスコードの確認（200なら成功）
            if response.status_code == 200:
                print(f"✓ ページ取得成功 - ステータスコード: {response.status_code}")
                # HTMLテキストを返す
                return response.text
            else:
                print(f"✗ ページ取得失敗 - ステータスコード: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            print(f"✗ タイムアウトエラー: {url}")
            return None
        except requests.exceptions.ConnectionError:
            print(f"✗ 接続エラー: {url}")
            return None
        except requests.exceptions.RequestException as error:
            print(f"✗ リクエストエラー: {error}")
            return None
        except Exception as error:
            print(f"✗ 予期しないエラー: {error}")
            return None

    def validate_url(self, url):
        """
        URLが正しい形式かを検証
        url: 検証するURL文字列
        """
        # URLの基本チェック
        if not url or not isinstance(url, str):
            print("✗ URLが入力されていません")
            return False
        
        # httpsまたはhttpで始まっているかチェック
        if not (url.startswith('https://') or url.startswith('http://')):
            print("✗ URLはhttps://またはhttp://で始まる必要があります")
            return False
        
        # 基本的な文字が含まれているかチェック
        if '.' not in url:
            print("✗ 有効なドメインが含まれていません")
            return False
        
        print("✓ URLの形式が正しいです")
        return True

    def test_connection(self, url):
        """
        指定されたURLへの接続テスト
        url: テストする練習用URL
        """
        print(f"\n--- 接続テスト実行中 ---")
        
        # URL形式の検証
        if not self.validate_url(url):
            return False
        
        # 練習用Webページ取得テスト
        html_content = self.fetch_webpage(url)
        
        if html_content:
            # 取得したHTMLの基本情報を表示
            content_length = len(html_content)
            print(f"✓ HTML取得成功 - サイズ: {content_length:,} 文字")
            
            # HTMLの最初の100文字を表示（デバッグ用）
            preview = html_content[:100].replace('\n', ' ').replace('\r', ' ')
            print(f"HTMLプレビュー: {preview}...")
            
            return True
        else:
            print("✗ 接続テスト失敗")
            return False

    def parse_html_content(self, html_content):
        """
        HTMLコンテンツを解析してBeautifulSoupオブジェクトを作成
        html_content: 解析するHTML文字列
        """
        try:
            # BeautifulSoupでHTMLを解析
            soup = BeautifulSoup(html_content, 'html.parser')
            print("✓ HTML解析完了")
            return soup
        except Exception as error:
            print(f"✗ HTML解析エラー: {error}")
            return None

    def extract_product_data(self, soup):
        """
        BeautifulSoupオブジェクトから商品データを抽出
        soup: 解析済みのBeautifulSoupオブジェクト
        """
        try:
            print("商品データ抽出開始...")
            
            # 抽出したデータを格納するリスト
            products_list = []
            
            # 商品情報を含むdivタグを全て取得
            product_elements = soup.find_all('div', class_='col-md-4 col-xl-4 col-lg-4')
            
            print(f"発見された商品数: {len(product_elements)}")
            
            # 各商品要素から情報を抽出
            for product_element in product_elements:
                # 商品タイトルの抽出（完全なタイトルを取得）
                title_element = product_element.find('a', class_='title')
                if title_element:
                    # title属性も確認して完全なタイトルを取得
                    product_title = title_element.get('title', '').strip()
                    if not product_title:
                        product_title = title_element.text.strip()
                else:
                    product_title = "タイトル不明"
                
                # 商品価格の抽出
                price_element = product_element.find('h4', class_='price float-end card-title pull-right')
                product_price = price_element.text.strip() if price_element else "価格不明"
                
                # 商品説明の抽出
                description_element = product_element.find('p', class_='description card-text')
                product_description = description_element.text.strip() if description_element else "説明なし"
                
                # 抽出したデータを辞書形式で保存
                product_info = {
                    'title': product_title,
                    'price': product_price,
                    'description': product_description
                }
                
                products_list.append(product_info)
            
            print(f"✓ データ抽出完了 - {len(products_list)}件の商品情報を取得")
            return products_list
            
        except Exception as error:
            print(f"✗ データ抽出エラー: {error}")
            return []

    def validate_extracted_data(self, products_data):
        """
        抽出されたデータの検証
        products_data: 抽出された商品データのリスト
        """
        if not products_data:
            print("✗ 抽出されたデータがありません")
            return False
        
        # データの基本統計を表示
        total_products = len(products_data)
        valid_titles = sum(1 for product in products_data if product['title'] != "タイトル不明")
        valid_prices = sum(1 for product in products_data if product['price'] != "価格不明")
        
        print(f"データ検証結果:")
        print(f"  総商品数: {total_products}")
        print(f"  有効なタイトル: {valid_titles}")
        print(f"  有効な価格: {valid_prices}")
        
        # 検証成功の条件
        if valid_titles > 0 and valid_prices > 0:
            print("✓ データ検証成功")
            return True
        else:
            print("✗ データ検証失敗")
            return False

    def display_extracted_data(self, products_data, max_display=5):
        """
        抽出されたデータを表示
        products_data: 表示する商品データのリスト
        max_display: 表示する最大件数
        """
        if not products_data:
            print("表示可能なデータがありません")
            return
        
        print(f"\n=== 抽出されたデータ（最大{max_display}件表示） ===")
        
        # 指定された件数まで表示
        display_count = min(len(products_data), max_display)
        
        for i in range(display_count):
            product = products_data[i]
            print(f"\n【商品 {i+1}】")
            print(f"タイトル: {product['title']}")
            print(f"価格: {product['price']}")
            print(f"説明: {product['description'][:100]}...")  # 説明は100文字まで表示
            print("-" * 50)
        
        if len(products_data) > max_display:
            print(f"\n※ 他に{len(products_data) - max_display}件のデータがあります")

    def scrape_website_data(self, url):
        """
        指定されたURLからデータを抽出する統合処理
        url: スクレイピング対象のURL
        """
        print(f"\n{'='*60}")
        print(f"Webスクレイピング実行開始")
        print(f"対象URL: {url}")
        print(f"{'='*60}")
        
        # Step1: Webページの取得
        html_content = self.fetch_webpage(url)
        if not html_content:
            print("✗ Webページの取得に失敗しました")
            return None
        
        # Step2: HTML解析
        soup = self.parse_html_content(html_content)
        if not soup:
            print("✗ HTML解析に失敗しました")
            return None
        
        # Step3: データ抽出
        products_data = self.extract_product_data(soup)
        if not products_data:
            print("✗ データ抽出に失敗しました")
            return None
        
        # Step4: データ検証
        if not self.validate_extracted_data(products_data):
            print("✗ データ検証に失敗しました")
            return None
        
        print("✓ 全ての処理が正常に完了しました")
        return products_data

    def save_data_to_file(self, products_data, filename=None):
        """
        抽出されたデータをCSVファイルに保存
        products_data: 保存する商品データのリスト
        filename: 保存ファイル名（指定しない場合は自動生成）
        """
        try:
            # ファイル名が指定されていない場合は自動生成
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"scraped_data_{timestamp}.csv"
            
            # 保存先のフルパスを作成
            file_path = os.path.join(self.output_folder, filename)
            
            # CSVファイルとして保存
            with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
                # CSVライターを作成
                writer = csv.writer(csv_file)
                
                # ヘッダー行を書き込み
                writer.writerow(['タイトル', '価格', '説明'])
                
                # 各商品データを書き込み
                for product in products_data:
                    writer.writerow([
                        product['title'],
                        product['price'],
                        product['description']
                    ])
            
            print(f"✓ データ保存完了: {file_path}")
            print(f"  保存件数: {len(products_data)}件")
            return file_path
            
        except IOError as io_error:
            print(f"✗ ファイル保存エラー: {io_error}")
            return None
        except Exception as error:
            print(f"✗ データ保存中の予期しないエラー: {error}")
            return None

    def verify_saved_file(self, file_path):
        """
        保存されたCSVファイルの内容を確認
        file_path: 確認するファイルのパス
        """
        try:
            # ファイルの存在確認
            if not os.path.exists(file_path):
                print(f"✗ ファイルが見つかりません: {file_path}")
                return False
            
            # ファイルサイズを取得
            file_size = os.path.getsize(file_path)
            print(f"保存ファイル確認:")
            print(f"  ファイルパス: {file_path}")
            print(f"  ファイルサイズ: {file_size:,} バイト")
            
            # CSVファイルを読み込んで行数を確認
            with open(file_path, 'r', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file)
                rows = list(reader)
                
                # ヘッダー行を除いたデータ行数を計算
                data_rows = len(rows) - 1 if len(rows) > 0 else 0
                
                print(f"  データ行数: {data_rows}行")
                print(f"  ヘッダー: {', '.join(rows[0]) if len(rows) > 0 else 'なし'}")
            
            print("✓ ファイル保存が正常に完了しています")
            return True
            
        except Exception as error:
            print(f"✗ ファイル確認エラー: {error}")
            return False

    def handle_scraping_errors(self, url, max_retries=3):
        """
        スクレイピングエラーの処理と再試行機能
        url: スクレイピング対象のURL
        max_retries: 最大再試行回数
        """
        for attempt in range(max_retries):
            try:
                # データ抽出を実行
                result = self.scrape_website_data(url)
                
                if result:
                    return result
                else:
                    print(f"✗ データ取得に失敗しました")
                    
            except Exception as error:
                print(f"✗ エラーが発生しました: {error}")
            
            # 最後の試行でない場合は待機
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2  # 2秒、4秒、6秒と待機時間を増加
                print(f"  {wait_time}秒待機してから再試行します...")
                import time
                time.sleep(wait_time)
        
        print(f"✗ {max_retries}回の試行すべてが失敗しました")
        return None

    def run_interactive_scraping(self):
        """
        対話式スクレイピングモード
        ユーザーからの入力を受け付けてスクレイピングを実行
        """
        print("\n" + "="*60)
        print("Webスクレイピング 対話モード")
        print("="*60)
        print("使い方:")
        print("1. スクレイピング対象のURLを入力してください")
        print("2. 'exit'と入力すると終了します")
        print("3. 練習用URL: https://webscraper.io/test-sites/e-commerce/allinone")
        print("-"*60)
        print("※ 今後このコードを元に他のURLに合わせて改良してみてください")
        
        scraping_count = 0  # スクレイピング実行回数のカウンター
        
        while True:
            try:
                # ユーザー入力の取得
                user_input = input("\nスクレイピング対象URL >>> ").strip()
                
                # 終了コマンドの確認
                if user_input.lower() == 'exit':
                    print(f"\nスクレイピングを終了します")
                    print(f"総実行回数: {scraping_count}回")
                    break
                
                # 空の入力をスキップ
                if not user_input:
                    print("URLを入力してください")
                    continue
                
                # エラー復旧機能付きスクレイピング実行
                extracted_data = self.handle_scraping_errors(user_input)
                
                if extracted_data:
                    # データ表示
                    self.display_extracted_data(extracted_data)
                    
                    # データ保存
                    saved_file = self.save_data_to_file(extracted_data)
                    if saved_file:
                        self.verify_saved_file(saved_file)
                    
                    scraping_count += 1
                else:
                    print("スクレイピングに失敗しました")
                
            except KeyboardInterrupt:
                print(f"\n\nプログラムが中断されました")
                print(f"総実行回数: {scraping_count}回")
                break
            except Exception as interface_error:
                print(f"エラーが発生しました: {interface_error}")


def main():
    """
    WebScraperの完全版テスト
    対話式モードでユーザー操作を受け付け
    """
    print("=== Webスクレイピング 完全版システム ===")
    
    # WebScraperクラスのインスタンス作成
    scraper = WebScraper()
    
    # 対話式スクレイピングモードの開始
    scraper.run_interactive_scraping()

    # # 以前のテスト機能（現在は使用しない）
    # target_url = "https://webscraper.io/test-sites/e-commerce/allinone"
    # extracted_data = scraper.scrape_website_data(target_url)
    # if extracted_data:
    #     scraper.display_extracted_data(extracted_data)
    #     print(f"\n✓ テスト成功 - {len(extracted_data)}件のデータを抽出しました")


if __name__ == "__main__":
    main()