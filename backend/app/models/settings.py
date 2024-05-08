from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

class UserSettings(BaseModel):
    source_name: str    # Nome del file originale caricato
    file_name: str      # Nome da attribuire ai file docx da generare
    zip_name: str     
    document_title: str 
    subjects: List[str]   
    classrooms: List[int]   
    number_of_exams: int
    number_of_questions: int  
    number_on_document: bool
    number_on_questions: bool
    shuffle_questions: bool
    shuffle_options: bool
    export_solutions: bool
    single_inclusion: bool
    