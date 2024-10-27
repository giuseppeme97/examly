import os
import sys

config = {
    "working_path": "/Users/giuseppe/Documents/examly",
    "source_file": "Domande.xlsx",
    "documents_directory": "output",
    "images_directory": "images",
    "template_directory": "template",
    "template_filename": "template.xlsx",
    "document_filename": "esame",
    "zip_filename": "compito",
    "subjects": ["INFORMATICA"],
    "classrooms": [4],
    "periods": [],
    "sectors": ["TEORIA"],
    "document_title": "Compito di Informatica - A.S. 2024/2025 - Classe 4H",
    "document_header": "Cognome e Nome: ________________________________________________________",
    "documents_number": 1,
    "questions_number": 100,
    "export_log": False,
    "are_pages_numbered": True,
    "are_documents_numbered": True,
    "are_questions_numbered": True,
    "are_questions_shuffled": True,
    "are_options_shuffled": True,
    "are_solutions_exported": True,
    "are_questions_single_included": True,
    "are_documents_exported_to_pdf": False,
    "are_documents_included_to_zip": False, 
    "excel_formats_supported": [".xlsx", ".xls"],
    "table_formats_supported": [".csv"],
    "subject_denomination": "MATERIA",
    "classroom_denomination": "CLASSE",
    "period_denomination": "PERIODO",
    "sector_denomination": "SETTORE",
    "include_denomination": "INCLUDERE",
    "question_denomination": "DOMANDA",
    "image_denomination": "IMMAGINE",
    "solution_denomination": "CORRETTA",
    "option_denomination": "OPZIONE",
    "include_accept_denomination": "SI",
    "word": {
        "font": "Liberation Sans",
        "language": "it-IT",
        "title_size": 15,    
        "questions_size": 11,
        "images_size": 2.5,
        "questions_distance": 3,
        "questions_RGB_color": [0, 0, 0],
        "columns_number": 2,
        "left_margin": 1,
        "right_margin": 1,
        "DSA": False
    }
}

def set_config():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    config['source_file'] = f"{config['working_path']}/{config['source_file']}"
    config['documents_directory'] = f"{config['working_path']}/{config['documents_directory']}"
    config['images_directory'] = f"{config['working_path']}/{config['images_directory']}"
    config['template_directory'] = f"{config['working_path']}/{config['template_directory']}"
    print("***")

set_config()