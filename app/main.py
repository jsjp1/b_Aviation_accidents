from fastapi import FastAPI
import uvicorn
import api
from model import DescriptionUpdate

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "FastAPI"}


@app.get("/api/accident")
async def read_recent_accident():
    return await api.read_recent_accident()


@app.get("/api/accidents")
async def read_accidents(start: int, size: int):
    return await api.read_accidents(start, size)


@app.get("/api/suggestions/{airline}")
async def read_airline_suggestions(airline: str):
    return await api.read_airline_suggestions(airline)


@app.get("/api/information/{airline}")
async def read_airline_info(airline: str):
    return await api.read_airline_info(airline)


@app.get("/api/description/{_id}")
async def read_airline_description(_id: str):
    return await api.read_airline_description(_id)


@app.get("/api/ko_description/{_id}")
async def read_airline_ko_description(_id: str):
    return await api.read_airline_ko_description(_id)


@app.get("/api/check_ko_description/{_id}")
async def check_ko_description(_id: str):
    is_empty = await api.check_ko_description(_id)
    return {"ko_description_empty": is_empty}


@app.put("/api/ko_description/")
async def update_ko_description(data: DescriptionUpdate):
    doc_id = data.doc_id
    description = data.description
    
    return await api.update_ko_description(doc_id, description)


if __name__ == "__main__":
    uvicorn.run(
        "main:app", port=8000, host="0.0.0.0",
        reload=True, reload_dirs=["html_files"],
    )
