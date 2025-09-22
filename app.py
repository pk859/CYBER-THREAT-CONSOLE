from flask import Flask, request, jsonify
from flask_cors import CORS
import mariadb # <-- EDITED: Changed the import
import pandas as pd
import requests
import subprocess
import sys
from datetime import datetime

# --- Configuration ---
SOAR_RISK_THRESHOLD = 20

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'abcd1234',
    'database': 'cyber_hackathon'
}

# --- EDITED: Updated the connection function for MariaDB ---
def get_db_connection():
    try:
        # Use mariadb.connect instead of mysql.connector.connect
        conn = mariadb.connect(**db_config)
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

app = Flask(__name__)
CORS(app)

# --- Predictive Risk Scoring Function ---
def calculate_predictive_risk_score(base_severity, criticality_level, ip_address, country, cursor):
    risk_score = base_severity * criticality_level
    print(f"Base risk score: {risk_score}")

    current_hour = datetime.now().hour
    if not (6 < current_hour < 22):
        risk_score += 3
        print(f"+3 risk for off-hours attack. New score: {risk_score}")

    country_watchlist = ["Russia", "China", "North Korea", "Iran"]
    if country in country_watchlist:
        risk_score += 5
        print(f"+5 risk for watchlist country ({country}). New score: {risk_score}")

    if ip_address:
        try:
            cursor.execute("SELECT COUNT(*) as count FROM incidents WHERE ip_address = ?", (ip_address,)) # EDITED: Use '?' for placeholders
            result = cursor.fetchone()
            if result and result[0] > 0:
                risk_score += result[0] * 2
                print(f"+{result[0] * 2} risk for repeat offender. Final score: {risk_score}")
        except Exception as e:
            print(f"Could not check IP history: {e}")
    return risk_score

@app.route('/incidents', methods=['POST'])
def add_incident():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor() # EDITED: No 'dictionary=True' needed initially

        ip_address = data.get('ip_address')
        country, city, lat, lon = 'N/A', 'N/A', None, None
        if ip_address:
            try:
                geo_response = requests.get(f'http://ip-api.com/json/{ip_address}?fields=status,country,city,lat,lon')
                if geo_response.status_code == 200:
                    geo_data = geo_response.json()
                    if geo_data['status'] == 'success':
                        country = geo_data.get('country', 'N/A')
                        city = geo_data.get('city', 'N/A')
                        lat = geo_data.get('lat')
                        lon = geo_data.get('lon')
            except requests.RequestException as e:
                print(f"Geolocation API failed: {e}")
                pass

        cursor.execute("SELECT base_severity FROM incident_types WHERE id = ?", (data['incident_type_id'],)) # EDITED: Use '?'
        incident_type_result = cursor.fetchone()
        cursor.execute("SELECT criticality_level FROM systems WHERE id = ?", (data['system_id'],)) # EDITED: Use '?'
        system_result = cursor.fetchone()

        if not incident_type_result or not system_result:
            return jsonify({"error": "Invalid system_id or incident_type_id"}), 400

        incident_type_severity = incident_type_result[0]
        system_criticality = system_result[0]

        risk_score = calculate_predictive_risk_score(
            incident_type_severity, 
            system_criticality,
            ip_address,
            country,
            cursor
        )

        if risk_score >= SOAR_RISK_THRESHOLD and ip_address:
            print(f"CRITICAL RISK DETECTED! Triggering automated block for IP: {ip_address}")
            subprocess.Popen([sys.executable, "block_ip.py", ip_address])

        sql = """INSERT INTO incidents (title, description, system_id, incident_type_id, risk_score, ip_address, country, city, latitude, longitude)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""" # EDITED: Use '?'
        values = (data['title'], data['description'], data['system_id'], data['incident_type_id'], risk_score, ip_address, country, city, lat, lon)
        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()
        return jsonify({"message": "Incident logged successfully!", "risk_score": risk_score}), 201

    except Exception as e:
        print(f"An error occurred in add_incident: {e}") 
        return jsonify({"error": str(e)}), 500

@app.route('/incidents', methods=['GET'])
def get_incidents():
    try:
        conn = get_db_connection()
        query = """
            SELECT i.id, i.title, i.status, i.risk_score, i.reported_at, 
                   s.name as system_name, it.name as incident_type,
                   i.ip_address, i.country, i.city, i.latitude, i.longitude
            FROM incidents i
            JOIN systems s ON i.system_id = s.id
            JOIN incident_types it ON i.incident_type_id = it.id
            ORDER BY i.reported_at DESC;
        """
        df = pd.read_sql(query, conn)
        conn.close()
        df['reported_at'] = df['reported_at'].astype(str)
        df.fillna('N/A', inplace=True)
        return df.to_json(orient="records"), 200
    except Exception as e:
        print(f"An error occurred in get_incidents: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)