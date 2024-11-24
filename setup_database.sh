#!/bin/bash

# Database credentials
DB_ROOT_USER="root"
DB_ROOT_PASSWORD="rootpassword"
DB_USER="deviant"
DB_PASSWORD="deviant123"
DB_NAME="link_shortener"
DB_HOST="172.17.0.2"  # Replace with the actual IP address of your MySQL container

# SQL commands to create the database and table
SQL_COMMANDS="
CREATE DATABASE IF NOT EXISTS $DB_NAME;
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'%';
USE $DB_NAME;
CREATE TABLE IF NOT EXISTS urls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    original_url TEXT NOT NULL,
    short_key VARCHAR(10) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL,
    click_count INT DEFAULT 0
);
FLUSH PRIVILEGES;
"

# Execute the SQL commands
mysql -u$DB_ROOT_USER -p$DB_ROOT_PASSWORD -h$DB_HOST -e "$SQL_COMMANDS"

echo "Database '$DB_NAME' and table 'urls' created successfully."