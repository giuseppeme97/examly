import random
from pathlib import Path
from word import Word
from source import Source
from template import Template
from config import config as cf
from utils import Utils


class Examly():
    def __init__(self, config, console=None) -> None:
        self.config = config
        self.source_loaded = None
        self.console = console if console else print
        self.console("Istanza di Examly creata.")


    def load_source(self) -> None:
        self.source = Source(self.config)
        if self.source.load_source():
            
            questions_log = self.source.check_questions()
            if len(questions_log) > 0:
                self.console("\nERRORE: Alcune domande presenti nella sorgente non sono complete.")
                self.console("Indici domande:")
                self.console(" ".join(map(str, questions_log)))
                self.source_loaded = False
            
            options_log = self.source.check_options_number()
            if len(options_log) > 0:
                self.console("\nERRORE: Alcune domande presenti nella sorgente non hanno un numero idoneo di opzioni.")
                self.console("Indici domande:")
                self.console(" ".join(map(str, options_log)))
                self.source_loaded = False
            
            orphans_log = self.source.check_orphan_questions()
            if len(orphans_log) > 0:
                self.console("\nERRORE: Alcune domande presenti nella sorgente non hanno alcune categorie assegnate.")
                self.console("Indici domande:")
                self.console(" ".join(map(str, orphans_log)))
                self.source_loaded = False

            solutions_log = self.source.check_solutions()
            if len(solutions_log) > 0:
                self.console("\nATTENZIONE: Alcune domande presenti nella sorgente non hanno specificata l'opzione corretta.")
                self.console("Indici domande:")
                self.console(" ".join(map(str, solutions_log)))

            if self.config["images_directory"]:
                images_log = self.source.check_images()
                if len(images_log["file_mancanti"]) > 0:
                    self.console("\nATTENZIONE: Alcune immagini presenti nella sorgente non sono state trovate.")
                    self.console("Immagini non trovate:")
                    self.console(" ".join(map(str, images_log["file_mancanti"])))
            
            self.console("Sorgente caricata correttamente.")
            self.source_loaded = True
        else:
            self.console("\nErrore nel caricamento della sorgente.")
            self.source_loaded = False

    
    def loaded_source(self) -> bool:
        return self.source_loaded
        

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
    

    def set_source_file(self, source_file: str) -> None:
        self.config["source_file"] = source_file


    def set_documents_directory(self, documents_directory: str) -> None:
        self.config["documents_directory"] = documents_directory


    def set_config(self, config: dict) -> None:
        self.config = config


    def set_console(self, console: callable) -> None:
        self.console = console


    def new_template(self) -> str:
        t = Template(self.config)
        template_path = t.save_tempale()
        if template_path:
            self.console("Nuovo template generato correttamente.")
        else:
            self.console("Errore nella generazione del template.")
        return template_path

        
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
    

    def write_exams_from_session(self, session: dict) -> None:
        Path(session["config"]["documents_directory"]).mkdir(parents=True, exist_ok=True)
        
        for document in session["documents"]:
            document_path = self.write_exam(document["sampled_questions"], document["document_number"], is_document_solution=False)
            self.console(f"\nGenerato {document_path} come esame.")

            if session["config"]["are_documents_exported_to_pdf"]:
                Utils.export_to_pdf(session["config"]["documents_directory"], document_path)

            if session["config"]["are_solutions_exported"]:
                solution_path = self.write_exam(document["sampled_questions"], document["document_number"], is_document_solution=True)
                self.console(f"Generato {solution_path} come esame.")
                
                if session["config"]["are_documents_exported_to_pdf"]:
                    Utils.export_to_pdf(session["config"]["documents_directory"], solution_path)
    

    def write_exams(self) -> dict:
        session = {
            "config": self.config,
            "documents": []
        }

        Path(self.config["documents_directory"]).mkdir(parents=True, exist_ok=True)

        if Utils.is_integer(self.config["exact_document_number"]):
            documents_iterator = range(self.config["exact_document_number"], self.config["exact_document_number"] + 1)
        else:
            documents_iterator = range(1, self.config["documents_number"] + 1)
        
        for document_number in documents_iterator:
            sampled_questions = self.sample_questions(self.source.get_questions())
            document = {
                "sampled_questions": sampled_questions,
                "document_number": document_number
            }
            document_path = self.write_exam(sampled_questions, document_number, is_document_solution=False)
            self.console(f"\nGenerato {document_path} come esame.")

            if self.config["are_documents_exported_to_pdf"]:
                Utils.export_to_pdf(self.config["documents_directory"], document_path)

            if self.config["are_solutions_exported"]:
                solution_path = self.write_exam(sampled_questions, document_number, is_document_solution=True)
                self.console(f"Generato {solution_path} come esame.")
                
                if self.config["are_documents_exported_to_pdf"]:
                    Utils.export_to_pdf(self.config["documents_directory"], solution_path)
            
            session["documents"].append(document)

        if self.config["are_documents_included_to_zip"]: 
            self.export_to_zip()

        if self.config["export_session"]:
            Utils.save_json(session)

        return session


    def check_soffice(self):
        pass
                    

    def export_to_zip(self) -> None:
        zip_filename = f"{self.config['zip_filename']}.zip"
        Utils.directory_to_zip(self.config['documents_directory'], zip_filename)

            

if __name__ == "__main__":
     examly = Examly(config=cf)
     examly.load_source()
     if examly.loaded_source():
         examly.write_exams()
        
