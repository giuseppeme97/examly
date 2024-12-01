import openpyxl
from openpyxl.styles import Side, Border
from pathlib import Path
from configs import Configuration

class Template:
    def __init__(self) -> None:
        self.workbook = openpyxl.Workbook()
        headers = [
            f"{Configuration.get_subject_denomination()}", 
            f"{Configuration.get_classroom_denomination()}",
            f"{Configuration.get_period_denomination()}",
            f"{Configuration.get_sector_denomination()}", 
            f"{Configuration.get_include_denomination()}", 
            f"{Configuration.get_question_denomination()}", 
            f"{Configuration.get_image_denomination()}", 
            f"{Configuration.get_solution_denomination()}", 
            f"{Configuration.get_option_denomination()}_1",
            f"{Configuration.get_option_denomination()}_2",
            f"{Configuration.get_option_denomination()}_3",
            f"{Configuration.get_option_denomination()}_4"
        ]
        
        for col_num, header in enumerate(headers, 1):
            self.workbook.active.cell(row=1, column=col_num, value=header).border = Border(bottom=Side(style='thin', color='000000'))


    def save(self) -> str:
        Path(Configuration.get_template_directory()).mkdir(parents=True, exist_ok=True)
        template_path = f"{Configuration.get_template_directory()}/{Configuration.get_template_filename()}" 
        try:               
            self.workbook.save(template_path)
            return template_path
        except:
            return None
        

def get_template():
    template = Template()
    return template.save()
        
