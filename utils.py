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
        command = [soffice_path, "--headless", "--convert-to", "pdf", "--outdir", ".", ".docx"]
        
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            return True

        except:
            return False
        

    @staticmethod
    def export_to_pdf(soffice_path, destination_directory, file_path) -> bool:
        command = [soffice_path, "--headless", "--convert-to", "pdf", "--outdir", destination_directory, file_path]
        
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            return True

        except:
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
    

    def get_params() -> tuple[dict]:
        filters = {
            "subjects": {
                "label": "Materie:",
                "items": []
            },
            "classrooms": {
                "label": "Classi:",
                "items": []
            },
            "periods": {
                "label": "Periodi:",
                "items": []
            },
            "sectors": {
                "label": "Settori:",
                "items": []
            },
        }

        options = {
            "are_pages_numbered": {
                "label": "Pagine numerate",
                "reference": None,
                "default": None
            },
            "are_documents_numbered": {
                "label": "Documenti numerati",
                "reference": None,
                "default": None
            },
            "are_questions_numbered": {
                "label": "Domande numerate",
                "reference": None,
                "default": None
            },
            "are_questions_shuffled": {
                "label": "Domande mescolate",
                "reference": None,
                "default": None
            },
            "are_options_shuffled": {
                "label": "Opzioni mescolate",
                "reference": None,
                "default": None
            },
            "are_solutions_exported": {
                "label": "Esporta correttori",
                "reference": None,
                "default": None
            },
            "are_questions_single_included": {
                "label": "Inclusione singola",
                "reference": None,
                "default": None
            },
            "are_documents_exported_to_pdf": {
                "label": "Esporta in PDF",
                "reference": None,
                "default": None
            },
            "are_documents_included_to_zip": {
                "label": "Includi in ZIP",
                "reference": None,
                "default": None
            },
            "export_session": {
                "label": "Esporta sessione",
                "reference": None,
                "default": None
            }
        }

        return filters, options


    

    