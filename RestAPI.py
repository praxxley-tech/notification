import json
import os
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth


def log_processed(entry, log_file="processed_ids.log"):
    with open(log_file, 'a') as f:
        f.write(f"{entry}\n")


def is_processed(entry, log_file="processed_ids.log"):
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            if entry in f.read().splitlines():
                return True
    return False


username = os.getenv('API_USERNAME')
password = os.getenv('API_PASSWORD')
base_url = os.getenv('BASE_URL')

response = requests.get(f"{base_url}/reports", auth=HTTPBasicAuth(username, password))
reports = response.json()
print(reports)
print(response.headers['Content-Type'])
print(response.status_code)

with open('all_reports.txt', 'w', encoding='utf-8') as f:
    json.dump(reports, f, indent=4, sort_keys=True)

if reports:
    for report in reports:
        object_id = report['id']
        if not is_processed(object_id):
            detail_response = requests.get(f"{base_url}/reports/{object_id}", auth=HTTPBasicAuth(username, password))
            detailed_report = detail_response.json()

            with open('report.txt', 'a') as f:
                f.write(json.dumps(detailed_report, indent=4, sort_keys=True) + "\n")
            log_processed(object_id)

            if 'alerts' in detailed_report:
                for alert in detailed_report['alerts']:
                    cve_id = alert['cve']
                    if not is_processed(cve_id):
                        cve_response = requests.get(f"{base_url}/cve/{cve_id}", auth=HTTPBasicAuth(username, password))
                        if cve_response.status_code == 200:
                            cve_details = cve_response.json()

                            with open('cve.txt', 'a') as f:
                                f.write(json.dumps(cve_details, indent=4, sort_keys=True) + "\n")
                            log_processed(cve_id)
else:
    print("No reports found.")
