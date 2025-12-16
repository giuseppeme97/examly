import random
from pathlib import Path
from word import Word
from source import Source
from template import *
from configs import Configuration
from utils import Utils


class Examly():
    def __init__(self, console) -> None:
        self.console = console or print
        self.ready = False
        self.console("🚀 Istanza di Examly creata.")
        
    def connect_source(self, web_mode: bool, source: str) -> None:
        Configuration.set_is_web_mode(web_mode)
        if Configuration.get_is_web_mode():
            Configuration.set_source_collection(source)
        else:
            Configuration.set_source_file(source)

        self.source = Source()
        
        if self.source.load():
            self.ready = True
            self.console("✅ Sorgente caricata e validata.")
        else:
            self.ready = False
            self.console("❌ Errore nel caricamento o nella validazione della sorgente.")
            for log in self.source.get_logs():
                self.console(f"💬 {log["message"]} Righe: {log["result"]}")
            

    def is_ready(self) -> bool:
        return self.ready

    def get_rows(self) -> int:
        return self.source.get_rows()

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

    def write_exams(self) -> None:
        Path(Configuration.get_documents_directory()).mkdir(parents=True, exist_ok=True)
        documents_list = []

        for document_number in range(Configuration.get_start_number(), Configuration.get_start_number() + Configuration.get_documents_number()):
            sampled_questions = self.sample_questions(self.source.get_questions())
            
            document_word_path = self.write_exam(sampled_questions, document_number, is_solution=False)
            documents_list.append(document_word_path)

            if Configuration.get_are_raw_exported():
                raw_document = {
                    "document": f"{Configuration.get_document_filename()}_{document_number}",
                    "content": sampled_questions
                }
                Utils.save_raw(Configuration.get_documents_directory(), f"{Configuration.get_document_filename()}_{document_number}", raw_document)

            print(f"✅ Generato documento {document_number}.")

            if Configuration.get_are_solutions_exported():
                solution_word_path = self.write_exam(sampled_questions, document_number, is_solution=True)
                documents_list.append(solution_word_path)

                if Configuration.get_are_raw_exported():
                    raw_solution = {
                        "document": document_number,
                        "content": [{
                            "id_question": index,
                            "correct_option": next(i for i, x in enumerate(question["options"]) if x["correct"]) + 1
                        } for index, question in enumerate(sampled_questions, start=1)]
                    }   
                    Utils.save_raw(Configuration.get_documents_directory(), f"{Configuration.get_document_filename()}_{document_number}_solutions", raw_solution)


        if Configuration.get_are_documents_included_to_zip():
            self.export_to_zip(documents_list)

        print("FINE!")

    def export_to_zip(self, documents_list) -> None:
        zip_filename = f"{Configuration.get_zip_filename()}.zip"
        Utils.documents_to_zip(
            Configuration.get_documents_directory(), documents_list, zip_filename)

    def set_documents_directory(self, value) -> None:
        Configuration.set_documents_directory(value)

    def set_images_directory(self, value) -> None:
        Configuration.set_images_directory(value)

    def set_template_directory(self, value) -> None:
        Configuration.set_template_directory(value)

    def set_template_filename(self, value) -> None:
        Configuration.set_template_filename(value)

    def set_document_filename(self, value) -> None:
        Configuration.set_document_filename(value)

    def set_zip_filename(self, value) -> None:
        Configuration.set_zip_filename(value)

    def get_filters(self) -> dict:
        if self.source.is_validated():
            return self.source.get_filters()
        else: 
            return {}

    def set_filters(self, filters: dict) -> None:
        for key, value in filters.items():
            Configuration.set_filter_values(key, value)

    def set_document_title(self, value) -> None:
        Configuration.set_document_title(value)

    def set_document_subtitle(self, value) -> None:
        Configuration.set_document_subtitle(value)

    def set_document_header(self, value) -> None:
        Configuration.set_document_header(value)

    def set_documents_number(self, value) -> None:
        Configuration.set_documents_number(value)

    def set_start_number(self, value) -> None:
        Configuration.set_start_number(value)

    def set_questions_number(self, value) -> None:
        Configuration.set_questions_number(value)

    def set_is_header_included(self, value) -> None:
        Configuration.set_is_header_included(value)

    def set_is_subtitle_included(self, value) -> None:
        Configuration.set_is_subtitle_included(value)

    def set_are_pages_numbered(self, value) -> None:
        Configuration.set_are_pages_numbered(value)

    def set_are_documents_numbered(self, value) -> None:
        Configuration.set_are_documents_numbered(value)

    def set_are_questions_numbered(self, value) -> None:
        Configuration.set_are_questions_numbered(value)

    def set_are_questions_shuffled(self, value) -> None:
        Configuration.set_are_questions_shuffled(value)

    def set_are_options_shuffled(self, value) -> None:
        Configuration.set_are_options_shuffled(value)

    def set_are_images_inserted(self, value) -> None:
        Configuration.set_are_images_inserted(value)

    def set_are_solutions_exported(self, value) -> None:
        Configuration.set_are_solutions_exported(value)

    def set_are_raw_exported(self, value) -> None:
        Configuration.set_are_raw_exported(value)

    def set_are_questions_single_included(self, value) -> None:
        Configuration.set_are_questions_single_included(value)

    def set_are_documents_included_to_zip(self, value) -> None:
        Configuration.set_are_documents_included_to_zip(value)

    def set_exact_document_number(self, value) -> None:
        Configuration.set_exact_document_number(value)

    def set_font(self, value) -> None:
        Configuration.set_font(value)

    def set_language(self, value) -> None:
        Configuration.set_language(value)

    def set_title_size(self, value) -> None:
        Configuration.set_title_size(value)

    def set_subtitle_size(self, value) -> None:
        Configuration.set_subtitle_size(value)

    def set_questions_size(self, value) -> None:
        Configuration.set_questions_size(value)

    def set_images_size(self, value) -> None:
        Configuration.set_images_size(value)

    def set_columns_number(self, value) -> None:
        Configuration.set_columns_number(value)

    def set_left_margin(self, value) -> None:
        Configuration.set_left_margin(value)

    def set_right_margin(self, value) -> None:
        Configuration.set_right_margin(value)


if __name__ == "__main__":
    examly = Examly()
    examly.connect_source(web_mode=False, source="inf.xlsx")
    examly.set_documents_directory("/Users/giuseppe/Documents/examly/output")
    examly.set_images_directory("/Users/giuseppe/Documents/examly/images")
    examly.set_template_directory("/Users/giuseppe/Documents/examly/template")
    examly.set_document_filename("esame")
    examly.set_zip_filename("compito")
    examly.set_filters({
        "MATERIA": ["INFORMATICA"],
        "CLASSE": [],
        "PERIODO": [],
        "SETTORE": []
    })
    examly.set_document_title("Prova comune di Informatica - A.S. 2025/2026 - Classi 3F 3G 3H")
    examly.set_document_subtitle("Segnare solo una delle quattro opzioni per ciascuna domanda.")
    examly.set_documents_number(3)
    examly.set_start_number(1)
    examly.set_questions_number(36)
    examly.set_is_header_included(True)
    examly.set_is_subtitle_included(True)
    examly.set_are_pages_numbered(True)
    examly.set_are_documents_numbered(True)
    examly.set_are_questions_numbered(True)
    examly.set_are_questions_shuffled(True)
    examly.set_are_options_shuffled(True)
    examly.set_are_images_inserted(False)
    examly.set_are_solutions_exported(True)
    examly.set_are_raw_exported(False)
    examly.set_are_questions_single_included(True)
    examly.set_are_documents_included_to_zip(False)
    examly.set_exact_document_number(False)
    examly.set_font("Liberation Sans")
    examly.set_language("it-IT")
    examly.set_title_size(15)
    examly.set_subtitle_size(12)
    examly.set_questions_size(11)
    examly.set_images_size(3.5)
    examly.set_columns_number(2)
    examly.set_left_margin(1)
    examly.set_right_margin(1)

    if examly.is_ready():
        examly.write_exams()
        # print("Domande filtrate:", examly.get_questions_cardinality())
