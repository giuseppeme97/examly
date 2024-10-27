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


    def get_rows(self) -> int:
        return self.df.shape[0]
    

    def check_all(self) -> bool:
        return self.check_solution_option() and self.check_incomplete_questions() and self.check_options_number()

    
    def check_solution_option(self) -> bool:
        logs = []
        for i, row in self.df.iterrows():
            if pd.isna(row[self.config['solution_denomination']]):
                logs.append(i)

        return len(logs) == 0 


    def check_incomplete_questions(self) -> bool:
        logs = []
        for i, row in self.df.iterrows():
            if pd.isna(row[self.config['question_denomination']]):
                logs.append(i)
                
        return len(logs) == 0 
        


    def check_options_number(self) -> bool:
        return True
    

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
        

    def check_image(self, row: object) -> str:
        if not pd.isna(row[self.config['image_denomination']]):
            return f"{self.config['images_directory']}/{str(row[self.config['image_denomination']])}"
        else:
            return None


    def get_questions(self) -> list[dict]:
        questions = []
        
        for _, row in self.df.iterrows():
            if (self.check_row(row)):
                question = {
                    "question": str(row[self.config['question_denomination']]),
                    "image": self.check_image(row),
                    "options": []
                }
                
                i = 1
                while f'{self.config["option_denomination"]}_{i}' in row:
                    if not pd.isna(row[f'{self.config["option_denomination"]}_{i}']):
                        question["options"].append({"text": str(row[f'{self.config["option_denomination"]}_{i}']),
                                                    "correct": True if int(row[self.config['solution_denomination']]) == (i) else False})
                    i = i + 1
                
                questions.append(question)
        return questions

        