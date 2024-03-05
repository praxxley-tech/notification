import psycopg2
import os

conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)

cur = conn.cursor()

query = "SELECT id, report_id, created_at, details FROM all_reports;"

cur.execute(query)

rows = cur.fetchall()

for row in rows:
    report_id = row[1]  
    created_at = row[2]
    details = row[3]

    file_name = f"{report_id}.txt"

    if not os.path.exists(file_name):
        details_text = ""
        if isinstance(details, dict):
            for key, value in details.items():
                details_text += f"{key}: {value}\n"
        else:
            details_text = details

        output_data = (
            f"Report ID: {report_id}\n"
            f"Created At: {created_at}\n"
            f"Details:\n{details_text}"
        )

        with open(file_name, 'w') as file:
            file.write(output_data)
            print(f"Daten wurden in {file_name} gespeichert.")
    else:
        print(f"Datei {file_name} existiert bereits. Überspringe.")

cur.close()
conn.close()
