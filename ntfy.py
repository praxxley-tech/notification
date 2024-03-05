import os
import requests

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
directory = r"cve_reports"
sent_alarms_file = "sent_alarms.txt"
ntfy_url = os.getenv('BASE_NTFY_URL')

def read_sent_items():
    if os.path.exists(sent_alarms_file):
        with open(sent_alarms_file, 'r') as file:
            return file.read().splitlines()
    return []


def add_sent_item(item_id):
    with open(sent_alarms_file, 'a') as file:
        file.write(f"{item_id}\n")


def send_files():
    sent_items = read_sent_items()

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            item_id = filename[:-4]
            if item_id not in sent_items:
                file_path = os.path.join(directory, filename)
                try:
                    with open(file_path, 'r') as file:
                        file_content = file.read()

                    response = requests.put(
                        ntfy_url,
                        data=file_content,
                        headers={"Content-Type": "text/plain"}
                    )
                    if response.status_code == 200:
                        print(f"Successfully sent {filename}")
                        add_sent_item(item_id)
                    else:
                        print(f"Failed to send {filename}, Status Code: {response.status_code}")
                except Exception as e:
                    print(f"Exception occurred while sending {filename}: {e}")


if __name__ == "__main__":
    send_files()
