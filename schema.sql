-- Create Districts Table
CREATE TABLE IF NOT EXISTS districts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    district_name VARCHAR(255) NOT NULL UNIQUE
);

-- Create Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('Admin', 'Employee', 'Participant') NOT NULL,
    district_id INT,
    is_approved BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (district_id) REFERENCES districts(id) ON DELETE SET NULL
);

-- Create Modules Table
CREATE TABLE IF NOT EXISTS modules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    content TEXT
);

-- Create Assessments Table
CREATE TABLE IF NOT EXISTS assessments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    module_id INT NOT NULL,
    question TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_answer ENUM('A', 'B', 'C', 'D') NOT NULL,
    FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE
);

-- Create Results Table
CREATE TABLE IF NOT EXISTS results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    module_id INT NOT NULL,
    score INT NOT NULL,
    passed BOOLEAN DEFAULT FALSE,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE
);

-- Create Progress Table
CREATE TABLE IF NOT EXISTS progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    module_id INT NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_module (user_id, module_id)
);

-- Create Trophies Table
CREATE TABLE IF NOT EXISTS trophies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    achieved BOOLEAN DEFAULT FALSE,
    achieved_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_trophy (user_id)
);

-- Insert Default Districts
INSERT IGNORE INTO districts (district_name) VALUES 
('Ahmedabad'), ('Surat'), ('Vadodara'), ('Rajkot'), ('Bhavnagar'), ('Jamnagar'), ('Gandhinagar');

-- Insert Initial Admin (Password: admin123)
-- Note: In the application code, we will use werkzeug.security to hash passwords.
-- For the initial SQL, we'll use a pre-calculated hash (scrypt:32768:8:1$...)
INSERT IGNORE INTO users (name, email, password_hash, role, is_approved) 
VALUES ('Super Admin', 'admin@platform.com', 'pbkdf2:sha256:260000$Jdite173CH60VoLf$513f0aa85452f0907cf12b0f9a3f6c595c3fb81c538f3d087911f9f1ebdad7a6', 'Admin', TRUE);
-- Create Messages Table
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE
);
