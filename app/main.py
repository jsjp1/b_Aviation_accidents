from fastapi import FastAPI
import uvicorn
import api
from model import DescriptionUpdate

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "FastAPI"}


@app.get("/api/accident")
def read_recent_accident():
    return api.read_recent_accident()


@app.get("/api/accidents")
def read_accidents(start: int, size: int):
    return api.read_accidents(start, size)


@app.get("/api/suggestions/{airline}")
def read_airline_suggestions(airline: str):
    return api.read_airline_suggestions(airline)


@app.get("/api/information/{airline}")
def read_airline_info(airline: str):
    return api.read_airline_info(airline)


@app.get("/api/description/{_id}")
def read_airline_description(_id: str):
    return api.read_airline_description(_id)


@app.get("/api/ko_description/{_id}")
def read_airline_ko_description(_id: str):
    return api.read_airline_ko_description(_id)


@app.get("/api/check_ko_description/{_id}")
def check_ko_description(_id: str):
    is_empty = api.check_ko_description(_id)
    return {"ko_description_empty": is_empty}


@app.put("/api/ko_description/")
def update_ko_description(data: DescriptionUpdate):
    doc_id = data.doc_id
    description = data.description
    
    return api.update_ko_description(doc_id, description)


if __name__ == "__main__":
    uvicorn.run(
        "main:app", port=8000, host="0.0.0.0",
        reload=True, reload_dirs=["html_files"],
    )
