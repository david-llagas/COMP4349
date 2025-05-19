#!/bin/bash

# Configuration
DB_HOST="comp4349-db.c4ygpkkfjv3j.us-east-1.rds.amazonaws.com"
DB_USER="admin"
DB_PASS="Bluelagoon9832#"
DB_NAME="comp4349-db"

# Create database
echo "📦 Creating database (if not exists)..."
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"

# Create table
echo "📸 Creating 'images' table..."
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" <<EOF
CREATE TABLE IF NOT EXISTS images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    s3_key VARCHAR(512) NOT NULL,
    caption TEXT DEFAULT NULL,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
EOF

echo "✅ Database setup complete."
