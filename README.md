# Django Photo Diary Application - Setup Guide

## ローカル環境でのセットアップ手順

### 1. Gitからプロジェクトを取得後の初期設定

1. **仮想環境の作成と有効化**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

2. **依存パッケージのインストール**:
   ```bash
   pip install -r requirements\base.txt
   pip install -r requirements\prod.txt
   ```
   * 注意: django-storages と boto3 は別々の行にする必要があります

3. **必要なライブラリのインストール**:
   ```bash
   pip install opencv-python
   pip install django-debug-toolbar   
   ```

4. **環境変数の設定**:
   * プロジェクトルートに `.env` ファイルを作成し、必要な環境変数を設定:
     ```
     SECRET_KEY=適切な秘密鍵
     ```

5. **settings モジュールの設定修正**:
   * `manage.py` の `DJANGO_SETTINGS_MODULE` を `config.local` に変更:
     ```python
     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.local')
     ```

6. **データベースのマイグレーション**:
   ```bash
   python manage.py migrate
   ```

7. **管理ユーザーの作成**:
   ```bash
   python manage.py createsuperuser
   ```

8. **開発サーバーの起動**:
   ```bash

   python manage.py runserver