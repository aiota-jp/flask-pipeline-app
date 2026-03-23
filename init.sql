-- データベースが存在しない場合は作成
CREATE DATABASE IF NOT EXISTS flaskdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- データベースを使用
USE flaskdb;

-- users テーブルを作成
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- サンプルデータを挿入
INSERT INTO users (name, email) VALUES
    ('YamadaTaro', 'taro@example.com'),
    ('SatoHanako', 'hanako@example.com'),
    ('SuzukiJiro', 'jiro@example.com')
ON DUPLICATE KEY UPDATE name=name;
