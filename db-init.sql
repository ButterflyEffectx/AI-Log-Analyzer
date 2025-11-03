CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS login_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user VARCHAR(50),
    ip_address VARCHAR(45),
    status ENUM('success','failed','blocked'),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ตัวอย่าง user admin
INSERT INTO users (username, password_hash) VALUES 
('admin', '$2b$10$L4iA8hTaaZf38P30TH8tAefojlFXGDb7W5Eo9X8toQTHOo7Oxf/oO'); 
-- แทนที่ hash ด้วย bcrypt ของ 'admin'
