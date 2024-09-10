from fastapi import APIRouter
from fastapi import UploadFile, BackgroundTasks
from utils.utils import save_source, get_hash_file, delete_file, delete_folder, get_paths
from models.settings import UserSettings
from core.examsgenerator import ExamsGenerator
from core.config import config
from fastapi.responses import FileResponse
from utils.params import UPLOADED, TEMPLATE

router = APIRouter(
    prefix="/action"
)


@router.post("/generate-exams/")
def generate_exams(user_settings: UserSettings, background_tasks: BackgroundTasks): 
    source_path, destination_path = get_paths(user_settings.source_name, UPLOADED)
    
    config.update({
        "destination_path": destination_path,
        "source_path": source_path,
        "include_to_zip": True,
        "file_name": user_settings.file_name,
        "classroom": user_settings.classrooms,
        "document_title": user_settings.document_title,
        "export_solutions": user_settings.export_solutions,
        "number_of_exams": user_settings.number_of_exams,
        "number_of_questions": user_settings.number_of_questions,
        "number_on_document": user_settings.number_on_document,
        "number_on_questions": user_settings.number_on_questions,
        "shuffle_options": user_settings.shuffle_options,
        "shuffle_questions": user_settings.shuffle_questions,
        "single_inclusion": user_settings.single_inclusion,
        "subject": user_settings.subjects,
        "zip_name": user_settings.zip_name,
    })

    ExamsGenerator(config, autoload=True, autostart=True)
    zip_path = f"{destination_path}/{user_settings.zip_name}.zip"
    background_tasks.add_task(delete_folder, destination_path)
    return FileResponse(path=zip_path, media_type='application/octet-stream')


@router.get("/download-template/")
def download_template(background_tasks: BackgroundTasks): 
    gen = ExamsGenerator(config, autoload=False, autostart=False)
    template_path = gen.get_template()
    background_tasks.add_task(delete_file, template_path)
    return FileResponse(path=template_path, media_type='application/octet-stream',filename=TEMPLATE)


@router.post("/load-source/")
def load_source(file_object: UploadFile):     
    source_name, source_path = save_source(file_object, UPLOADED)
    config.update({"source_path": source_path})
    
    gen = ExamsGenerator(config, autoload=True, autostart=False)
    response = {
        "sourceName": source_name,
        "sha256": get_hash_file(source_path), 
        "rows": gen.get_rows(), 
        "subjects": gen.get_subjects(), 
        "classrooms": gen.get_classrooms()
    }  
    return response