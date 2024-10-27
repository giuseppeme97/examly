import openpyxl
from openpyxl.styles import Side, Border
from pathlib import Path

class Template:
    def __init__(self, config) -> None:
        self.config = config
        self.workbook = openpyxl.Workbook()
        headers = [
            f"{self.config['subject_denomination']}", 
            f"{self.config['classroom_denomination']}",
            f"{self.config['period_denomination']}",
            f"{self.config['sector_denomination']}", 
            f"{self.config['include_denomination']}", 
            f"{self.config['question_denomination']}", 
            f"{self.config['images_denomination']}", 
            f"{self.config['solution_denomination']}", 
            f"{self.config['option_denomination']}_1",
            f"{self.config['option_denomination']}_2",
            f"{self.config['option_denomination']}_3",
            f"{self.config['option_denomination']}_4"
        ]
        
        for col_num, header in enumerate(headers, 1):
            self.workbook.active.cell(row=1, column=col_num, value=header).border = Border(bottom=Side(style='thin', color='000000'))


    def save_tempale(self) -> bool:
        Path(self.config["template_directory"]).mkdir(parents=True, exist_ok=True)
        template_path = f"{self.config['template_directory']}/{self.config['template_filename']}" 
        try:               
            self.workbook.save(template_path)
            return True
        except:
            return False
        
