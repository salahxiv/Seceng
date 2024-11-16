from flask import Flask, request, jsonify
import requests
import sqlite3

app = Flask(__name__)

# Database setup
conn = sqlite3.connect('example.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, info TEXT)''')
conn.commit()

# Unrestricted Resource Consumption - Example
@app.route('/calculate', methods=['GET'])
def calculate():
    n = int(request.args.get('n', '1000000'))  # Allows users to set a very high value
    result = 0
    for i in range(n):
        result += i
    return jsonify({'result': result})

# Server Side Request Forgery (SSRF) - Example
@app.route('/fetchData', methods=['POST'])
def fetch_data():
    url = request.json.get('url')
    try:
        response = requests.get(url)  # No validation of URL, allowing internal network access
        return jsonify({'content': response.text})
    except requests.RequestException as e:
        return str(e), 400

# Security Misconfiguration - Example
@app.route('/debug', methods=['GET'])
def debug():
    return "Debug mode is on!", 200  # Indicates that the application might be running in debug mode

# Unsafe Consumption of APIs - Example
@app.route('/importData', methods=['POST'])
def import_data():
    data = request.json.get('data')
    try:
        # Directly execute user input, making it vulnerable to SQL Injection
        query = f"INSERT INTO data (info) VALUES ('{data}')"
        c.executescript(query)  # Using executescript to allow multiple SQL statements, making it vulnerable to SQL Injection
        conn.commit()
        return "Data inserted!", 200
    except sqlite3.OperationalError as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Running in debug mode, which is a security risk