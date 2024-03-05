import os
import json
import psycopg2
from psycopg2.extras import execute_batch

# Datenbankverbindung
conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Cursor erstellen
cur = conn.cursor()

# Tabellen erstellen
cur.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id SERIAL PRIMARY KEY,
        report_id TEXT UNIQUE,
        report_content JSONB
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS all_reports (
        id SERIAL PRIMARY KEY,
        report_id TEXT UNIQUE,
        created_at TIMESTAMP,
        details TEXT[]
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS cve_details (
        id SERIAL PRIMARY KEY,
        cve_id TEXT UNIQUE,
        created_at TIMESTAMP,
        cvss_v3 FLOAT,
        cwes TEXT[],
        raw_nvd_data JSONB,
        summary TEXT,
        updated_at TIMESTAMP,
        vendors TEXT[]
    )
""")

# Verarbeitung von report.txt
with open(r'report.txt', 'r') as file:
    data = json.load(file)
    for alert in data['alerts']:
        cur.execute("""
            INSERT INTO reports (report_id, report_content) 
            VALUES (%s, %s) 
            ON CONFLICT (report_id) DO NOTHING
        """, (alert['id'], json.dumps(alert)))

# Verarbeitung von all_reports.txt
with open(r'all_reports.txt', 'r') as file:
    data = json.load(file)
    for report in data:
        cur.execute("""
            INSERT INTO all_reports (report_id, created_at, details) 
            VALUES (%s, %s, %s) 
            ON CONFLICT (report_id) DO NOTHING
        """, (report['id'], report['created_at'], report['details']))

with open(r'cve.txt', 'r', encoding='utf-8') as file:
    cve_data = json.load(file)

    cve_id = cve_data['id']
    created_at = cve_data['created_at']
    cvss_v3 = cve_data['cvss']['v3'] if 'v3' in cve_data['cvss'] else None
    cwes = cve_data['cwes']
    raw_nvd_data = json.dumps(cve_data['raw_nvd_data'])
    summary = cve_data['summary']
    updated_at = cve_data['updated_at']
    vendors = list(cve_data['vendors'].keys())

    cur.execute("""
        INSERT INTO cve_details (cve_id, created_at, cvss_v3, cwes, raw_nvd_data, summary, updated_at, vendors)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (cve_id) DO NOTHING
    """, (cve_id, created_at, cvss_v3, cwes, raw_nvd_data, summary, updated_at, vendors))

# Commit und Cleanup
conn.commit()
cur.close()
conn.close()
