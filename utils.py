from datetime import datetime
import json
import subprocess
import zipfile
import os
import wx


class Utils:
    @staticmethod
    def is_integer(value):
        if isinstance(value, int): return True
        if isinstance(value, str):
            try:
                int(value)
                return True
            except ValueError:
                return False
        return False

    @staticmethod
    def save_json(documents_directory, session: dict) -> None:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(f"{documents_directory}/{now}.json", "w") as file:
            json.dump(session, file, indent=4)

    @staticmethod
    def load_json(session_file) -> dict:
        with open(session_file, "r") as file:
            return json.load(file)

    @staticmethod
    def check_soffice(soffice_path) -> bool:
        command = [soffice_path, "--headless","--convert-to", "pdf", "--outdir", ".", ".docx"]

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            return True
        except:
            return False

    @staticmethod
    def export_to_pdf(soffice_path, destination_directory, file_path) -> str:
        command = [soffice_path, "--headless", "--convert-to", "pdf", "--outdir", destination_directory, file_path]

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            return file_path.replace(".docx", ".pdf")
        except:
            return None

    @staticmethod
    def documents_to_zip(documents_directory, documents_list, zip_filename) -> str:
        zip_path = f"{documents_directory}/{zip_filename}"
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in os.listdir(documents_directory):
                document_path = os.path.join(documents_directory, file)
                if document_path in documents_list:
                    zipf.write(document_path, file)
                    os.remove(document_path)
        return zip_path

    @staticmethod
    def only_integer(event):
        key_code = event.GetKeyCode()
        if not (ord('0') <= key_code <= ord('9')) and key_code != wx.WXK_BACK:
            return
        event.Skip()

