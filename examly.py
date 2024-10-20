import pandas as pd
import random
import os
import zipfile
import openpyxl
from openpyxl.styles import Side, Border
from pathlib import Path
from word import Word
import json
import sys


class Examly():
    def __init__(self, config_filename) -> None:
        self.documents_config, self.word_config = self.get_configs(config_filename)


    def show_menu(self) -> None:
        pass


    def start(self) -> None:
        if self.load_source():
            filtered_questions = self.filter_questions()
            self.write_exams(filtered_questions)
            if self.documents_config["are_documents_included_to_zip"]: self.zip_exams()
        else:
            print("Errore nel caricamento della sorgente delle domande.")

    
    def set_config(self, config: dict) -> None:
        self.documents_config = config


    def load_config(self, config_path) -> dict:
        with open(config_path) as file:
            return json.load(file)
        

    def get_configs(self, config_filename: str) -> tuple[dict]:
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        document_config = self.load_config(f"{base_path}/{config_filename}")
        word_config = document_config["word"]
        document_config['source_path'] = f"{base_path}/{document_config['source_path']}"
        document_config['document_path'] = f"{base_path}/{document_config['document_path']}"
        document_config['template_path'] = f"{base_path}/{document_config['template_path']}"
        return (document_config, word_config)
    

    def check_source(self) -> None:
        pass


    def load_source(self) -> bool:
        _, ext = os.path.splitext(self.documents_config["source_path"])
            
        if ext in self.documents_config["excel_formats_supported"]:
            self.df = pd.read_excel(self.documents_config["source_path"])
        elif ext in self.documents_config["table_formats_supported"]:
            self.df = pd.read_csv(self.documents_config["source_path"], sep=";")
        else:
            return False
        
        # TODO: controllare la validità di tutte le righe
        # self.check_source()
        
        print("Sorgente caricata.\n")
        return True


    def get_subjects(self) -> list[str]:
        return sorted(pd.Series(self.df[self.documents_config["subject_denomination"]].unique()).dropna().tolist()) 


    def get_classrooms(self) -> list[int]:
        return sorted(list(map(int, pd.Series(self.df[self.documents_config["classroom_denomination"]].unique()).dropna().tolist())))


    def get_rows(self) -> int:
        return self.df.shape[0]


    def get_template(self) -> str:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        headers = [
            f"{self.documents_config['subject_denomination']}", 
            f"{self.documents_config['classroom_denomination']}",
            f"{self.documents_config['period_denomination']}",
            f"{self.documents_config['sector_denomination']}", 
            f"{self.documents_config['include_denomination']}", 
            f"{self.documents_config['question_denomination']}", 
            f"{self.documents_config['solution_denomination']}", 
            f"{self.documents_config['option_denomination']}_1",
            f"{self.documents_config['option_denomination']}_2",
            f"{self.documents_config['option_denomination']}_3",
            f"{self.documents_config['option_denomination']}_4"
        ]
        
        for col_num, header in enumerate(headers, 1):
            cell = sheet.cell(row=1, column=col_num, value=header)
            cell.border = Border(bottom=Side(style='thin', color='000000'))
        
        Path(self.documents_config["template_path"]).mkdir(parents=True, exist_ok=True)
        template_path = f"{self.documents_config['template_path']}/{self.documents_config['template_filename']}"                
        workbook.save(template_path)
        return template_path
    

    def check_row(self, row: object) -> bool:
        base = (
            ((row[self.documents_config['subject_denomination']] in self.documents_config['subjects']) if len(self.documents_config['subjects']) > 0 else True) and
            ((int(row[self.documents_config['classroom_denomination']]) in self.documents_config['classrooms']) if len(self.documents_config['classrooms']) > 0 else True) and
            ((row[self.documents_config['sector_denomination']] in self.documents_config['sectors']) if(len(self.documents_config['sectors'])) > 0 else True) and
            ((int(row[self.documents_config['period_denomination']]) in self.documents_config['periods']) if(len(self.documents_config['periods'])) > 0 else True)
        )

        if self.documents_config['are_questions_single_included']:
            return base and (row[self.documents_config['include_denomination']] == self.documents_config['include_accept_denomination'])
        else:
            return base


    def filter_questions(self) -> list[dict]:
        filtered_questions = []
        
        for _, row in self.df.iterrows():
            if (self.check_row(row)):
                question = {
                    "question": str(row[self.documents_config['question_denomination']]),
                    "options": []
                }
                
                # TODO: numero opzioni variabili
                for i in range(0, self.documents_config['options_number']):
                    question["options"].append({"text": str(row[f'{self.documents_config["option_denomination"]}_{i + 1}']),
                                                "correct": True if int(row[self.documents_config['solution_denomination']]) == (i + 1) else False})
                
                filtered_questions.append(question)
        
        return filtered_questions


    def sample_questions(self, questions: list[dict]) -> list[dict]:
        if self.documents_config['are_questions_shuffled']:
            random.shuffle(questions)
        
        if self.documents_config['are_options_shuffled']:
            for question in questions:
                random.shuffle(question['options'])
        
        return questions[0: self.documents_config['questions_number']]
    

    def write_exam(self, questions: list[dict], document_number: int, is_document_solution: bool) -> None:
        Word(
            self.word_config,
            questions,
            document_number,
            is_document_solution,
            self.documents_config["document_title"],
            self.documents_config["document_header"],
            self.documents_config["are_documents_numbered"],
            self.documents_config["are_questions_numbered"],
            self.documents_config["document_path"],
            self.documents_config["document_filename"]
        )
    

    def write_exams(self, filtered_questions: list[dict]) -> None:
        Path(self.documents_config["document_path"]).mkdir(parents=True, exist_ok=True)
        
        for i in range(0, self.documents_config["documents_number"]):
            document_number = i + 1
            sampled_questions = self.sample_questions(filtered_questions)
            self.write_exam(sampled_questions, document_number, is_document_solution=False)

            if self.documents_config["are_solutions_exported"]:
                self.write_exam(sampled_questions, document_number, is_document_solution=True)
            
            print(f"Generato esame {document_number}...")


    def zip_exams(self) -> None:
        zip_filename = f"{self.documents_config['zip_filename']}.zip"
        with zipfile.ZipFile(f"{self.documents_config['document_path']}/{zip_filename}", 'w') as zipf:
            for file in os.listdir(self.documents_config["document_path"]):
                if file.lower().endswith('.docx'):
                    docx_file_path = os.path.join(self.documents_config["document_path"], file)
                    zipf.write(docx_file_path, file)
                    os.remove(docx_file_path)



if __name__ == "__main__":
     e = Examly("config.json")
     e.start()
        
