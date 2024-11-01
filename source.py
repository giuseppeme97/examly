import os
import pandas as pd
from configs import Configuration

class Source:
    def __init__(self) -> None:
        self.loaded = False
        self.load()


    def is_loaded(self) -> bool:
        return self.loaded
        

    def load(self) -> None:
        _, ext = os.path.splitext(Configuration.get_source_file())

        if ext in Configuration.get_excel_formats_supported():
            reader = pd.read_excel

        if ext in Configuration.get_table_formats_supported():
            reader = pd.read_csv
            
        try:
            self.df = reader(Configuration.get_source_file())
            self.loaded = True
        except:
            self.loaded = False


    def get_subjects(self) -> list[str]:
        return sorted(pd.Series(self.df[Configuration.get_subject_denomination()].unique()).dropna().tolist()) 


    def get_classrooms(self) -> list[int]:
        return sorted(list(map(int, pd.Series(self.df[Configuration.get_classroom_denomination()].unique()).dropna().tolist())))
    

    def get_sectors(self) -> list[str]:
        return sorted(pd.Series(self.df[Configuration.get_sector_denomination()].unique()).dropna().tolist())
    

    def get_periods(self) -> list[str]:
        return sorted(pd.Series(self.df[Configuration.get_period_denomination()].unique()).dropna().tolist())


    def get_rows(self) -> int:
        return self.df.shape[0]

    
    def check_solutions(self) -> list[int]:
        logs = []
        for i, row in self.df.iterrows():
            if pd.isna(row[Configuration.get_solution_denomination()]):
                logs.append(i + 2)

        return logs 


    def check_questions(self) -> list[int]:
        logs = []
        for i, row in self.df.iterrows():
            if pd.isna(row[Configuration.get_question_denomination()]):
                logs.append(i + 2)
                
        return logs 
    

    def check_images(self) -> dict:
        founded_images = []
        missed_images = []

        for _, row in self.df.iterrows():
            if not pd.isna(row[Configuration.get_image_denomination()]):
                image_path = f"{Configuration.get_images_directory()}/{str(row[Configuration.get_image_denomination()])}"
                if os.path.isfile(image_path):
                    founded_images.append(image_path)
                else:
                    missed_images.append(image_path)
        
        return {
            "file_esistenti": founded_images,
            "file_mancanti": missed_images
        }
        

    def check_options_number(self) -> list[int]:
        logs = []
        for i, row in self.df.iterrows():
            missed_options = 0
            option_number = 1
            while f'{Configuration.get_option_denomination()}_{option_number}' in row:
                if pd.isna(row[f'{Configuration.get_option_denomination()}_{option_number}']):
                    missed_options += 1
                option_number = option_number + 1
            option_number = option_number - 1
            if option_number - missed_options == 1:
                logs.append(i + 2)
        return logs
    

    def check_orphan_questions(self) -> list[int]:
        logs = []
        for i, row in self.df.iterrows():
            if pd.isna(row[Configuration.get_subject_denomination()]) or pd.isna(row[Configuration.get_classroom_denomination()]) or pd.isna(row[Configuration.get_period_denomination()]) or pd.isna(row[Configuration.get_sector_denomination()]):
                logs.append(i + 2)
        return logs 
    

    def check_row(self, row: object) -> bool:
        base = (
            ((row[Configuration.get_subject_denomination()] in Configuration.get_subjects()) if len(Configuration.get_subjects()) > 0 else True) and
            ((int(row[Configuration.get_classroom_denomination()]) in Configuration.get_classrooms()) if len(Configuration.get_classrooms()) > 0 else True) and
            ((row[Configuration.get_sector_denomination()] in Configuration.get_sectors()) if(len(Configuration.get_sectors())) > 0 else True) and
            ((int(row[Configuration.get_period_denomination()]) in Configuration.get_periods()) if(len(Configuration.get_periods())) > 0 else True)
        )

        if Configuration.get_are_questions_single_included():
            return base and (row[Configuration.get_include_denomination()] == Configuration.get_include_accept_denomination())
        else:
            return base
        

    def get_image_path(self, row: object) -> str:
        image_path = f"{Configuration.get_images_directory()}/{str(row[Configuration.get_image_denomination()])}"
        if not pd.isna(row[Configuration.get_image_denomination()]) and os.path.isfile(image_path):
            return image_path
        else:
            return None


    def get_questions(self) -> tuple[list[dict], int]:
        questions = []
        
        for _, row in self.df.iterrows():
            if (self.check_row(row)):
                question = {
                    "question": str(row[Configuration.get_question_denomination()]),
                    "image": self.get_image_path(row),
                    "options": []
                }
                
                i = 1
                while f'{Configuration.get_option_denomination()}_{i}' in row:
                    if not pd.isna(row[f'{Configuration.get_option_denomination()}_{i}']):
                        question["options"].append({"text": str(row[f'{Configuration.get_option_denomination()}_{i}']),
                                                    "correct": True if int(row[Configuration.get_solution_denomination()]) == (i) else False})
                    i = i + 1
                
                questions.append(question)
        return (questions, len(questions))

        