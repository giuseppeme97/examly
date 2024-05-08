import uuid
import os
import shutil
import hashlib


def delete_file(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)


def delete_folder(path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path)


def generate_source_name(file_object: object) -> tuple[str, str]:
    _, ext = os.path.splitext(file_object.filename)
    return (uuid.uuid4(), ext)


def get_paths(source_name: str, uploaded_folder_root: str) -> tuple[str, str]:
    id, _ = os.path.splitext(source_name)
    destination_path = f"{uploaded_folder_root}/{id}"
    source_path = f"{destination_path}/{source_name}"
    return (source_path, destination_path)


def save_source(file_object: str, uploaded_folder_root: str)  -> tuple[str, str]:
    id, ext = generate_source_name(file_object)
    uploaded_folder = f"{uploaded_folder_root}/{id}"
    source_name = f"{id}{ext}"
    source_path = f"{uploaded_folder}/{source_name}"    
    os.makedirs(uploaded_folder, exist_ok=True) 
    
    with open(source_path, "wb") as buffer:
        shutil.copyfileobj(file_object.file, buffer)

    return (source_name, source_path)


def get_hash_file(file_path: str) -> str:
    hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            hash.update(chunk)

    return hash.hexdigest()
