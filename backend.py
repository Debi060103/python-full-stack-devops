from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

db_config = {
    'host': 'database-1.chewiacy0zhj.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'database1',
    'database': 'dev'  # or your DB name
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route("/insert", methods=["POST"])
def insert_user():
    try:
        data = request.json
        print("Received:", data)  # Debug
        name = data.get("name")
        email = data.get("email")

        if not name or not email:
            return jsonify({"message": "Missing name or email"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        conn.close()

        return jsonify({"message": "User inserted successfully"}), 201
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"message": "Insert failed", "error": str(e)}), 500

@app.route("/users", methods=["GET"])
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
        return jsonify(users), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"message": "Failed to fetch users", "error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)