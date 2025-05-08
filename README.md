# Django Photo Diary Application - Setup Guide

## ローカル環境でのセットアップ手順

### 1. Gitからプロジェクトを取得後の初期設定

1. **仮想環境の作成と有効化**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

2. **依存パッケージのインストール**

   ```bash
   pip install -r requirements\base.txt
   pip install -r requirements\prod.txt
   ```

   ※ `django-storages` と `boto3` は別々の行にする必要があります

3. **必要なライブラリのインストール**

   ```bash
   pip install opencv-python
   pip install django-debug-toolbar
   ```

4. **環境変数の設定**

   プロジェクトルートに `.env` ファイルを作成し、以下のように記述：

   ```
   SECRET_KEY=適切な秘密鍵
   ```

5. **settings モジュールの設定修正**

   `manage.py` の `DJANGO_SETTINGS_MODULE` を `config.local` に変更：

   ```python
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.local')
   ```

6. **データベースのマイグレーション**

   ```bash
   python manage.py migrate
   ```

7. **管理ユーザーの作成**

   ```bash
   python manage.py createsuperuser
   ```

8. **開発サーバーの起動**

   ```bash
   python manage.py runserver
   ```

---

## 本番サーバーでの管理者パスワードリセット手順（自分用）

秘密鍵（`.ppk`）を使用してPuTTYからSSHログインし、Djangoの管理ユーザーのパスワードを変更する方法です。

### 1. PuTTYでのログイン設定

1. **Host Name**：`your-server-ip`（またはホスト名）
2. **Connection type**：SSH
3. **Connection > SSH > Auth**
   → `Private key file for authentication` に `.ppk` ファイルを指定（例：`your-key.ppk`）
4. **ログインユーザー名を入力**（例：`webapp`）

---

### 2. サーバーでの操作手順

```bash
cd ~/mysite
source venv/bin/activate
python manage.py shell
```

Django シェルに入ったら以下を実行：

```python
from accounts.models import CustomUser
CustomUser.objects.values('id', 'username', 'email')  # 登録ユーザー確認

user = CustomUser.objects.get(username='admin_user')  # 適宜変更
user.set_password('YourNewPassword123')  # 新しいパスワード
user.save()
exit()
```

※ `username='admin_user'` は、実際のユーザー名に置き換えてください。

仮想環境を終了：

```bash
deactivate
```

セッションを終了：

```bash
exit
```

---

### 3. パスワード変更後の確認

ブラウザで以下にアクセス：

```
https://your-server-domain/admin
```

新しいパスワードでログインできることを確認。

---

## 備考

* 管理者が存在しない場合は以下で新規作成：

  ```bash
  python manage.py createsuperuser
  ```

* `CustomUser` を使っていても `set_password()` → `save()` で安全に変更可能

* `.env` や `secrets.json` などの認証情報は `.gitignore` に追加しておくこと
