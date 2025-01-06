from fastapi import FastAPI
import uvicorn
import api

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "FastAPI"}


@app.get("/api/accidents")
def read_accidents(start: int, size: int):
    return api.read_accidents(start, size)


@app.get("/api/suggestions/{airline}")
def read_airline_suggestions(airline: str):
    return api.read_airline_suggestions(airline)


@app.get("/api/information/{airline}")
def read_airline_info(airline: str):
    return api.read_airline_info(airline)


@app.get("/api/description/{airline}/{date}")
def read_airline_description(airline: str, date: str):
    return api.read_airline_description(airline, date)


if __name__ == "__main__":
    uvicorn.run(
        "main:app", port=8000, host="0.0.0.0",
        reload=True, reload_dirs=["html_files"],
    )
