import os
import pandas as pd

class Source:
    def __init__(self, config) -> None:
        self.config = config
        

    def load_source(self) -> bool:
        _, ext = os.path.splitext(self.config["source_file"])

        if ext in self.config["excel_formats_supported"]:
            reader = pd.read_excel

        if ext in self.config["table_formats_supported"]:
            reader = pd.read_csv
            
        try:
            self.df = reader(self.config["source_file"])
            return True
        except:
            return False


    def get_subjects(self) -> list[str]:
        return sorted(pd.Series(self.df[self.config["subject_denomination"]].unique()).dropna().tolist()) 


    def get_classrooms(self) -> list[int]:
        return sorted(list(map(int, pd.Series(self.df[self.config["classroom_denomination"]].unique()).dropna().tolist())))
    

    def get_sectors(self) -> list[str]:
        return sorted(pd.Series(self.df[self.config["sector_denomination"]].unique()).dropna().tolist())
    

    def get_periods(self) -> list[str]:
        return sorted(pd.Series(self.df[self.config["period_denomination"]].unique()).dropna().tolist())


    def get_rows(self) -> int:
        return self.df.shape[0]

    
    def check_solutions(self) -> list[int]:
        logs = []
        for i, row in self.df.iterrows():
            if pd.isna(row[self.config['solution_denomination']]):
                logs.append(i + 2)

        return logs 


    def check_questions(self) -> list[int]:
        logs = []
        for i, row in self.df.iterrows():
            if pd.isna(row[self.config['question_denomination']]):
                logs.append(i + 2)
                
        return logs 
    

    def check_images(self) -> dict:
        founded_images = []
        missed_images = []

        for _, row in self.df.iterrows():
            if not pd.isna(row[self.config['image_denomination']]):
                image_path = f"{self.config['images_directory']}/{str(row[self.config['image_denomination']])}"
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
            while f'{self.config["option_denomination"]}_{option_number}' in row:
                if pd.isna(row[f'{self.config["option_denomination"]}_{option_number}']):
                    missed_options += 1
                option_number = option_number + 1
            option_number = option_number - 1
            if option_number - missed_options == 1:
                logs.append(i + 2)
        return logs
    

    def check_orphan_questions(self) -> list[int]:
        logs = []
        for i, row in self.df.iterrows():
            if pd.isna(row[self.config['subject_denomination']]) or pd.isna(row[self.config['classroom_denomination']]) or pd.isna(row[self.config['period_denomination']]) or pd.isna(row[self.config['sector_denomination']]):
                logs.append(i + 2)
        return logs 
    

    def check_row(self, row: object) -> bool:
        base = (
            ((row[self.config['subject_denomination']] in self.config['subjects']) if len(self.config['subjects']) > 0 else True) and
            ((int(row[self.config['classroom_denomination']]) in self.config['classrooms']) if len(self.config['classrooms']) > 0 else True) and
            ((row[self.config['sector_denomination']] in self.config['sectors']) if(len(self.config['sectors'])) > 0 else True) and
            ((int(row[self.config['period_denomination']]) in self.config['periods']) if(len(self.config['periods'])) > 0 else True)
        )

        if self.config['are_questions_single_included']:
            return base and (row[self.config['include_denomination']] == self.config['include_accept_denomination'])
        else:
            return base
        

    def get_image_path(self, row: object) -> str:
        image_path = f"{self.config['images_directory']}/{str(row[self.config['image_denomination']])}"
        if not pd.isna(row[self.config['image_denomination']]) and os.path.isfile(image_path):
            return image_path
        else:
            return None


    def get_questions(self) -> tuple[list[dict], int]:
        questions = []
        
        for _, row in self.df.iterrows():
            if (self.check_row(row)):
                question = {
                    "question": str(row[self.config['question_denomination']]),
                    "image": self.get_image_path(row),
                    "options": []
                }
                
                i = 1
                while f'{self.config["option_denomination"]}_{i}' in row:
                    if not pd.isna(row[f'{self.config["option_denomination"]}_{i}']):
                        question["options"].append({"text": str(row[f'{self.config["option_denomination"]}_{i}']),
                                                    "correct": True if int(row[self.config['solution_denomination']]) == (i) else False})
                    i = i + 1
                
                questions.append(question)
        return (questions, len(questions))

        