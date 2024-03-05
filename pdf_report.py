from fpdf import FPDF
import glob
import os
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, 'CVE Report ' + datetime.now().strftime("%Y-%m-%d"), 0, align='C')
        self.ln(10)
        self.image(r'itpoint-removebg-preview.png', x=170, y=8, w=30)

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, title, 0, align='L')
        self.ln(10)

    def wrap_text(self, text, max_width=95):
        """Teilt den Text in mehrere Zeilen auf, wenn er länger als max_width ist."""
        if not text:
            return text
        wrapped_text = ""
        current_line = ""
        words = text.split()
        for word in words:
            if len(current_line + word) <= max_width:
                current_line += word + " "
            else:
                wrapped_text += current_line + "\n"
                current_line = word + " "
        wrapped_text += current_line
        return wrapped_text

    def chapter_body(self, body):
        wrapped_body = self.wrap_text(body)
        self.set_font('Helvetica', '', 12)
        self.multi_cell(0, 10, wrapped_body)
        self.ln()

def text_files_to_pdf(output_pdf, directory, log_file):
    pdf = PDF()
    pdf.add_page()

    text_files = glob.glob(os.path.join(directory, '*.txt'))

    processed_files = []
    if os.path.exists(log_file):
        with open(log_file, 'r') as file:
            processed_files = file.read().splitlines()

    new_files = [f for f in text_files if os.path.splitext(os.path.basename(f))[0] not in processed_files]

    for text_file in sorted(new_files):
        base_name = os.path.splitext(os.path.basename(text_file))[0]
        with open(text_file, 'r') as file:
            body = file.read()

        pdf.chapter_title(base_name)
        pdf.chapter_body(body)

        processed_files.append(base_name)

    if new_files:
        pdf.output(output_pdf)
        with open(log_file, 'w') as log:
            for name in processed_files:
                log.write(name + '\n')
        print(f"{output_pdf} wurde erfolgreich erstellt/aktualisiert mit {len(new_files)} neuen Datei(en).")
    else:
        print("Keine neuen Dateien zum Verarbeiten gefunden. PDF wurde nicht überschrieben.")

directory = r"reports"
output_pdf = 'cve_report.pdf'
log_file = 'processed_files.log'

text_files_to_pdf(output_pdf, directory, log_file)
