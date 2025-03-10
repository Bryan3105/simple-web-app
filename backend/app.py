from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import psycopg2  # PostgreSQL library
import os
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Database connection settings (using environment variables for security)
DB_HOST = os.environ.get("DB_HOST", "localhost") #localhost for local testing
DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
DB_PORT = os.environ.get("DB_PORT", "5432")  # Default PostgreSQL port
try:
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)
    cur = conn.cursor()
    #Test Connection
    cur.execute("SELECT 1")
    result = cur.fetchone()
    print("Database connection successful:", result)

except psycopg2.Error as e:
   logging.error("Database connection error: %s", e)
   # Handle the error gracefully - for example, exit the application
   raise SystemExit("Failed to connect to database. Exiting.")
# API endpoint to process data
@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        number1 = float(data['number1'])
        number2 = float(data['number2'])

        sum_result = number1 + number2

        # Insert data into the database
        cur = conn.cursor() # Get a new cursor
        cur.execute("INSERT INTO numbers (number1, number2, sum) VALUES (%s, %s, %s)", (number1, number2, sum_result))
        conn.commit()
        logging.info("Data inserted into database: number1=%s, number2=%s, sum=%s", number1, number2, sum_result)
        return jsonify({'sum': sum_result})

    except Exception as e:
        logging.error("Error processing request: %s", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
