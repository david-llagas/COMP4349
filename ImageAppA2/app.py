from flask import Flask, request, render_template, redirect, url_for
import boto3
import os
import mysql.connector
from werkzeug.utils import secure_filename
from datetime import datetime

# --- Configuration ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'

# AWS S3 Config
S3_BUCKET = 'comp4349-images'  
S3_REGION = 'us-east-1'  

# RDS MySQL Config
DB_CONFIG = {
    'host': 'comp4349-db.c4ygpkkfjv3j.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'Bluelagoon9832#',
    'database': 'comp4349db'
}

# --- S3 Client ---
s3 = boto3.client('s3', region_name=S3_REGION)

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part", 400

        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400

        filename = secure_filename(file.filename)
        local_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(local_path)

        s3_key = f"images/{filename}"
        try:
            # Upload to S3
            s3.upload_file(local_path, S3_BUCKET, s3_key)

            # Store metadata in RDS
            save_to_db(filename, s3_key)

            return redirect(url_for('gallery'))
        except Exception as e:
            return f"Error uploading: {str(e)}", 500

    return render_template('upload.html')

@app.route('/gallery')
def gallery():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM images ORDER BY upload_time DESC")
        images = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('gallery.html', images=images, bucket=S3_BUCKET)
    except Exception as e:
        return f"Database error: {str(e)}", 500

# --- Helper function ---
def save_to_db(filename, s3_key):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    query = "INSERT INTO images (filename, s3_key) VALUES (%s, %s)"
    cursor.execute(query, (filename, s3_key))
    conn.commit()
    cursor.close()
    conn.close()

# --- Start App ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
