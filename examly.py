import random
import os
import zipfile
from pathlib import Path
from word import Word
from source import Source
from template import Template
from config import config as cf
import subprocess


class Examly():
    def __init__(self, config, console=None) -> None:
        self.config = config
        if not console:
            self.console = print


    def loaded_source(self) -> bool:
        self.source = Source(self.config)
        if self.source.load_source():
            self.console("Sorgente caricata correttamente.")

            questions_log = self.source.check_questions()
            if len(questions_log) > 0:
                self.console("\nERRORE: Alcune domande presenti nella sorgente non sono complete.")
                self.console("Indici domande:")
                self.console(questions_log)
                return False
            
            options_log = self.source.check_options_number()
            if len(options_log) > 0:
                self.console("\nERRORE: Alcune domande presenti nella sorgente non hanno un numero idoneo di opzioni.")
                self.console("Indici domande:")
                self.console(options_log)
                return False
            
            orphans_log = self.source.check_orphan_questions()
            if len(orphans_log) > 0:
                self.console("\nERRORE: Alcune domande presenti nella sorgente non hanno alcune categorie assegnate.")
                self.console("Indici domande:")
                self.console(orphans_log)
                return False

            solutions_log = self.source.check_solutions()
            if len(solutions_log) > 0:
                self.console("\nATTENZIONE: Alcune domande presenti nella sorgente non hanno specificata l'opzione corretta.")
                self.console("Indici domande:")
                self.console(solutions_log)

            images_log = self.source.check_images()
            if len(images_log["file_mancanti"]) > 0:
                self.console("\nATTENZIONE: Alcune immagini presenti nella sorgente non sono state trovate.")
                self.console("Indici domande:")
                self.console(images_log["file_mancanti"])
            
            return True
        else:
            self.console("\nErrore nel caricamento della sorgente.")
            return False
        

    def get_subjects(self) -> list[str]:
        return self.source.get_subjects()


    def get_classrooms(self) -> list[int]:
        return self.source.get_classrooms()
    

    def get_sectors(self) -> list[str]:
        return self.source.get_sectors()
    

    def get_periods(self) -> list[str]:
        return self.source.get_periods()


    def get_rows(self) -> int:
        return self.source.get_rows()


    def set_config(self, config: dict) -> None:
        self.config = config


    def new_template(self) -> None:
        t = Template(self.config)
        if t.save_tempale():
            self.console("Nuovo template generato correttamente.")
        else:
            self.console("Errore nella generazione del template.")
        

    def sample_questions(self, questions: list[dict]) -> list[dict]:
        if self.config['are_questions_shuffled']:
            random.shuffle(questions)
        
        if self.config['are_options_shuffled']:
            for question in questions:
                random.shuffle(question['options'])
        
        return questions[0: self.config['questions_number']]
    

    def write_exam(self, questions: list[dict], document_number: int, is_document_solution: bool) -> str:
        w = Word(self.config, questions, document_number, is_document_solution)
        return w.save_document(self.config["documents_directory"], self.config["document_filename"], document_number)
    

    def write_exams(self, filtered_questions: list[dict]) -> None:
        Path(self.config["documents_directory"]).mkdir(parents=True, exist_ok=True)
        
        for document_number in range(1, self.config["documents_number"] + 1):
            sampled_questions = self.sample_questions(filtered_questions)
            document_path = self.write_exam(sampled_questions, document_number, is_document_solution=False)
            self.console(f"\nGenerato {document_path} come esame.")

            if self.config["are_documents_exported_to_pdf"]:
                self.export_to_pdf(self.config["documents_directory"], document_path)

            if self.config["are_solutions_exported"]:
                solution_path = self.write_exam(sampled_questions, document_number, is_document_solution=True)
                self.console(f"Generato {solution_path} come esame.")
                
                if self.config["are_documents_exported_to_pdf"]:
                    self.export_to_pdf(self.config["documents_directory"], solution_path)
                    
            
    def export_to_pdf(self, destination_directory, file_path) -> None:
        comando = [self.config["soffice_path"], "--headless", "--convert-to", "pdf", "--outdir", destination_directory, file_path]
        
        try:
            subprocess.run(comando, check=True, capture_output=True, text=True)
            self.console(f"Convertito {file_path} in PDF.")

        except subprocess.CalledProcessError:
            self.console(f"Errore nella conversione di {file_path}!")


    def export_to_zip(self) -> None:
        zip_filename = f"{self.config['zip_filename']}.zip"
        with zipfile.ZipFile(f"{self.config['documents_directory']}/{zip_filename}", 'w') as zipf:
            for file in os.listdir(self.config["documents_directory"]):
                if file.lower().endswith('.docx') or file.lower().endswith('.pdf'):
                    document_path = os.path.join(self.config["documents_directory"], file)
                    zipf.write(document_path, file)    
                    os.remove(document_path)


    def run(self) -> None:
        if self.loaded_source():
            questions, _ = self.source.get_questions()
            self.write_exams(questions)
            if self.config["are_documents_included_to_zip"]: 
                self.export_to_zip()


if __name__ == "__main__":
     examly = Examly(config=cf)
     examly.run()
        
