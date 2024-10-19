import pandas as pd
import random
import os
import zipfile
import openpyxl
from openpyxl.styles import Side, Border
from pathlib import Path
from word import Word


class ExamsGenerator():
    def __init__(self, config: dict) -> None:
        self.config = config


    # Starts automatically the generation of the exams
    def start(self):
        if self.load_source():
            self.generate()
        else:
            print("Errore nel caricamento della sorgente delle domande.")

    
    # Updates the loaded configurations
    def set_config(self, config: dict) -> None:
        self.config = config


    # Loads the source of all questions from various types of files (.xlsx, .csv)
    # TODO: catch exceptions
    def load_source(self) -> bool:
        _, ext = os.path.splitext(self.config["source_path"])
            
        if ext in self.config["supported_excel_formats"]:
            self.df = pd.read_excel(self.config["source_path"])
        elif ext in self.config["supported_table_formats"]:
            self.df = pd.read_csv(self.config["source_path"],  sep=";")
        else:
            return False
        
        print("Sorgente caricata.\n")
        return True


    # Gets the list of all subjects inside the source of questions
    def get_subjects(self) -> list:
        return sorted(pd.Series(self.df[self.config["subject_denomination"]].unique()).dropna().tolist()) 


    # Gets the list of all different classrooms inside the source of questions
    def get_classrooms(self) -> list:
        return sorted(list(map(int, pd.Series(self.df[self.config["classroom_denomination"]].unique()).dropna().tolist())))


    # Gets the number of questions inside the source
    def get_rows(self) -> int:
        return self.df.shape[0]


    # Generate a new .xlsx file to be used for a new source of questions
    def get_template(self) -> str:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        headers = [
            f"{self.config['subject_denomination']}", 
            f"{self.config['classroom_denomination']}",
            f"{self.config['era_denomination']}",
            f"{self.config['sector_denomination']}", 
            f"{self.config['include_denomination']}", 
            f"{self.config['question_denomination']}", 
            f"{self.config['solution_denomination']}", 
            f"{self.config['option_denomination']}_1",
            f"{self.config['option_denomination']}_2",
            f"{self.config['option_denomination']}_3",
            f"{self.config['option_denomination']}_4"
        ]
        
        for col_num, header in enumerate(headers, 1):
            cell = sheet.cell(row=1, column=col_num, value=header)
            cell.border = Border(bottom=Side(style='thin', color='000000'))
        
        Path(self.config["template_path"]).mkdir(parents=True, exist_ok=True)
        template_path = f"{self.config['template_path']}/{self.config['template_name']}"                
        workbook.save(template_path)
        return template_path
    

    # Checks if the i-question respects the params inside the configuration
    def _check_row(self, row: object) -> bool:
        base = (
            ((row[self.config['subject_denomination']] in self.config['subject']) if len(self.config['subject']) > 0 else True) and
            ((int(row[self.config['classroom_denomination']]) in self.config['classroom']) if len(self.config['classroom']) > 0 else True) and
            ((row[self.config['sector_denomination']] in self.config['sector']) if(len(self.config['sector'])) > 0 else True) and
            ((int(row[self.config['era_denomination']]) in self.config['era']) if(len(self.config['era'])) > 0 else True)
        )

        if self.config['single_inclusion']:
            return base and (row[self.config['include_denomination']] == self.config['include_accept_denomination'])
        else:
            return base

    # Creates the pool of questions that fit with the params inside the configuration
    def _pool_questions(self) -> None:
        self.questions = []
        
        for _, row in self.df.iterrows():
            if (self._check_row(row)):
                question = {
                    "question": str(row[self.config['question_denomination']]),
                    "options": []
                }
                
                for i in range(0, self.config['number_of_options']):
                    question["options"].append({"text": str(row[f'{self.config["option_denomination"]}_{i + 1}']),
                                                "correct": True if int(row[self.config['solution_denomination']]) == (i + 1) else False})
                
                self.questions.append(question)


    # Samples randomically a determinated number of questions from the pool
    def _sample_questions(self) -> list:
        if self.config['shuffle_questions']:
            random.shuffle(self.questions)
        
        if self.config['shuffle_options']:
            for question in self.questions:
                random.shuffle(question['options'])
        
        return self.questions[0: self.config['number_of_questions']]
    

    # Generates a new .docx with the sampled questions
    def _write_exam(self, questions: list, exam_number: int, solutions: bool) -> None:
        Word(
                questions,
                exam_number,
                solutions,
                self.config["document_title"],
                self.config["document_header"],
                self.config["number_on_document"],
                self.config["number_on_questions"],
                self.config["number_of_options"],
                self.config["destination_path"],
                self.config["file_name"]
        )
    

    # Generate multiple .docx documents, sampling new questions for every new document
    def _write_exams(self) -> None:
        Path(self.config["destination_path"]).mkdir(parents=True, exist_ok=True)
        questions = self._sample_questions()
        
        for i in range(0, self.config["number_of_exams"]):
            exam_number = i + 1
            self._write_exam(questions, exam_number, False)

            if self.config["export_solutions"]:
                self._write_exam(questions, exam_number, True)
            
            print(f"Generato esame {exam_number}...")


    def _zip_exams(self) -> None:
        zip_name = f"{self.config['zip_name']}.zip"
        with zipfile.ZipFile(f"{self.config['destination_path']}/{zip_name}", 'w') as zipf:
            for file in os.listdir(self.config["destination_path"]):
                if file.lower().endswith('.docx'):
                    docx_file_path = os.path.join(self.config["destination_path"], file)
                    zipf.write(docx_file_path, file)
                    os.remove(docx_file_path)


    def generate(self) -> None:
        self._pool_questions()
        self._write_exams()
        if self.config["include_to_zip"]: self._zip_exams()

        

        
