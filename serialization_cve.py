import psycopg2
import os
import json

conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

cur = conn.cursor()

query = "SELECT id, cve_id, created_at, cvss_v3, cwes, raw_nvd_data FROM cve_details;"

cur.execute(query)

rows = cur.fetchall()

cve_reports_folder = 'cve_reports'
if not os.path.exists(cve_reports_folder):
    os.makedirs(cve_reports_folder)

for row in rows:
    cve_id, created_at, cvss_v3, cwes, raw_nvd_data = row[1:]

    file_name = f"{cve_id}.txt"
    file_path_in_reports = os.path.join(cve_reports_folder, file_name)
    file_path_in_root = os.path.join('reports', file_name)

    if isinstance(raw_nvd_data, str):
        raw_nvd_data = json.loads(raw_nvd_data)

    published_date = raw_nvd_data.get('published', 'N/A')

    references = raw_nvd_data.get('references', [])
    references_text = ', '.join([ref.get('url', 'N/A') for ref in references])

    tags_list = [tag for ref in references for tag in ref.get('tags', [])]
    tags_text = ', '.join(tags_list)

    source = references[0].get('source', 'N/A') if references else 'N/A'

    nvd_data_text = (f"Published: {published_date}\n"
                     f"References: {references_text}\n"
                     f"Tags: {tags_text}\n"
                     f"Source: {source}\n")

    output_data = (
        f"CVE ID: {cve_id}\n"
        f"Created At: {created_at}\n"
        f"CVSS v3: {cvss_v3}\n"
        f"CWES: {cwes}\n"
        f"Raw NVD Data:\n{nvd_data_text}"
    )

    def write_data(path, data):
        with open(path, 'w') as file:
            file.write(data)
            print(f"Daten wurden in {path} gespeichert.")

    if not os.path.exists(file_path_in_reports):
        write_data(file_path_in_reports, output_data)

    if not os.path.exists(file_path_in_root):
        write_data(file_path_in_root, output_data)

cur.close()
conn.close()
