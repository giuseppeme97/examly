import random
from pathlib import Path
from word import Word
from source import Source
from template import *
from configs import Configuration
from utils import Utils


class Examly():
    def __init__(self, console: callable = None) -> None:
        self.source_validated: bool = None
        self.console: callable = console if console else print
        self.console("Istanza di Examly creata.")
        if not Utils.check_soffice(Configuration.get_soffice_path()):
            self.console("ATTENZIONE: Comando soffice non presente nell'ambiente di esecuzione.")

    def load_source(self) -> None:
        self.source = Source()
        if self.source.is_loaded():
            questions_log = self.source.check_questions()
            if len(questions_log) > 0:
                self.console("\nERRORE: Alcune domande presenti nella sorgente non sono complete.")
                self.console("Indici domande:")
                self.console(" ".join(map(str, questions_log)))
                self.source_validated = False
                return

            options_log = self.source.check_options_number()
            if len(options_log) > 0:
                self.console("\nERRORE: Alcune domande presenti nella sorgente non hanno un numero idoneo di opzioni.")
                self.console("Indici domande:")
                self.console(" ".join(map(str, options_log)))
                self.source_validated = False
                return

            orphans_log = self.source.check_orphan_questions()
            if len(orphans_log) > 0:
                self.console("\nERRORE: Alcune domande presenti nella sorgente non hanno alcuni filtri assegnati.")
                self.console("Indici domande:")
                self.console(" ".join(map(str, orphans_log)))
                self.source_validated = False
                return

            solutions_log = self.source.check_solutions()
            if len(solutions_log) > 0:
                self.console("\nATTENZIONE: Alcune domande presenti nella sorgente non hanno specificata l'opzione corretta.")
                self.console("Indici domande:")
                self.console(" ".join(map(str, solutions_log)))

            if Configuration.get_are_images_inserted():
                if Configuration.get_images_directory():
                    images_log = self.source.check_images()
                    if len(images_log["file_mancanti"]) > 0:
                        self.console("\nATTENZIONE: Alcune immagini presenti nella sorgente non sono state trovate.")
                        self.console("Immagini non trovate:")
                        self.console(" ".join(map(str, images_log["file_mancanti"])))

            self.console("Sorgente caricata correttamente.")
            self.source_validated = True
        else:
            self.console("\nErrore nel caricamento della sorgente.")
            self.source_validated = False

    def is_source_validated(self) -> bool:
        return self.source_validated
    
    def get_filters(self) -> dict:
        return self.source.get_filters()

    def get_rows(self) -> int:
        return self.source.get_rows()

    def set_source_file(self, source_file: str) -> None:
        Configuration.set_source_file(source_file)

    def set_documents_directory(self, documents_directory: str) -> None:
        Configuration.set_documents_directory(documents_directory)

    def set_console(self, console: callable) -> None:
        self.console = console

    def new_template(self) -> str:
        template_path = get_template()
        if template_path:
            self.console("Nuovo template generato correttamente.")
        else:
            self.console("Errore nella generazione del template.")
        return template_path

    def sample_questions(self, questions: list[dict]) -> list[dict]:
        if Configuration.get_are_questions_shuffled():
            random.shuffle(questions)

        if Configuration.get_are_options_shuffled():
            for question in questions:
                random.shuffle(question['options'])

        return questions[0: Configuration.get_questions_number()]
    
    def get_questions_cardinality(self) -> int:
        return len(self.source.get_questions())

    def write_exam(self, questions: list[dict], document_number: int, is_solution: bool) -> str:
        word = Word(questions, document_number, is_solution)
        return word.save()

    def write_exams(self, only_len=False) -> None:
        Path(Configuration.get_documents_directory()).mkdir(parents=True, exist_ok=True)
        documents_list = []
        print("Genero documenti...")

        for document_number in range(Configuration.get_start_number(), Configuration.get_start_number() + Configuration.get_documents_number()):
            sampled_questions = self.sample_questions(self.source.get_questions())
            
            if Configuration.get_are_raw_exported():
                raw = {
                    "document": f"{Configuration.get_document_filename()}_{document_number}",
                    "content": sampled_questions
                }
                Utils.save_raw(Configuration.get_documents_directory(), f"{Configuration.get_document_filename()}_{document_number}", raw)
            
            document_word_path = self.write_exam(sampled_questions, document_number, is_solution=False)
            documents_list.append(document_word_path)

            if Configuration.get_are_documents_exported_to_pdf():
                document_pdf_path = Utils.export_to_pdf(Configuration.get_soffice_path(), Configuration.get_documents_directory(), document_word_path)
                documents_list.append(document_pdf_path)

            if Configuration.get_are_solutions_exported():
                solution_word_path = self.write_exam(sampled_questions, document_number, is_solution=True)
                documents_list.append(solution_word_path)

                if Configuration.get_are_documents_exported_to_pdf():
                    solution_pdf_path = Utils.export_to_pdf(Configuration.get_soffice_path(), Configuration.get_documents_directory(), solution_word_path)
                    documents_list.append(solution_pdf_path)

        if Configuration.get_are_documents_included_to_zip():
            self.export_to_zip(documents_list)

        print("Documenti generati correttamente!")

    def export_to_zip(self, documents_list) -> None:
        zip_filename = f"{Configuration.get_zip_filename()}.zip"
        Utils.documents_to_zip(Configuration.get_documents_directory(), documents_list, zip_filename)


if __name__ == "__main__":
    examly = Examly()
    examly.load_source()

    if examly.is_source_validated():
        print(examly.get_questions_cardinality())
