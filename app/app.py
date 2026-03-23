from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
import time

app = Flask(__name__)

# MySQL 接続設定（環境変数から取得）
db_config = {
    'host': os.getenv('DB_HOST', 'db'),
    'user': os.getenv('DB_USER', 'flaskuser'),
    'password': os.getenv('DB_PASSWORD', 'flaskpass'),
    'database': os.getenv('DB_NAME', 'flaskdb')
}

def get_db_connection():
    """MySQL への接続を取得（リトライ機能付き）"""
    max_retries = 5
    retry_interval = 2
    
    for attempt in range(max_retries):
        try:
            conn = mysql.connector.connect(**db_config)
            return conn
        except mysql.connector.Error as err:
            if attempt < max_retries - 1:
                print(f"データベース接続失敗（試行 {attempt + 1}/{max_retries}）: {err}")
                time.sleep(retry_interval)
            else:
                raise

@app.route('/')
def index():
    """ユーザー一覧を表示"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index.html', users=users, error=None)
    except Exception as e:
        return render_template('index.html', users=[], error=str(e))

@app.route('/add', methods=['POST'])
def add_user():
    """新規ユーザーを追加"""
    name = request.form.get('name')
    email = request.form.get('email')
    
    if not name or not email:
        return redirect(url_for('index'))
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (name, email) VALUES (%s, %s)',
            (name, email)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"ユーザー追加エラー: {e}")
    
    return redirect(url_for('index'))

@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    """ユーザーを削除"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"ユーザー削除エラー: {e}")
    
    return redirect(url_for('index'))

# @app.route('/health')
# def health():
#     """ヘルスチェック用エンドポイント"""
#     try:
#         conn = get_db_connection()
#         conn.close()
#         return {'status': 'healthy', 'database': 'connected'}, 200
#     except Exception as e:
#         return {'status': 'unhealthy', 'error': str(e)}, 503

# app/app.py の一部を変更
@app.route('/health')
def health():
    """ヘルスチェック用エンドポイント"""
    try:
        conn = get_db_connection()
        conn.close()
        return {
            'status': 'healthy',
            'database': 'connected',
            'version': '1.1.0'  # ← バージョンを追加
        }, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
