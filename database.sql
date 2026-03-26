-- Create Database
CREATE DATABASE  carbon_tracker;

USE carbon_tracker;

-- ================= USERS TABLE =================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- ================= EMISSIONS TABLE =================
CREATE TABLE emissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    location VARCHAR(100),
    travel FLOAT DEFAULT 0,
    electricity FLOAT DEFAULT 0,
    food FLOAT DEFAULT 0,
    total FLOAT,
    eco_score VARCHAR(20),
    date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

