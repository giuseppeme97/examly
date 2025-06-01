from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from examly import Examly

app = FastAPI()
examly = Examly()


class BaseRequest(BaseModel):
    source: str
    filters: dict
    options: dict


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/filters/")
async def get_filters(item: BaseRequest):
    examly.set_source(item.source, True)
    examly.load_source()
    
    if examly.is_ready():
        return examly.get_filters()
    else:
        raise HTTPException(
            status_code=500,
            detail="Errore nel recupero dei filtri."
        )

@app.post("/cardinality/")
async def get_cardinality(item: BaseRequest):
    examly.set_source(item.source, True)
    examly.load_source()
    
    if examly.is_ready():
        examly.set_filters(item.filters)
        return examly.get_questions_cardinality()
    else:
        raise HTTPException(
            status_code=500,
            detail="Errore nel recupero dei filtri."
        )


