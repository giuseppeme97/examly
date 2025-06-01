from pydantic import BaseModel
from examly import Examly
from mongo import MongoConnector
from fastapi import FastAPI, UploadFile, File, HTTPException


app = FastAPI()
examly = Examly(web_mode=True)
mongo_connector = MongoConnector()


class BaseRequest(BaseModel):
    source: str
    filters: dict
    options: dict


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/filters/")
async def get_filters(item: BaseRequest):
    examly.connect_source(item.source)

    if examly.is_ready():
        return examly.get_filters()
    else:
        raise HTTPException(
            status_code=500, detail="Errore nel recupero dei filtri.")


@app.get("/sources/")
async def get_sources():
    return mongo_connector.get_all_collections()


@app.post("/sources/")
async def new_source(file: UploadFile = File(...)):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=400, detail="Il file deve essere un Excel (.xlsx o .xls)")

    try:
        content = await file.read()
        mongo_connector.new_collection(file.filename, content)
        return {"message": "OK"}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Errore durante la lettura del file: {str(e)}")


@app.post("/cardinality/")
async def get_cardinality(item: BaseRequest):
    examly.connect_source(item.source)

    if examly.is_ready():
        examly.set_filters(item.filters)
        return examly.get_questions_cardinality()
    else:
        raise HTTPException(
            status_code=500, detail="Errore nel recupero dei filtri.")
