from datetime import datetime
import json
import subprocess
import zipfile
import os

class Utils:
    @staticmethod
    def is_integer(value):
        if isinstance(value, int):
            return True
        if isinstance(value, str):
            try:
                int(value)
                return True
            except ValueError:
                return False
        return False
    

    @staticmethod
    def save_json(self, session: dict) -> None:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(f"{self.config['documents_directory']}/{now}.json", "w") as file:
            json.dump(session, file, indent=4)


    @staticmethod
    def load_json(self, session_file) -> dict:
        with open(session_file, "r") as file:
            return json.load(file)
        

    @staticmethod
    def export_to_pdf(self, destination_directory, file_path) -> bool:
        command = [self.config["soffice_path"], "--headless", "--convert-to", "pdf", "--outdir", destination_directory, file_path]
        
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            return True

        except subprocess.CalledProcessError:
            return False
        

    @staticmethod
    def directory_to_zip(documents_directory, zip_filename) -> str:
        zip_path = f"{documents_directory}/{zip_filename}"
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in os.listdir(documents_directory):
                document_path = os.path.join(documents_directory, file)
                zipf.write(document_path, file)    
                os.remove(document_path)    
        return zip_path
    

    