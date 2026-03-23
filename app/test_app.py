import pytest
from app import app
import os

@pytest.fixture
def client():
    """テスト用のクライアントを作成"""
    app.config['TESTING'] = True
    
    # テスト用の環境変数を設定
    os.environ['DB_HOST'] = 'localhost'
    os.environ['DB_USER'] = 'testuser'
    os.environ['DB_PASSWORD'] = 'testpass'
    os.environ['DB_NAME'] = 'testdb'
    
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """ヘルスチェックエンドポイントのテスト"""
    response = client.get('/health')
    
    # ステータスコードが 200 または 503 であることを確認
    assert response.status_code in [200, 503]
    
    # JSON レスポンスであることを確認
    assert response.content_type == 'application/json'
    
    # status フィールドが存在することを確認
    data = response.get_json()
    assert 'status' in data

def test_index_page(client):
    """トップページのテスト"""
    response = client.get('/')
    
    # ステータスコードが 200 であることを確認
    assert response.status_code == 200
    
    # HTML が返されることを確認
    assert b'<!DOCTYPE html>' in response.data

def test_add_user_validation(client):
    """ユーザー追加のバリデーションテスト"""
    # 空のデータで POST
    response = client.post('/add', data={})
    
    # リダイレクトされることを確認
    assert response.status_code == 302
