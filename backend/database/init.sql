-- ============================================
-- 企业办公助手 - MySQL 数据库初始化脚本
-- ============================================

CREATE DATABASE IF NOT EXISTS enterprise_assistant
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE enterprise_assistant;

-- 管理员用户表
CREATE TABLE IF NOT EXISTS admin_users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(20) NOT NULL DEFAULT 'admin',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 员工表
CREATE TABLE IF NOT EXISTS employees (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(20) NOT NULL,
  age INT NOT NULL,
  email VARCHAR(255) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_created_at (created_at),
  CONSTRAINT chk_age CHECK (age >= 18 AND age <= 60)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 设备分类表
CREATE TABLE IF NOT EXISTS categories (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(20) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 设备表
CREATE TABLE IF NOT EXISTS devices (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  model VARCHAR(100) DEFAULT '',
  category_id INT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT,
  INDEX idx_category_id (category_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 预设管理员账号: admin / admin123
-- 密码使用 werkzeug.security.generate_password_hash 生成
INSERT INTO admin_users (username, password_hash, role) VALUES
('admin', 'scrypt:32768:8:1$3kfJdDeTUd4abEzf$ca7e635f9e315fdd994a98847ef6e0d4cc8967eff6d1640de5a5412a503947378d7c9d9278b293a397bb9f28fe026ce7bc94fa9b5f38ed349c4b8df360f043ad', 'admin')
ON DUPLICATE KEY UPDATE username=username;

-- 示例数据
INSERT INTO categories (name) VALUES
('IT设备'), ('办公耗材'), ('网络设备');

INSERT INTO devices (name, model, category_id) VALUES
('Dell笔记本', 'XPS 13', 1),
('ThinkPad', 'T14', 1),
('戴尔显示器', 'U2720Q', 1),
('HP打印机', 'LaserJet Pro', 2),
('华为路由器', 'AX3 Pro', 3);

INSERT INTO employees (name, age, email) VALUES
('张三', 28, 'zhangsan@company.com'),
('李四', 32, 'lisi@company.com'),
('王五', 25, 'wangwu@company.com');
