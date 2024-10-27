import random
import os
import zipfile
from pathlib import Path
from word import Word
from source import Source
from template import Template
import json
import sys
from config import config


class Examly():
    def __init__(self) -> None:
        self.config = self.get_config()


    def show_menu(self) -> None:
        pass


    def start(self) -> None:
        self.source = Source(self.config)
        if self.source.load_source():
            print("Sorgente caricata correttamente.")
            questions = self.source.get_questions()
            print(f"Filtrate {len(questions)} domande.")
            self.write_exams(questions)
            if self.config["are_documents_included_to_zip"]: self.zip_exams()
        else:
            print("Errore nel caricamento della risorsa.")


    def set_config(self, config: dict) -> None:
        self.config = config


    def load_config(self, config_path) -> dict:
        with open(config_path) as file:
            return json.load(file)
        

    def get_config(self) -> dict:
        return config


    def save_template(self) -> None:
        t = Template(self.config)
        t.save_tempale()
        

    def sample_questions(self, questions: list[dict]) -> list[dict]:
        if self.config['are_questions_shuffled']:
            random.shuffle(questions)
        
        if self.config['are_options_shuffled']:
            for question in questions:
                random.shuffle(question['options'])
        
        return questions[0: self.config['questions_number']]
    

    def write_exam(self, questions: list[dict], document_number: int, is_document_solution: bool) -> None:
        w = Word(self.config, questions, document_number, is_document_solution)
        w.save_document(self.config["documents_directory"], self.config["document_filename"], document_number)
    

    def write_exams(self, filtered_questions: list[dict]) -> None:
        Path(self.config["documents_directory"]).mkdir(parents=True, exist_ok=True)
        
        for document_number in range(1, self.config["documents_number"] + 1):
            sampled_questions = self.sample_questions(filtered_questions)
            self.write_exam(sampled_questions, document_number, is_document_solution=False)

            if self.config["are_solutions_exported"]:
                self.write_exam(sampled_questions, document_number, is_document_solution=True)
            
            print(f"Esame {document_number} generato!")


    def zip_exams(self) -> None:
        zip_filename = f"{self.config['zip_filename']}.zip"
        with zipfile.ZipFile(f"{self.config['documents_directory']}/{zip_filename}", 'w') as zipf:
            for file in os.listdir(self.config["documents_directory"]):
                if file.lower().endswith('.docx'):
                    docx_file_path = os.path.join(self.config["documents_directory"], file)
                    zipf.write(docx_file_path, file)
                    os.remove(docx_file_path)



if __name__ == "__main__":
     e = Examly()
     e.start()
        
